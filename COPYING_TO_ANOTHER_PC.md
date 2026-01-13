# Copying This Project to Another PC

## ✅ Yes, it will work! But follow these steps:

### What to Copy

**Copy these files/folders:**
- ✅ All `.py` files (app.py, config.py, medical_parser.py, utils.py, etc.)
- ✅ `templates/` folder (HTML files)
- ✅ `requirements.txt` file
- ✅ `config.py` (your settings)
- ✅ All `.md` documentation files (optional)
- ✅ `build_*.bat` / `build_*.sh` files (if building executables)
- ✅ `app.spec` (if building executables)

**DO NOT copy:**
- ❌ `venv/` folder (virtual environment - platform-specific and large)
- ❌ `__pycache__/` folders (Python cache)
- ❌ `*.pyc` files (compiled Python files)
- ❌ `.cache/` folders
- ❌ Any downloaded Whisper models (they'll download automatically)

### Setup Steps on New PC

1. **Install Python** (if not already installed)
   - Download from: https://www.python.org/downloads/
   - Make sure to check "Add Python to PATH" during installation
   - Python 3.8 or higher required

2. **Copy the project folder** (excluding venv folder)

3. **Create a virtual environment** (recommended):
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Install Whisper** (if using Whisper):
   ```bash
   pip install openai-whisper
   ```
   Note: Whisper models will download automatically on first use (~500MB for 'small' model)

6. **Run the application**:
   ```bash
   python app.py
   # or
   python3 app.py
   ```

### What Happens Automatically

- ✅ **Whisper models**: Will download automatically on first use (one-time download)
- ✅ **Configuration**: Your `config.py` settings are preserved
- ✅ **Dependencies**: Install from `requirements.txt`

### Important Notes

1. **Virtual Environment (venv)**: 
   - DON'T copy the `venv/` folder - it's platform-specific
   - Create a new one on the new PC

2. **Whisper Models**:
   - Located in: `~/.cache/whisper/` (macOS/Linux) or `C:\Users\YourName\.cache\whisper\` (Windows)
   - NOT in your project folder
   - Will download automatically (one-time, ~500MB for 'small' model)

3. **Platform Differences**:
   - Works on Windows, macOS, and Linux
   - Use appropriate Python commands (`python` vs `python3`)
   - Use appropriate script files (`.bat` for Windows, `.sh` for macOS/Linux)

4. **Internet Required**:
   - First run: To install packages and download Whisper model
   - After setup: Only for translation (Google Translate API)
   - Speech recognition works offline after initial setup (if using local Whisper)

### Quick Start Scripts

**One script does everything!**

**Windows:**
- Double-click `start_windows.bat` - Automatically sets up (first time) and starts the app

**macOS/Linux:**
- Run: `chmod +x start_macos.sh && ./start_macos.sh` - Automatically sets up (first time) and starts the app

The script automatically:
- ✅ Checks if setup is needed (first time only)
- ✅ Creates virtual environment (if needed)
- ✅ Installs all dependencies (if needed)
- ✅ Installs Whisper (if needed)
- ✅ Starts the application
- ✅ Everything is automatic!

### Checklist for Copying

- [ ] Python installed on new PC (3.8+)
- [ ] Copied all code files (excluding venv/)
- [ ] Created new virtual environment
- [ ] Installed dependencies (`pip install -r requirements.txt`)
- [ ] Installed Whisper (`pip install openai-whisper`)
- [ ] Test run the application
- [ ] Whisper model downloads automatically on first use

### Troubleshooting

**"Python not found"**:
- Install Python and add it to PATH

**"Module not found" errors**:
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt`

**"Whisper model not found"**:
- This is normal on first run
- Model will download automatically (check internet connection)
- Takes a few minutes (~500MB download)

**Port already in use**:
- Change `PORT` in `config.py` to a different number (e.g., 5002, 5003)

## Summary

✅ **Yes, copying the code folder works!**
✅ **Just need to:**
   - Install Python
   - Create new virtual environment
   - Install dependencies
   - Models download automatically

❌ **Don't copy:**
   - `venv/` folder
   - `__pycache__/` folders
   - Already downloaded models (they're not in the project folder anyway)

