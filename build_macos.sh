#!/bin/bash
# Build script for macOS executable

echo "Building macOS executable..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Install PyInstaller if not available
python3 -m pip install pyinstaller

# Run the build script
python3 build_executable.py

echo ""
echo "Build complete! Check the 'dist' folder for the executable."

