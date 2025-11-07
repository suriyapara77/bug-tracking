from flask import Blueprint, request, jsonify, render_template
from functools import lru_cache
from typing import Optional, Dict, List, Any
from datetime import datetime
from sqlalchemy import or_
import os
import re
import logging

# Configure logging
logger = logging.getLogger(__name__)

chatbot_bp = Blueprint('chatbot', __name__)

# Constants
PRIORITY_ORDER = {'High': 3, 'Medium': 2, 'Low': 1}
MAX_ISSUES_LIMIT = 10
MAX_RESPONSE_TOKENS = 500

# Regex patterns as constants
ASSIGNEE_PATTERNS = [
    r"what (?:is|are) (\w+) (?:working on|doing|assigned to)",
    r"(\w+)'s (?:tasks|issues|work)",
    r"show (?:me )?(?:issues|tasks) (?:for|assigned to|of) (\w+)(?:\s|$)",
    r"what (?:does|is) (\w+) (?:have|working on)",
    r"who (?:is|are) (\w+)",
]

TASK_SUGGESTION_PATTERNS = [
    r"suggest (?:a|one) (?:task|issue) (?:to work on|for me|to do)",
    r"what (?:task|issue) (?:should|can) i (?:work on|do|tackle)",
    r"give me (?:a|one) (?:task|issue) (?:to work on|suggestion)",
    r"recommend (?:a|one) (?:task|issue)",
    r"what (?:should|can) i (?:work on|do next)",
]

PRIORITY_PATTERNS = [
    r"(?:top|high|highest) priority (?:tasks|issues)",
    r"(?:suggest|show|give me) (?:tasks|priorities)",
    r"what (?:are|is) the (?:top|most important) (?:tasks|issues)",
    r"(?:urgent|important) (?:tasks|issues)",
]

STATUS_PATTERNS = [
    r"(?:open|in-progress|closed) (?:issues|tasks)",
    r"show (?:me )?(?:all )?(?:open|in-progress|closed)",
]

COMMON_WORDS = {'what', 'show', 'who', 'me', 'all', 'the', 'top', 'high', 'is', 'are'}


class ChatbotService:
    """Service class for chatbot operations"""
    
    @staticmethod
    def get_openai_client():
        """Get OpenAI client with error handling"""
        try:
            from openai import OpenAI
            api_key = os.environ.get('OPENAI_API_KEY')
            if not api_key:
                logger.warning("OpenAI API key not found")
                return None
            return OpenAI(api_key=api_key)
        except ImportError:
            logger.error("OpenAI package not installed")
            return None
        except Exception as e:
            logger.error(f"Error initializing OpenAI client: {e}")
            return None
    
    @staticmethod
    def get_models():
        """Get database models"""
        from models import Issue, User
        from extensions import db
        return Issue, User, db


class MessageParser:
    """Parse and extract intent from user messages"""
    
    @staticmethod
    def extract_assignee(message: str) -> Optional[str]:
        """Extract assignee name from message"""
        message_lower = message.lower()
        
        for pattern in ASSIGNEE_PATTERNS:
            match = re.search(pattern, message_lower)
            if match:
                potential_name = match.group(1).capitalize()
                if potential_name.lower() not in COMMON_WORDS:
                    return potential_name
        return None
    
    @staticmethod
    def extract_status(message: str) -> Optional[str]:
        """Extract status from message"""
        message_lower = message.lower()
        
        for pattern in STATUS_PATTERNS:
            if re.search(pattern, message_lower):
                if 'open' in message_lower:
                    return 'Open'
                elif 'in-progress' in message_lower or 'in progress' in message_lower:
                    return 'In-Progress'
                elif 'closed' in message_lower:
                    return 'Closed'
        return None
    
    @staticmethod
    def is_task_suggestion(message: str) -> bool:
        """Check if message is asking for task suggestion"""
        return any(re.search(p, message.lower()) for p in TASK_SUGGESTION_PATTERNS)
    
    @staticmethod
    def is_priority_query(message: str) -> bool:
        """Check if message is asking about priorities"""
        return any(re.search(p, message.lower()) for p in PRIORITY_PATTERNS)
    
    @classmethod
    def parse(cls, message: str) -> Dict[str, Any]:
        """Parse message and extract all intents"""
        return {
            'assignee_name': cls.extract_assignee(message),
            'is_priority_query': cls.is_priority_query(message),
            'is_task_suggestion': cls.is_task_suggestion(message),
            'status': cls.extract_status(message),
            'original_message': message
        }


