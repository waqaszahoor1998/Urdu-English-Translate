#!/bin/bash

echo "========================================"
echo "Urdu Voice Translation App"
echo "========================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed!"
    echo "Please install Python 3 from https://www.python.org/downloads/"
    exit 1
fi

# Check if virtual environment exists, if not create it and install dependencies
if [ ! -d "venv" ]; then
    echo "[SETUP] Virtual environment not found. Setting up..."
    echo ""
    echo "[1/4] Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment!"
        exit 1
    fi
    echo "      Virtual environment created!"
    echo ""
    
    echo "[2/4] Activating virtual environment..."
    source venv/bin/activate
    echo ""
    
    echo "[3/4] Installing dependencies..."
    echo "      This may take a few minutes..."
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies!"
        exit 1
    fi
    echo "      Dependencies installed!"
    echo ""
    
    echo "[4/4] Installing Whisper..."
    pip install openai-whisper
    echo "      Whisper installed! Models will download automatically on first use."
    echo ""
    echo "Setup complete! Starting application..."
    echo ""
else
    source venv/bin/activate
fi

# Check if Flask is installed (quick check)
python3 -c "import flask" &> /dev/null
if [ $? -ne 0 ]; then
    echo "[SETUP] Dependencies not found. Installing..."
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
    pip install openai-whisper
    echo ""
fi

echo "Starting application..."
echo ""
echo "The app will open in your browser automatically."
echo "If it doesn't, go to: http://127.0.0.1:5001"
echo ""
echo "Press Ctrl+C to stop the server."
echo ""

# Run the application
python3 app.py

