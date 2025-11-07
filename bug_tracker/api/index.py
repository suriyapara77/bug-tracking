import sys
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the parent directory (bug_tracker) to the path so we can import app
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Set VERCEL environment variable if not set (Vercel usually sets this automatically)
if not os.environ.get('VERCEL'):
    os.environ['VERCEL'] = '1'

# Ensure /tmp directory exists for SQLite on Vercel
if os.environ.get('VERCEL'):
    tmp_dir = '/tmp'
    if not os.path.exists(tmp_dir):
        try:
            os.makedirs(tmp_dir, exist_ok=True)
        except Exception as e:
            logger.warning(f"Could not create /tmp directory: {e}")

try:
    logger.info(f"Current directory: {current_dir}")
    logger.info(f"Parent directory: {parent_dir}")
    logger.info(f"Python path: {sys.path[:3]}")
    
    from app import app
    handler = app
    logger.info("Flask app imported successfully")
except ImportError as e:
    # More detailed error for import issues
    logger.error(f"Failed to import app: {e}", exc_info=True)
    logger.error(f"Current working directory: {os.getcwd()}")
    logger.error(f"Files in parent_dir: {os.listdir(parent_dir) if os.path.exists(parent_dir) else 'N/A'}")
    raise
except Exception as e:
    # Log error for debugging
    logger.error(f"Failed to initialize app: {e}", exc_info=True)
    raise


