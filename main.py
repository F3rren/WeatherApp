#!/usr/bin/env python3
"""
Entry point for MeteoApp.
This file allows running the app from the project root.
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app.main import run

if __name__ == "__main__":
    run()
