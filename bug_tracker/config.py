import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # For Vercel deployment, use /tmp for SQLite (only writable location)
    # For production, consider using PostgreSQL or another cloud database
    if os.environ.get('VERCEL'):
        # On Vercel, use /tmp for database (only writable location)
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:////tmp/bug_tracker.db'
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///bug_tracker.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False


