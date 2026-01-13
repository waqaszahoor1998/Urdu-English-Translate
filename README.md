# Urdu Voice to English Translation

A web application that converts Urdu voice input to text and translates it to English.

## Features

- 🎤 Real-time voice recording in Urdu
- 📝 Automatic speech-to-text conversion for Urdu
- 🌐 Translation from Urdu to English
- 💻 Beautiful, modern web interface
- 📱 Responsive design for mobile and desktop

## Requirements

- Python 3.7 or higher
- Microphone access in your browser
- Internet connection (for Google Speech API and translation services)

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install system dependencies:**

   **For macOS:**
   ```bash
   brew install portaudio
   ```

   **For Ubuntu/Debian:**
   ```bash
   sudo apt-get install portaudio19-dev python3-pyaudio ffmpeg
   ```

   **For Windows:**
   - Download and install [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - Install [ffmpeg](https://ffmpeg.org/download.html) and add it to PATH

## Usage

1. **Start the Flask server:**
   ```bash
   python app.py
   ```

2. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

3. **Click the "Click to Record" button** and allow microphone access when prompted

4. **Speak in Urdu** - The application will:
   - Record your voice
   - Convert it to Urdu text
   - Translate it to English
   - Display both the Urdu text and English translation

## How It Works

1. **Voice Input**: Uses the browser's MediaRecorder API to capture audio
2. **Speech Recognition**: Converts audio to text using Google Speech Recognition API (supports Urdu - ur-PK)
3. **Translation**: Translates the Urdu text to English using Google Translate API

## Notes

- Make sure to speak clearly and in a quiet environment for best results
- The first use may take longer as it adjusts for ambient noise
- Internet connection is required for speech recognition and translation services
- Best results are achieved with Chrome, Firefox, or Edge browsers

## Troubleshooting

- **Microphone not working**: Check browser permissions and allow microphone access
- **No translation**: Check your internet connection
- **Audio format errors**: Make sure ffmpeg is installed for audio conversion
- **PortAudio errors**: Install the system dependencies mentioned above

## License

This project is open source and available for personal and commercial use.

