#!/usr/bin/env python3
"""
Simple launcher script for the Urdu Voice Translation App
Opens the browser automatically when the server starts
"""
import webbrowser
import time
import sys
import os
from threading import Timer

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from config import PORT, HOST

def open_browser():
    """Open the browser after a short delay"""
    time.sleep(1.5)  # Wait for server to start
    url = f"http://{HOST}:{PORT}"
    webbrowser.open(url)

if __name__ == '__main__':
    # Open browser in a separate thread
    Timer(1.5, open_browser).start()
    
    print("="*60)
    print("Urdu Voice to English Translation")
    print("="*60)
    print(f"\nServer starting on http://{HOST}:{PORT}")
    print("Browser will open automatically...")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        app.run(debug=False, port=PORT, host=HOST, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\nServer stopped. Goodbye!")
        sys.exit(0)

