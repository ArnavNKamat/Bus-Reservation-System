# run_web.py
"""
Convenient launcher for the Bus Reservation Web Application.
Run: python run_web.py
"""

import os
import sys

# Ensure current directory is in python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from web.app import app

if __name__ == "__main__":
    print("=" * 60)
    print("  Starting Goa Bus Reservation System Web Server...")
    print("  Access the web app at: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5000, debug=False)
