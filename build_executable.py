#!/usr/bin/env python3
"""
Build script to create executable for Urdu Voice Translation App
Works on both Windows and macOS
"""
import sys
import os
import shutil
import subprocess
from pathlib import Path

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """Install PyInstaller"""
    print("Installing PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_executable():
    """Build the executable"""
    # Get the script directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    # Check if PyInstaller is installed
    if not check_pyinstaller():
        print("PyInstaller not found. Installing...")
        install_pyinstaller()
    
    # Clean previous builds
    for dir_name in ['build', 'dist', '__pycache__']:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}...")
            shutil.rmtree(dir_name)
    
    # Remove old spec file if exists
    spec_file = script_dir / 'app.spec'
    if spec_file.exists():
        spec_file.unlink()
    
    print("\n" + "="*60)
    print("Building executable...")
    print("="*60 + "\n")
    
    # Build command
    build_cmd = [
        'pyinstaller',
        '--name=UrduVoiceTranslator',
        '--onefile',
        '--windowed',  # No console window (use --console for debugging)
        '--add-data=templates;templates',  # Windows format (use : for macOS/Linux)
        '--hidden-import=flask',
        '--hidden-import=speech_recognition',
        '--hidden-import=deep_translator',
        '--hidden-import=pydub',
        '--hidden-import=whisper',
        '--hidden-import=openai',
        '--hidden-import=config',
        '--collect-all=flask',
        '--collect-all=speech_recognition',
        '--collect-all=deep_translator',
        '--collect-all=pydub',
        'app.py'
    ]
    
    # Adjust for macOS/Linux
    if sys.platform != 'win32':
        build_cmd[4] = '--add-data=templates:templates'
        build_cmd[0] = 'pyinstaller'
    
    try:
        subprocess.check_call(build_cmd)
        print("\n" + "="*60)
        print("✅ Build successful!")
        print("="*60)
        print(f"\nExecutable location: {script_dir / 'dist' / 'UrduVoiceTranslator'}")
        if sys.platform == 'win32':
            print("Windows: dist/UrduVoiceTranslator.exe")
        else:
            print("macOS/Linux: dist/UrduVoiceTranslator")
        print("\nYou can distribute the executable from the 'dist' folder.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    build_executable()