class IssueQueryService:
    """Service for querying issues from database"""
    
    @staticmethod
    def query_by_assignee(assignee_name: str) -> List[Dict]:
        """Query issues assigned to a specific person"""
        Issue, User, db = ChatbotService.get_models()
        
        try:
            # Use case-insensitive search with better matching
            user = User.query.filter(User.name.ilike(f'%{assignee_name}%')).first()
            
            if not user:
                logger.info(f"User not found: {assignee_name}")
                return []
            
            issues = Issue.query.filter_by(assignee_id=user.id).all()
            return [issue.to_dict() for issue in issues]
        except Exception as e:
            logger.error(f"Error querying by assignee: {e}")
            return []
    
    @staticmethod
    def query_priority_issues() -> List[Dict]:
        """Query top priority issues (High priority, then Medium, excluding Closed)"""
        Issue, User, db = ChatbotService.get_models()
        
        try:
            high_priority = Issue.query.filter(
                Issue.priority == 'High',
                Issue.status != 'Closed'
            ).order_by(Issue.created_at.desc()).limit(MAX_ISSUES_LIMIT).all()
            
            all_issues = list(high_priority)
            
            if len(high_priority) < MAX_ISSUES_LIMIT:
                medium_priority = Issue.query.filter(
                    Issue.priority == 'Medium',
                    Issue.status != 'Closed'
                ).order_by(Issue.created_at.desc()).limit(MAX_ISSUES_LIMIT - len(high_priority)).all()
                all_issues.extend(medium_priority)
            
            return [issue.to_dict() for issue in all_issues]
        except Exception as e:
            logger.error(f"Error querying priority issues: {e}")
            return []
    
    @staticmethod
    def query_by_status(status: str) -> List[Dict]:
        """Query issues by status"""
        Issue, User, db = ChatbotService.get_models()
        
        try:
            issues = Issue.query.filter_by(status=status).order_by(Issue.created_at.desc()).all()
            return [issue.to_dict() for issue in issues]
        except Exception as e:
            logger.error(f"Error querying by status: {e}")
            return []
    
    @staticmethod
    def query_suggested_task() -> Optional[Dict]:
        """Query best task suggestion (Open, ordered by priority and due date)"""
        Issue, User, db = ChatbotService.get_models()
        
        try:
            open_issues = Issue.query.filter_by(status='Open').all()
            
            if not open_issues:
                return None
            
            # Sort by priority (desc) then due_date (asc)
            sorted_issues = sorted(
                open_issues,
                key=lambda issue: (
                    -PRIORITY_ORDER.get(issue.priority, 0),
                    issue.due_date if issue.due_date else datetime.max
                )
            )
            
            return sorted_issues[0].to_dict() if sorted_issues else None
        except Exception as e:
            logger.error(f"Error querying suggested task: {e}")
            return None
    
    @staticmethod
    def query_active_issues() -> List[Dict]:
        """Query all active (Open or In-Progress) issues"""
        Issue, User, db = ChatbotService.get_models()
        
        try:
            issues = Issue.query.filter(
                or_(Issue.status == 'Open', Issue.status == 'In-Progress')
            ).order_by(
                Issue.priority.desc(),
                Issue.created_at.desc()
            ).limit(MAX_ISSUES_LIMIT).all()
            
            return [issue.to_dict() for issue in issues]
        except Exception as e:
            logger.error(f"Error querying active issues: {e}")
            return []


class ResponseFormatter:
    """Format responses for user"""
    
    @staticmethod
    def format_issues_for_llm(issues: List[Dict]) -> str:
        """Format issues data for LLM context"""
        if not issues:
            return "No issues found."
        
        formatted = []
        for issue in issues:
            assignee_info = (
                f"Assigned to: {issue['assignee']['name']} ({issue['assignee']['role']})"
                if issue.get('assignee') else "Unassigned"
            )
            due_date_info = f"Due: {issue['due_date']}" if issue.get('due_date') else "No due date"
            
            formatted.append(
                f"ID: {issue['id']}\n"
                f"Title: {issue['title']}\n"
                f"Description: {issue['description']}\n"
                f"Status: {issue['status']}\n"
                f"Priority: {issue['priority']}\n"
                f"{assignee_info}\n"
                f"{due_date_info}\n"
                f"Created: {issue['created_at']}\n"
            )
        
        return "\n---\n".join(formatted)
    
    @staticmethod
    def format_simple_task_suggestion(task: Dict) -> str:
        """Format a simple task suggestion without LLM"""
        assignee = task.get('assignee', {}).get('name', 'Unassigned') if task.get('assignee') else 'Unassigned'
        due_date = task.get('due_date', 'No due date')
        
        if due_date and due_date != 'No due date':
            try:
                due_date_obj = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                due_date = due_date_obj.strftime('%Y-%m-%d')
            except Exception:
                pass
        
        return (
            f"I suggest you work on: {task['title']}\n\n"
            f"Description: {task['description']}\n"
            f"Priority: {task['priority']}\n"
            f"Due Date: {due_date}\n"
            f"Assigned to: {assignee}"
        )
    
    @staticmethod
    def format_simple_issues_list(issues: List[Dict], query_context: str) -> str:
        """Format a simple list of issues without LLM"""
        response_text = f"{query_context}\n\n"
        for issue in issues[:5]:  # Limit to 5 for readability
            assignee = issue.get('assignee', {}).get('name', 'Unassigned') if issue.get('assignee') else 'Unassigned'
            response_text += f"- {issue['title']} ({issue['status']}, {issue['priority']} priority, Assigned to: {assignee})\n"
        return response_text


