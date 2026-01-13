from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from deep_translator import GoogleTranslator
import io
import base64
from pydub import AudioSegment
from pydub.effects import normalize
import tempfile
import os
import sys
import logging
from config import (
    MAX_AUDIO_SIZE_MB, MAX_AUDIO_DURATION_SECONDS,
    SPEECH_LANGUAGE, SPEECH_LANGUAGE_GOOGLE, TRANSLATION_SOURCE, TRANSLATION_TARGET,
    LOG_LEVEL, SPEECH_ENGINE, WHISPER_MODEL, OPENAI_API_KEY, USE_OPENAI_API
)

# Configure logging first
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to import Whisper (optional dependency)
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    logger.warning("Whisper not available. Install with: pip install openai-whisper")

# Try to import OpenAI API (optional)
try:
    import openai
    OPENAI_AVAILABLE = True
    if USE_OPENAI_API and OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
except ImportError:
    OPENAI_AVAILABLE = False
    if USE_OPENAI_API:
        logger.warning("OpenAI library not available. Install with: pip install openai")

# Handle PyInstaller path for templates
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    app = Flask(__name__, template_folder=template_folder)
else:
    # Running as script
    app = Flask(__name__)

# Global Whisper model (load once, reuse)
_whisper_model = None

def get_whisper_model():
    """Load Whisper model (lazy loading)"""
    global _whisper_model
    if _whisper_model is None and WHISPER_AVAILABLE:
        try:
            logger.info(f"Loading Whisper model: {WHISPER_MODEL}")
            _whisper_model = whisper.load_model(WHISPER_MODEL)
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {str(e)}")
            _whisper_model = False  # Mark as failed
    return _whisper_model

def recognize_with_whisper(audio_path):
    """Recognize speech using OpenAI Whisper (local)"""
    if not WHISPER_AVAILABLE:
        return None
    
    try:
        model = get_whisper_model()
        if model is None or model is False:
            return None
        
        logger.info("Transcribing with Whisper...")
        result = model.transcribe(audio_path, language=SPEECH_LANGUAGE)
        text = result.get("text", "").strip()
        return text if text else None
    except Exception as e:
        logger.error(f"Whisper recognition error: {str(e)}")
        return None

def recognize_with_openai_api(audio_path):
    """Recognize speech using OpenAI API"""
    if not (OPENAI_AVAILABLE and USE_OPENAI_API and OPENAI_API_KEY):
        return None
    
    try:
        logger.info("Transcribing with OpenAI API...")
        with open(audio_path, 'rb') as audio_file:
            # OpenAI API v1.0+ syntax
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=SPEECH_LANGUAGE
            )
            text = transcript.text.strip() if hasattr(transcript, 'text') else str(transcript).strip()
            return text if text else None
    except Exception as e:
        logger.error(f"OpenAI API recognition error: {str(e)}")
        return None

