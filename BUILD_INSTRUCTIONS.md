# Building Executables for Windows and macOS

This guide explains how to create standalone executable files for the Urdu Voice Translation App.

## Prerequisites

- Python 3.7 or higher installed
- All dependencies installed (run `pip install -r requirements.txt`)
- PyInstaller will be installed automatically by the build scripts

## Quick Start

### For Windows:
1. Double-click `build_windows.bat`
2. Wait for the build to complete
3. Find the executable in the `dist` folder: `UrduVoiceTranslator.exe`

### For macOS:
1. Open Terminal
2. Navigate to the project directory
3. Run: `chmod +x build_macos.sh && ./build_macos.sh`
4. Find the executable in the `dist` folder: `UrduVoiceTranslator`

## Manual Build Process

### Step 1: Install PyInstaller
```bash
pip install pyinstaller
```

### Step 2: Build the Executable

**Windows:**
```bash
pyinstaller --name=UrduVoiceTranslator --onefile --windowed --add-data="templates;templates" app.py
```

**macOS/Linux:**
```bash
pyinstaller --name=UrduVoiceTranslator --onefile --windowed --add-data="templates:templates" app.py
```

**With console (for debugging):**
Replace `--windowed` with `--console` to see error messages.

### Step 3: Using the Spec File (Recommended)

1. Edit `app.spec` if needed (already configured)
2. Build using the spec file:
   ```bash
   pyinstaller app.spec
   ```

## Build Options Explained

- `--onefile`: Creates a single executable file (easier to distribute)
- `--windowed`: No console window (use `--console` for debugging)
- `--add-data`: Includes the templates folder
- `--name`: Name of the executable
- `--hidden-import`: Ensures modules are included

## File Structure After Build

```
project/
├── build/          # Temporary build files (can be deleted)
├── dist/           # Final executable is here
│   └── UrduVoiceTranslator[.exe]
├── app.spec        # PyInstaller configuration
└── ...
```

## Distributing the Executable

1. **Windows:**
   - Copy `dist/UrduVoiceTranslator.exe` to the target computer
   - Users can double-click to run (no Python needed)
   - May need to allow the app through Windows Defender

2. **macOS:**
   - Copy `dist/UrduVoiceTranslator` to the target Mac
   - Users may need to allow it in Security & Privacy settings
   - Right-click → Open (first time only) to bypass Gatekeeper

## Troubleshooting

### "App can't be opened" (macOS)
- Right-click the app → Open
- Or: System Preferences → Security & Privacy → Allow

### Missing Template Errors
- Ensure `--add-data` includes the templates folder
- Check the path separator (; for Windows, : for macOS/Linux)

### Large Executable Size
- Normal! PyInstaller bundles Python and all dependencies
- Typical size: 50-150 MB
- This is expected for Python applications

### Executable Runs but Server Doesn't Start
- Build with `--console` instead of `--windowed` to see errors
- Check if the port (5001) is already in use

### Dependencies Missing
- Add missing modules to `--hidden-import` in the spec file
- Rebuild after adding imports

## Creating a GUI Wrapper (Optional)

For a more user-friendly experience, you can create a simple GUI:

1. Install tkinter (usually comes with Python)
2. Create a GUI launcher that:
   - Shows a window with "Start" button
   - Opens the browser automatically
   - Shows status messages

Example GUI launcher code can be added if needed.

## Advanced Options

### Code Signing (macOS)
To avoid Gatekeeper warnings:
```bash
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" dist/UrduVoiceTranslator
```

### Creating Installer (Windows)
Use tools like:
- Inno Setup
- NSIS (Nullsoft Scriptable Install System)
- WiX Toolset

### Creating DMG (macOS)
```bash
hdiutil create -volname "UrduVoiceTranslator" -srcfolder dist -ov -format UDZO UrduVoiceTranslator.dmg
```

## Notes

- First run of the executable may be slower (extracting files)
- Antivirus software may flag PyInstaller executables (false positive)
- Users still need internet connection (for translation services)
- Whisper models (if used) are not included by default (users need to download separately)

## File Size Considerations

The executable will be large (50-150MB) because it includes:
- Python interpreter
- Flask and all dependencies
- All Python libraries

This is normal for PyInstaller applications.

## Alternative: Portable Python Distribution

Instead of executables, you could:
1. Use Portable Python
2. Include a batch/shell script to run the app
3. Package everything in a ZIP file

This results in smaller distribution but requires users to have some technical knowledge.

