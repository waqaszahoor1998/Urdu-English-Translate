@echo off
echo ========================================
echo Urdu Voice Translation App
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Check if virtual environment exists, if not create it and install dependencies
if not exist "venv\" (
    echo [SETUP] Virtual environment not found. Setting up...
    echo.
    echo [1/4] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo       Virtual environment created!
    echo.
    
    echo [2/4] Activating virtual environment...
    call venv\Scripts\activate.bat
    echo.
    
    echo [3/4] Installing dependencies...
    echo       This may take a few minutes...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies!
        pause
        exit /b 1
    )
    echo       Dependencies installed!
    echo.
    
    echo [4/4] Installing Whisper...
    pip install openai-whisper
    echo       Whisper installed! Models will download automatically on first use.
    echo.
    echo Setup complete! Starting application...
    echo.
) else (
    call venv\Scripts\activate.bat
)

REM Check if Flask is installed (quick check)
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [SETUP] Dependencies not found. Installing...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    pip install openai-whisper
    echo.
)

echo Starting application...
echo.
echo The app will open in your browser automatically.
echo If it doesn't, go to: http://127.0.0.1:5001
echo.
echo Press Ctrl+C to stop the server.
echo.

REM Run the application
python app.py

pause

