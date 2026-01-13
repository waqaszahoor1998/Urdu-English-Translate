# Quick Start Guide

## 🚀 Fastest Way to Get Started

### For Windows Users:

1. **Double-click `start_windows.bat`**
   - First time: Automatically installs everything (2-5 minutes)
   - After that: Starts the app immediately
   - App opens in your browser automatically
   - Start recording! 🎤

### For macOS/Linux Users:

1. **Run: `./start_macos.sh`**
   ```bash
   chmod +x start_macos.sh
   ./start_macos.sh
   ```
   - First time: Automatically installs everything (2-5 minutes)
   - After that: Starts the app immediately
   - App opens in your browser automatically
   - Start recording! 🎤

## 📋 What the Script Does:

- ✅ Checks if Python is installed
- ✅ Creates virtual environment (if needed)
- ✅ Installs all dependencies (if needed)
- ✅ Installs Whisper (if needed)
- ✅ Starts the application
- ✅ Everything automatic - no manual steps!

## 🎯 That's It!

Just one script - it handles everything automatically!

- **First run**: Sets up everything (one-time setup)
- **Subsequent runs**: Starts immediately (fast!)

## 📝 Notes:

- **First run**: Whisper models (~500MB) download automatically (one-time)
- **Internet needed**: For translation (Google Translate API)
- **No API keys**: Everything works free out of the box!

## 🔧 Troubleshooting:

**"Python not found"**:
- Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

**Setup fails**:
- Make sure you have internet connection
- Check that Python is installed correctly
- Try running the script as administrator (Windows)

**App won't start**:
- Check that port 5001 is not in use
- Try changing PORT in config.py

## 🏗️ Building Executable (Optional):

If you want to create a standalone executable:

**Windows**: Double-click `build_windows.bat`
**macOS/Linux**: Run `./build_macos.sh`