class LLMService:
    """Service for LLM interactions"""
    
    @staticmethod
    def get_system_prompt(is_task_suggestion: bool) -> str:
        """Get appropriate system prompt"""
        if is_task_suggestion:
            return """You are a helpful assistant for a bug tracking system. 
The user is asking for a task suggestion. You should recommend ONE specific task from the Open issues, 
prioritizing by: 1) Priority (High > Medium > Low), 2) Earliest due date.
Be enthusiastic and encouraging. Explain why this task is a good choice.
Format your response in a natural, conversational way.
If there are no Open issues, politely inform the user."""
        else:
            return """You are a helpful assistant for a bug tracking system. 
You help users understand their issues and tasks. 
Be concise, friendly, and informative. 
Format your response in a natural, conversational way.
If there are no issues, politely inform the user."""
    
    @staticmethod
    def generate_response(
        client,
        user_message: str,
        query_context: str,
        issues_text: str,
        is_task_suggestion: bool
    ) -> str:
        """Generate LLM response"""
        system_prompt = LLMService.get_system_prompt(is_task_suggestion)
        
        user_prompt = f"""User asked: "{user_message}"

{query_context}

Here are the relevant issues from the database:

{issues_text}

Please provide a natural, conversational response to the user's question based on this data."""
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=MAX_RESPONSE_TOKENS
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            raise


# Routes
@chatbot_bp.route('/chat', methods=['GET'])
def chat_page():
    """Render the chatbot page"""
    return render_template('chatbot.html')


@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint that parses messages and queries the database"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Validate message length
        if len(user_message) > 500:
            return jsonify({'error': 'Message too long (max 500 characters)'}), 400
        
        # Parse the message
        parsed = MessageParser.parse(user_message)
        
        # Query database based on parsed intent
        issues_data = []
        query_context = ""
        suggested_task = None
        
        if parsed['is_task_suggestion']:
            suggested_task = IssueQueryService.query_suggested_task()
            if suggested_task:
                issues_data = [suggested_task]
                query_context = "Found a suggested task based on priority and due date."
            else:
                query_context = "No Open issues available to suggest."
        elif parsed['assignee_name']:
            issues_data = IssueQueryService.query_by_assignee(parsed['assignee_name'])
            query_context = f"Found {len(issues_data)} issue(s) assigned to {parsed['assignee_name']}."
        elif parsed['is_priority_query']:
            issues_data = IssueQueryService.query_priority_issues()
            query_context = f"Found {len(issues_data)} high priority issue(s)."
        elif parsed['status']:
            issues_data = IssueQueryService.query_by_status(parsed['status'])
            query_context = f"Found {len(issues_data)} {parsed['status']} issue(s)."
        else:
            issues_data = IssueQueryService.query_active_issues()
            query_context = f"Found {len(issues_data)} active issue(s)."
        
        # Format issues for LLM
        issues_text = ResponseFormatter.format_issues_for_llm(issues_data)
        
        # Get OpenAI client
        openai_client = ChatbotService.get_openai_client()
        
        # If OpenAI is not available, return a simple formatted response
        if not openai_client:
            if parsed['is_task_suggestion']:
                if suggested_task:
                    response_text = ResponseFormatter.format_simple_task_suggestion(suggested_task)
                    return jsonify({'message': response_text}), 200
                else:
                    return jsonify({'message': "I don't have any Open issues to suggest at the moment."}), 200
            elif issues_data:
                response_text = ResponseFormatter.format_simple_issues_list(issues_data, query_context)
                return jsonify({'message': response_text}), 200
            else:
                return jsonify({'message': f"{query_context} No issues match your query."}), 200
        
        # Generate LLM response
        bot_message = LLMService.generate_response(
            openai_client,
            user_message,
            query_context,
            issues_text,
            parsed['is_task_suggestion']
        )
        
        return jsonify({'message': bot_message}), 200
    
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}")
        return jsonify({'error': 'An error occurred processing your request'}), 500


@chatbot_bp.route('/api/chatbot', methods=['POST'])
def chatbot():
    """Legacy endpoint - redirects to /chat"""
    return chat()