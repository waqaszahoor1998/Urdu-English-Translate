# Urdu Voice to English Translation

A web application that converts Urdu voice input to text and translates it to English, with optional medical prescription formatting.

## ✨ Features

- 🎤 Real-time voice recording in Urdu
- 📝 Automatic speech-to-text conversion (Whisper or Google Speech API)
- 🌐 Translation from Urdu to English
- 🏥 Optional medical prescription formatting
- 🔍 Language detection (English/Urdu)
- 💻 Beautiful, modern web interface
- 📱 Responsive design for mobile and desktop

## 🚀 Quick Start (Easiest Way)

### For Windows:
**Just double-click `start_windows.bat`** - it handles everything automatically!

### For macOS/Linux:
```bash
chmod +x start_macos.sh
./start_macos.sh
```

That's it! The script will:
- ✅ Check Python installation
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Start the application
- ✅ Open in your browser

**First run takes 2-5 minutes** (one-time setup). After that, it starts immediately!

## 📋 Manual Installation (Alternative)

If you prefer manual setup:

1. **Requirements:**
   - Python 3.7 or higher
   - Microphone access in your browser
   - Internet connection (for translation services)

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install system dependencies (optional, for better audio processing):**

   **For macOS:**
   ```bash
   brew install portaudio ffmpeg
   ```

   **For Ubuntu/Debian:**
   ```bash
   sudo apt-get install portaudio19-dev python3-pyaudio ffmpeg
   ```

   **For Windows:**
   - Download and install [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - Install [ffmpeg](https://ffmpeg.org/download.html) and add it to PATH

4. **Start the application:**
   ```bash
   python app.py
   ```

5. **Open your browser:**
   ```
   http://localhost:5001
   ```

## 🎯 Usage

1. Click the **"Click to Record"** button and allow microphone access
2. **Speak in Urdu or English** - The application will:
   - Record your voice
   - Convert it to text
   - Translate to English (if Urdu detected)
   - Display both original and translated text
3. Click **"Format as Prescription"** (optional) to format medical text

## 🔧 How It Works

1. **Voice Input**: Browser's MediaRecorder API captures audio
2. **Speech Recognition**: 
   - Whisper (local, recommended) - Works offline, best accuracy
   - Google Speech API (fallback) - Requires internet
3. **Language Detection**: Automatically detects English or Urdu
4. **Translation**: Google Translate API (Urdu → English)
5. **Medical Formatting**: Optional prescription formatting for medical text

## 📝 Notes

- **No API keys required** - Works out of the box!
- **Offline speech recognition** - If Whisper is installed (downloads automatically)
- **Internet required** - For translation service (always needed)
- **First run** - Whisper models download automatically (~500MB, one-time)
- **Best results** - Chrome, Firefox, or Edge browsers
- **Clear audio** - Speak clearly in a quiet environment

## 🏥 Medical Features

- Automatic extraction of medications, tests, and patient descriptions
- Optional prescription formatting with "Format as Prescription" button
- Works with both Urdu and English medical terminology

## Troubleshooting

- **Microphone not working**: Check browser permissions and allow microphone access
- **No translation**: Check your internet connection
- **Audio format errors**: Make sure ffmpeg is installed for audio conversion
- **PortAudio errors**: Install the system dependencies mentioned above

## License

This project is open source and available for personal and commercial use.

