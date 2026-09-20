# wsgi.py
"""
WSGI entry point for hosting on PythonAnywhere, Render, or production servers.
"""

import os
import sys

# Add the project root directory to sys.path
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from web.app import app as application

if __name__ == "__main__":
    application.run()
