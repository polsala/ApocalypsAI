#!/usr/bin/env python3
"""
Sample Python application for Nightly Docker DevBox
"""

import sys
import os
from datetime import datetime


def main():
    """Main application function"""
    print("🐍 Welcome to the Python Development Environment!")
    print(f"Python version: {sys.version}")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Working directory: {os.getcwd()}")
    
    # Demonstrate some basic Python functionality
    print("\n📊 Basic Python functionality:")
    
    # List comprehension
    squares = [x**2 for x in range(1, 11)]
    print(f"Squares 1-10: {squares}")
    
    # Dictionary comprehension
    word_lengths = {word: len(word) for word in ["hello", "world", "python", "devbox"]}
    print(f"Word lengths: {word_lengths}")
    
    # Try importing some common packages
    try:
        import requests
        print(f"✓ requests version: {requests.__version__}")
    except ImportError:
        print("✗ requests not available")
    
    try:
        import numpy
        print(f"✓ numpy version: {numpy.__version__}")
    except ImportError:
        print("✗ numpy not available")
    
    try:
        import pandas
        print(f"✓ pandas version: {pandas.__version__}")
    except ImportError:
        print("✗ pandas not available")
    
    print("\n🎉 Python environment is ready for development!")


if __name__ == "__main__":
    main()
