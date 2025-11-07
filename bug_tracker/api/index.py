import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the parent directory (bug_tracker) to the path so we can import app
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Set VERCEL environment variable if not set (Vercel usually sets this automatically)
if not os.environ.get('VERCEL'):
    os.environ['VERCEL'] = '1'

try:
    from app import app
    handler = app
    logger.info("Flask app imported successfully")
except Exception as e:
    # Log error for debugging
    logger.error(f"Failed to import app: {e}", exc_info=True)
    raise