def recognize_with_google(audio_data):
    """Recognize speech using Google Speech Recognition"""
    try:
        recognizer = sr.Recognizer()
        logger.info("Transcribing with Google Speech API...")
        text = recognizer.recognize_google(audio_data, language=SPEECH_LANGUAGE_GOOGLE)
        return text.strip() if text else None
    except sr.UnknownValueError:
        logger.warning("Google Speech API could not understand the audio")
        return None
    except sr.RequestError as e:
        logger.error(f"Google Speech API error: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Google recognition error: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-audio', methods=['POST'])
def process_audio():
    tmp_file_path = None
    wav_path = None
    
    try:
        # Validate request
        if not request.json:
            return jsonify({'error': 'Invalid request format'}), 400
        
        audio_data = request.json.get('audio')
        if not audio_data:
            return jsonify({'error': 'No audio data received'}), 400
        
        # Decode base64 audio data
        try:
            if ',' in audio_data:
                audio_bytes = base64.b64decode(audio_data.split(',')[1])
            else:
                audio_bytes = base64.b64decode(audio_data)
        except Exception as e:
            logger.error(f"Base64 decoding error: {str(e)}")
            return jsonify({'error': 'Invalid audio data format'}), 400
        
        # Validate audio file size
        audio_size_mb = len(audio_bytes) / (1024 * 1024)
        if audio_size_mb > MAX_AUDIO_SIZE_MB:
            return jsonify({
                'error': f'Audio file too large. Maximum size is {MAX_AUDIO_SIZE_MB}MB'
            }), 400
        
        logger.info(f"Processing audio file: {audio_size_mb:.2f}MB")
        
        # Create a temporary file to save audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_file_path = tmp_file.name
        
        try:
            # Convert audio to WAV format
            try:
                audio = AudioSegment.from_file(tmp_file_path)
            except Exception as e:
                logger.error(f"Audio file loading error: {str(e)}")
                return jsonify({
                    'error': 'Unsupported audio format. Please use a supported format.'
                }), 400
            
            # Validate audio duration
            duration_seconds = len(audio) / 1000.0
            if duration_seconds > MAX_AUDIO_DURATION_SECONDS:
                return jsonify({
                    'error': f'Audio too long. Maximum duration is {MAX_AUDIO_DURATION_SECONDS} seconds'
                }), 400
            
            if duration_seconds < 0.5:
                return jsonify({
                    'error': 'Audio too short. Please record at least 0.5 seconds.'
                }), 400
            
            logger.info(f"Audio duration: {duration_seconds:.2f} seconds")
            
            # Improve audio quality: normalize and convert to mono for better recognition
            audio = normalize(audio)
            if audio.channels > 1:
                audio = audio.set_channels(1)  # Convert to mono
            
            # Set sample rate to 16kHz (good for speech recognition)
            audio = audio.set_frame_rate(16000)
            
            # Convert to WAV format for speech recognition
            wav_path = tmp_file_path.replace('.webm', '.wav')
            audio.export(wav_path, format='wav', parameters=["-ar", "16000"])
            
            # Recognize speech in Urdu using selected engine
            urdu_text = None
            engine_used = 'unknown'
            
            logger.info(f"Starting speech recognition with engine: {SPEECH_ENGINE}")
            
            if SPEECH_ENGINE == 'whisper' or (SPEECH_ENGINE == 'auto' and WHISPER_AVAILABLE):
                # Try Whisper first (best accuracy for Urdu)
                if USE_OPENAI_API and OPENAI_AVAILABLE:
                    urdu_text = recognize_with_openai_api(wav_path)
                    engine_used = 'openai_api'
                else:
                    urdu_text = recognize_with_whisper(wav_path)
                    engine_used = 'whisper_local'
                
                # Fallback to Google if Whisper fails and auto mode
                if not urdu_text and SPEECH_ENGINE == 'auto':
                    logger.info("Whisper failed, falling back to Google Speech API...")
                    try:
                        recognizer = sr.Recognizer()
                        with sr.AudioFile(wav_path) as source:
                            recognizer.adjust_for_ambient_noise(source, duration=0.5)
                            audio_data = recognizer.record(source)
                        urdu_text = recognize_with_google(audio_data)
                        engine_used = 'google'
                    except Exception as e:
                        logger.error(f"Google fallback error: {str(e)}")
            
            elif SPEECH_ENGINE == 'google' or (SPEECH_ENGINE == 'auto' and not WHISPER_AVAILABLE):
                # Use Google Speech Recognition
                try:
                    recognizer = sr.Recognizer()
                    with sr.AudioFile(wav_path) as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        audio_data = recognizer.record(source)
                    urdu_text = recognize_with_google(audio_data)
                    engine_used = 'google'
                except Exception as e:
                    logger.error(f"Google recognition error: {str(e)}")
            
            if not urdu_text or len(urdu_text.strip()) == 0:
                return jsonify({
                    'error': 'No speech detected in the audio. Please try again with clearer audio.'
                }), 400
            
            logger.info(f"Recognized Urdu text ({engine_used}): {urdu_text[:50]}...")
            
            # Translate Urdu to English
            try:
                translator = GoogleTranslator(source=TRANSLATION_SOURCE, target=TRANSLATION_TARGET)
                english_text = translator.translate(urdu_text)
                logger.info(f"Translation completed")
                
                return jsonify({
                    'success': True,
                    'urdu_text': urdu_text,
                    'english_text': english_text,
                    'duration': round(duration_seconds, 2),
                    'engine_used': engine_used
                })
            except Exception as e:
                logger.error(f"Translation error: {str(e)}")
                return jsonify({
                    'error': 'Translation service unavailable. Please try again later.'
                }), 500
        
        finally:
            # Clean up temporary files
            for file_path in [tmp_file_path, wav_path]:
                if file_path and os.path.exists(file_path):
                    try:
                        os.unlink(file_path)
                    except Exception as e:
                        logger.warning(f"Failed to delete temp file {file_path}: {str(e)}")
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'An unexpected error occurred. Please try again.'
        }), 500

if __name__ == '__main__':
    from config import DEBUG, PORT, HOST
    logger.info(f"Starting Flask app on {HOST}:{PORT} (debug={DEBUG})")
    app.run(debug=DEBUG, port=PORT, host=HOST)

