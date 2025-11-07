import sys
import os
import traceback

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Set VERCEL environment variable
os.environ['VERCEL'] = '1'

# Import and create app with error handling
try:
    from app import app
    handler = app
except Exception as e:
    # Print detailed error for Vercel logs
    print(f"ERROR: Failed to import app: {e}")
    print(f"Traceback: {traceback.format_exc()}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    print(f"Files in parent_dir: {os.listdir(parent_dir) if os.path.exists(parent_dir) else 'N/A'}")
    raise


