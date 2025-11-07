from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
from extensions import db
from models import Issue, User

issues_bp = Blueprint('issues', __name__)

@issues_bp.route('/')
def index():
    return render_template('index.html')

@issues_bp.route('/calendar')
def calendar():
    return render_template('calendar.html')

@issues_bp.route('/issue/new')
def issue_form():
    return render_template('issue_form.html')

@issues_bp.route('/issue/<int:issue_id>/edit')
def edit_issue_form(issue_id):
    return render_template('issue_form.html', issue_id=issue_id)

@issues_bp.route('/issues', methods=['GET'])
def get_issues():
    # Start with base query
    query = Issue.query
    
    # Filter by title (search)
    title = request.args.get('title')
    if title:
        query = query.filter(Issue.title.ilike(f'%{title}%'))
    
    # Filter by status
    status = request.args.get('status')
    if status:
        query = query.filter(Issue.status == status)
    
    # Filter by assignee_id
    assignee_id = request.args.get('assignee_id')
    if assignee_id:
        try:
            assignee_id = int(assignee_id)
            query = query.filter(Issue.assignee_id == assignee_id)
        except ValueError:
            pass  # Invalid assignee_id, ignore
    
    # Filter by assignee name (search in related User)
    assignee_name = request.args.get('assignee')
    if assignee_name:
        # Use outer join to include issues without assignees if needed
        query = query.outerjoin(User, Issue.assignee_id == User.id).filter(
            User.name.ilike(f'%{assignee_name}%')
        )
    
    # Execute query
    issues = query.all()
    return jsonify([issue.to_dict() for issue in issues])

@issues_bp.route('/issues', methods=['POST'])
def create_issue():
    data = request.json
    
    # Validate required fields
    if not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    if not data.get('description'):
        return jsonify({'error': 'Description is required'}), 400
    
    # Handle assignee_id - convert empty string to None
    assignee_id = data.get('assignee_id')
    if assignee_id == '' or assignee_id is None:
        assignee_id = None
    else:
        try:
            assignee_id = int(assignee_id)
        except (ValueError, TypeError):
            assignee_id = None
    
    # Handle due_date
    due_date = None
    if data.get('due_date'):
        try:
            due_date = datetime.fromisoformat(data['due_date'])
        except (ValueError, TypeError):
            due_date = None
    
    issue = Issue(
        title=data.get('title'),
        description=data.get('description'),
        status=data.get('status', 'Open'),
        priority=data.get('priority', 'Medium'),
        assignee_id=assignee_id,
        due_date=due_date
    )
    db.session.add(issue)
    db.session.commit()
    return jsonify(issue.to_dict()), 201

@issues_bp.route('/issues/<int:issue_id>', methods=['GET'])
def get_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    return jsonify(issue.to_dict())

@issues_bp.route('/issues/<int:issue_id>', methods=['PUT'])
def update_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    data = request.json
    
    # Update fields if provided
    if 'title' in data:
        issue.title = data.get('title')
    if 'description' in data:
        issue.description = data.get('description')
    if 'status' in data:
        issue.status = data.get('status')
    if 'priority' in data:
        issue.priority = data.get('priority')
    if 'assignee_id' in data:
        issue.assignee_id = data.get('assignee_id')
    if 'due_date' in data:
        if data.get('due_date'):
            issue.due_date = datetime.fromisoformat(data['due_date'])
        else:
            issue.due_date = None
    
    db.session.commit()
    return jsonify(issue.to_dict())

@issues_bp.route('/issues/<int:issue_id>', methods=['DELETE'])
def delete_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    db.session.delete(issue)
    db.session.commit()
    return jsonify({'message': 'Issue deleted successfully'}), 200

@issues_bp.route('/issues/<int:issue_id>/status', methods=['PATCH'])
def update_issue_status(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    data = request.json
    
    # Validate status value
    new_status = data.get('status')
    if not new_status:
        return jsonify({'error': 'Status is required'}), 400
    
    # Validate status is one of the allowed values
    allowed_statuses = ['Open', 'In-Progress', 'Closed']
    if new_status not in allowed_statuses:
        return jsonify({'error': f'Status must be one of: {", ".join(allowed_statuses)}'}), 400
    
    issue.status = new_status
    db.session.commit()
    return jsonify(issue.to_dict())

# User routes
@issues_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@issues_bp.route('/api/users', methods=['GET'])
def get_api_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@issues_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    
    # Validate required fields
    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    if not data.get('role'):
        return jsonify({'error': 'Role is required'}), 400
    
    # Check if user with same name already exists
    existing_user = User.query.filter_by(name=data.get('name')).first()
    if existing_user:
        return jsonify({'error': 'User with this name already exists'}), 400
    
    new_user = User(
        name=data.get('name'),
        role=data.get('role')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@issues_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Check if user has assigned issues
    assigned_issues = Issue.query.filter_by(assignee_id=user_id).all()
    
    if assigned_issues:
        # Option 1: Prevent deletion if user has assigned issues
        return jsonify({
            'error': f'Cannot delete user. User has {len(assigned_issues)} assigned issue(s). Please reassign or delete those issues first.'
        }), 400
        
        # Option 2 (alternative): Set assignee_id to None for all assigned issues
        # Uncomment the lines below if you prefer this behavior:
        # for issue in assigned_issues:
        #     issue.assignee_id = None
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

@issues_bp.route('/users/new')
def user_form():
    return render_template('user_form.html')