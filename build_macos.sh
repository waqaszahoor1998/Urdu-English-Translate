#!/bin/bash

echo "========================================"
echo "Building Urdu Voice Translation App Executable"
echo "========================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed!"
    echo "Please install Python 3 from https://www.python.org/downloads/"
    exit 1
fi

echo "[1/4] Python found!"
python3 --version
echo ""

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "[2/4] Virtual environment not found. Creating..."
    python3 -m venv venv
    source venv/bin/activate
    echo "      Virtual environment created!"
    echo ""
    echo "[3/4] Installing dependencies..."
    echo "      This may take a few minutes..."
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install pyinstaller
    echo "      Dependencies installed!"
else
    echo "[2/4] Virtual environment found."
    source venv/bin/activate
    echo ""
    echo "[3/4] Checking dependencies..."
    if ! python3 -c "import flask" &> /dev/null; then
        echo "      Installing missing dependencies..."
        pip install --upgrade pip
        pip install -r requirements.txt
    fi
    if ! python3 -c "import PyInstaller" &> /dev/null; then
        echo "      Installing PyInstaller..."
        pip install pyinstaller
    fi
    echo "      All dependencies ready!"
fi
echo ""

echo "[4/4] Building executable with PyInstaller..."
echo "      This may take several minutes..."
echo "      Please wait..."
echo ""

python3 build_executable.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Build failed! Check the error messages above."
    exit 1
fi

echo ""
echo "========================================"
echo "Build Complete!"
echo "========================================"
echo ""
echo "Executable created in the 'dist' folder:"
echo "  dist/UrduVoiceTranslator"
echo ""
echo "You can now distribute this file to other macOS computers."
echo "No Python installation needed on the target computer!"
echo ""
