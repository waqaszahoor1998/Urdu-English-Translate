@echo off
REM Build script for Windows executable
echo Building Windows executable...

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install PyInstaller if not available
python -m pip install pyinstaller

REM Run the build script
python build_executable.py

REM Pause to see the results
pause

