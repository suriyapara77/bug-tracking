import sys
import os

# Add the parent directory (bug_tracker) to the path so we can import app
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from app import app

# This is the entry point for Vercel serverless functions
# Vercel will automatically call this handler for all routes

