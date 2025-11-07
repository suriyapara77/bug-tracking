from flask import Flask
from flask_cors import CORS
from extensions import db
from config import Config
from datetime import datetime, timedelta

def create_app():
    # Get the base directory (bug_tracker folder)
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Initialize Flask with explicit template and static folders
    # This ensures templates and static files are found correctly in serverless environments
    app = Flask(__name__, 
                template_folder=os.path.join(base_dir, 'templates'),
                static_folder=os.path.join(base_dir, 'static'))
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    from routes.issues import issues_bp
    from routes.chatbot import chatbot_bp
    
    app.register_blueprint(issues_bp)
    app.register_blueprint(chatbot_bp)
    
    # Create database tables and seed data
    with app.app_context():
        db.create_all()
        seed_data()
    
    return app

def seed_data():
    """Seed the database with sample users and issues"""
    from models import User, Issue
    
    try:
        # Check if data already exists
        if User.query.first() is not None:
            return  # Data already seeded
    except Exception as e:
        # If query fails, database might not be ready yet
        import logging
        logging.warning(f"Could not check for existing data: {e}")
        return
    
    try:
        # Create sample users
        users = [
            User(name='Alex', role='Developer'),
            User(name='Maddy', role='QA Engineer'),
            User(name='Sarah', role='Project Manager'),
            User(name='John', role='Developer'),
            User(name='Emily', role='Designer'),
        ]
        
        for user in users:
            db.session.add(user)
        db.session.commit()
        
        # Get user IDs after commit
        alex = User.query.filter_by(name='Alex').first()
        maddy = User.query.filter_by(name='Maddy').first()
        sarah = User.query.filter_by(name='Sarah').first()
        john = User.query.filter_by(name='John').first()
        emily = User.query.filter_by(name='Emily').first()
        
        # Verify all users were created successfully
        if not all([alex, maddy, sarah, john, emily]):
            import logging
            logging.warning("Not all users were created successfully")
            return  # Exit early if users are missing
    except Exception as e:
        import logging
        logging.warning(f"Error creating users: {e}")
        db.session.rollback()
        return  # Exit early if user creation fails
    
    # Calculate dates for the current week
    today = datetime.now()
    # Get Monday of current week (Monday = 0, Sunday = 6)
    days_since_monday = today.weekday()
    monday = today.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days_since_monday)
    
    # Create sample issues with various statuses, priorities, and due dates
    issues = [
        # High priority issues for Alex
        Issue(
            title='Fix login authentication bug',
            description='Users are unable to log in with their credentials. Need to investigate and fix the authentication flow.',
            status='Open',
            priority='High',
            assignee_id=alex.id,
            due_date=monday + timedelta(days=1)  # Tuesday
        ),
        Issue(
            title='Implement user profile page',
            description='Create a new user profile page with edit functionality and avatar upload.',
            status='In-Progress',
            priority='High',
            assignee_id=alex.id,
            due_date=monday + timedelta(days=3)  # Thursday
        ),
        Issue(
            title='Optimize database queries',
            description='Review and optimize slow database queries in the dashboard endpoint.',
            status='Open',
            priority='Medium',
            assignee_id=alex.id,
            due_date=monday + timedelta(days=5)  # Saturday
        ),
        
        # Issues for Maddy
        Issue(
            title='Test payment integration',
            description='Write comprehensive tests for the new payment integration feature.',
            status='Open',
            priority='High',
            assignee_id=maddy.id,
            due_date=monday + timedelta(days=2)  # Wednesday
        ),
        Issue(
            title='Review pull request #123',
            description='Review and test the changes in pull request #123 before merging.',
            status='In-Progress',
            priority='Medium',
            assignee_id=maddy.id,
            due_date=monday + timedelta(days=4)  # Friday
        ),
        Issue(
            title='Update test documentation',
            description='Update the test documentation with new test cases and procedures.',
            status='Open',
            priority='Low',
            assignee_id=maddy.id,
            due_date=monday + timedelta(days=6)  # Sunday
        ),
        
        # Issues for Sarah
        Issue(
            title='Plan sprint 15',
            description='Plan and organize tasks for sprint 15, including backlog grooming.',
            status='Open',
            priority='High',
            assignee_id=sarah.id,
            due_date=monday  # Monday
        ),
        Issue(
            title='Client meeting preparation',
            description='Prepare presentation and materials for the upcoming client meeting.',
            status='In-Progress',
            priority='Medium',
            assignee_id=sarah.id,
            due_date=monday + timedelta(days=1)  # Tuesday
        ),
        
        # Issues for John
        Issue(
            title='Refactor API endpoints',
            description='Refactor the REST API endpoints to follow best practices and improve maintainability.',
            status='Open',
            priority='Medium',
            assignee_id=john.id,
            due_date=monday + timedelta(days=2)  # Wednesday
        ),
        Issue(
            title='Add error logging',
            description='Implement comprehensive error logging system for better debugging.',
            status='Closed',
            priority='Low',
            assignee_id=john.id,
            due_date=monday - timedelta(days=2)  # Past date
        ),
        
        # Issues for Emily
        Issue(
            title='Design new dashboard UI',
            description='Create mockups and designs for the new dashboard user interface.',
            status='Open',
            priority='High',
            assignee_id=emily.id,
            due_date=monday + timedelta(days=3)  # Thursday
        ),
        Issue(
            title='Update brand colors',
            description='Update the application with new brand colors and styling guidelines.',
            status='In-Progress',
            priority='Medium',
            assignee_id=emily.id,
            due_date=monday + timedelta(days=4)  # Friday
        ),
        
        # Unassigned issues
        Issue(
            title='Security audit',
            description='Conduct a comprehensive security audit of the application.',
            status='Open',
            priority='High',
            assignee_id=None,
            due_date=monday + timedelta(days=1)  # Tuesday
        ),
        Issue(
            title='Update dependencies',
            description='Update all project dependencies to their latest stable versions.',
            status='Open',
            priority='Low',
            assignee_id=None,
            due_date=monday + timedelta(days=5)  # Saturday
        ),
    ]
    
    try:
        for issue in issues:
            db.session.add(issue)
        
        db.session.commit()
        import logging
        logging.info("Sample data seeded successfully!")
    except Exception as e:
        import logging
        logging.warning(f"Error seeding issues: {e}")
        db.session.rollback()
        # Don't raise - app should still work without seed data

# Create app instance for flask run
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)