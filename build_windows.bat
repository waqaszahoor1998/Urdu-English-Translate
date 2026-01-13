@echo off
echo ========================================
echo Building Urdu Voice Translation App Executable
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

echo [1/4] Python found!
python --version
echo.

REM Check if virtual environment exists, if not create it
if not exist "venv\" (
    echo [2/4] Virtual environment not found. Creating...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo       Virtual environment created!
    echo.
    echo [3/4] Installing dependencies...
    echo       This may take a few minutes...
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install pyinstaller
    echo       Dependencies installed!
) else (
    echo [2/4] Virtual environment found.
    call venv\Scripts\activate.bat
    echo.
    echo [3/4] Checking dependencies...
    python -c "import flask" >nul 2>&1
    if errorlevel 1 (
        echo       Installing missing dependencies...
        pip install --upgrade pip
        pip install -r requirements.txt
    )
    python -c "import PyInstaller" >nul 2>&1
    if errorlevel 1 (
        echo       Installing PyInstaller...
        pip install pyinstaller
    )
    echo       All dependencies ready!
)
echo.

echo [4/4] Building executable with PyInstaller...
echo       This may take several minutes...
echo       Please wait...
echo.

python build_executable.py

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed! Check the error messages above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Executable created in the 'dist' folder:
echo   dist\UrduVoiceTranslator.exe
echo.
echo You can now distribute this .exe file to other Windows computers.
echo No Python installation needed on the target computer!
echo.
pause
