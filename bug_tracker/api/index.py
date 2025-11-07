import sys
import os

# Add the parent directory (bug_tracker) to the path so we can import app
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Set VERCEL environment variable if not set (Vercel usually sets this automatically)
if not os.environ.get('VERCEL'):
    os.environ['VERCEL'] = '1'

from app import app

# Export the app for Vercel's Python runtime
# Vercel automatically handles WSGI conversion for Flask apps
# The app variable is what Vercel will use as the handler
handler = app


