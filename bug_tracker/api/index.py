import sys
import os

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Set VERCEL environment variable
os.environ['VERCEL'] = '1'

# Import and create app
from app import app

# Vercel expects 'handler' to be the WSGI application
handler = app


