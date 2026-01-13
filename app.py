from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from deep_translator import GoogleTranslator
import io
import base64
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range, high_pass_filter
import tempfile
import os
import sys
import logging
from config import (
    MAX_AUDIO_SIZE_MB, MAX_AUDIO_DURATION_SECONDS,
    SPEECH_LANGUAGE, SPEECH_LANGUAGE_GOOGLE, TRANSLATION_SOURCE, TRANSLATION_TARGET,
    LOG_LEVEL, SPEECH_ENGINE, WHISPER_MODEL, OPENAI_API_KEY, USE_OPENAI_API,
    ENABLE_MEDICAL_PARSING, USE_MEDICAL_NLP,
    WHISPER_TEMPERATURE, WHISPER_BEAM_SIZE, WHISPER_BEST_OF, WHISPER_PATIENCE,
    WHISPER_CONDITION_ON_PREVIOUS_TEXT
)

# Configure logging first
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to import language detection
try:
    from langdetect import detect, LangDetectException
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False
    logger.warning("langdetect not available. Install with: pip install langdetect")

# Import language detection utility
try:
    from utils import detect_language
except ImportError:
    detect_language = None
    logger.warning("Language detection utility not available")

# Import medical parser
try:
    from medical_parser import parse_prescription, format_prescription_text
    MEDICAL_PARSER_AVAILABLE = True
except ImportError:
    MEDICAL_PARSER_AVAILABLE = False
    logger.warning("Medical parser not available")

# Try to import medical NLP models (optional)
try:
    import torch
    from transformers import AutoTokenizer, AutoModelForTokenClassification
    MEDICAL_NLP_AVAILABLE = True
except ImportError:
    MEDICAL_NLP_AVAILABLE = False
    if USE_MEDICAL_NLP:
        logger.warning("Medical NLP libraries not available. Install with: pip install torch transformers")

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
    """Recognize speech using OpenAI Whisper (local) with advanced parameters for better accuracy"""
    if not WHISPER_AVAILABLE:
        return None
    
    try:
        model = get_whisper_model()
        if model is None or model is False:
            return None
        
        logger.info(f"Transcribing with Whisper (model: {WHISPER_MODEL}, beam_size: {WHISPER_BEAM_SIZE})...")
        
        # Use advanced transcription parameters for improved accuracy
        transcribe_options = {
            'language': SPEECH_LANGUAGE,
            'temperature': WHISPER_TEMPERATURE,  # 0.0 = deterministic, best for accuracy
            'beam_size': WHISPER_BEAM_SIZE,  # Higher = better accuracy but slower
            'best_of': WHISPER_BEST_OF,  # Number of candidates
            'patience': WHISPER_PATIENCE,  # Beam search patience
            'condition_on_previous_text': WHISPER_CONDITION_ON_PREVIOUS_TEXT,  # Use context
            'verbose': False
        }
        
        result = model.transcribe(audio_path, **transcribe_options)
        text = result.get("text", "").strip()
        
        # Log transcription quality metrics if available
        if 'segments' in result and result['segments']:
            avg_no_speech_prob = sum(seg.get('no_speech_prob', 0) for seg in result['segments']) / len(result['segments'])
            logger.info(f"Whisper transcription completed (avg no_speech_prob: {avg_no_speech_prob:.3f}, segments: {len(result['segments'])})")
        
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

def recognize_with_google(audio_data, language=None):
    """Recognize speech using Google Speech Recognition"""
    try:
        recognizer = sr.Recognizer()
        lang = language or SPEECH_LANGUAGE_GOOGLE
        logger.info(f"Transcribing with Google Speech API (language: {lang})...")
        text = recognizer.recognize_google(audio_data, language=lang)
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

@app.route('/format-prescription', methods=['POST'])
def format_prescription():
    """Format English text as medical prescription (optional feature)"""
    try:
        if not request.json:
            return jsonify({'error': 'Invalid request format'}), 400
        
        english_text = request.json.get('text')
        if not english_text:
            return jsonify({'error': 'No text provided'}), 400
        
        if not MEDICAL_PARSER_AVAILABLE:
            return jsonify({
                'error': 'Medical parser not available'
            }), 503
        
        try:
            logger.info("Formatting text as medical prescription...")
            prescription_data = parse_prescription(english_text)
            prescription_text = format_prescription_text(prescription_data)
            logger.info(f"Prescription formatted: {len(prescription_data['medicines'])} medicines, {len(prescription_data['tests'])} tests")
            
            return jsonify({
                'success': True,
                'prescription_text': prescription_text
            })
        except Exception as e:
            logger.error(f"Medical parsing error: {str(e)}")
            return jsonify({
                'error': f'Failed to format prescription: {str(e)}'
            }), 500
            
    except Exception as e:
        logger.error(f"Unexpected error in format_prescription: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'An unexpected error occurred. Please try again.'
        }), 500

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
            
            # Recognize speech - try English first, then Urdu
            recognized_text = None
            detected_language = None
            engine_used = 'unknown'
            original_text = None
            
            logger.info(f"Starting speech recognition with engine: {SPEECH_ENGINE}")
            
            # Try English recognition first
            try:
                recognizer = sr.Recognizer()
                with sr.AudioFile(wav_path) as source:
                    # Reduced ambient noise adjustment time for soft speech (0.3s instead of 0.5s)
                    # This prevents cutting off the beginning of soft speech
                    recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    # Increase energy threshold slightly for better soft speech detection
                    recognizer.energy_threshold = 300  # Lower threshold for soft speech
                    audio_data = recognizer.record(source)
                
                # Try English first (but don't trust it if it looks like Romanized Urdu)
                try:
                    recognized_text_en = recognize_with_google(audio_data, language='en-US')
                    if recognized_text_en:
                        # Check if it looks like Romanized Urdu (common Urdu words in English letters)
                        # If it does, prefer Urdu recognition instead
                        romanized_urdu_indicators = ['achcha', 'yah', 'kya', 'hai', 'nahin', 'ka', 'ki', 'se', 'ko', 'mein']
                        text_lower = recognized_text_en.lower()
                        if any(indicator in text_lower for indicator in romanized_urdu_indicators):
                            logger.info("Text looks like Romanized Urdu, will try Urdu recognition instead")
                            recognized_text_en = None  # Don't use English recognition result
                        else:
                            recognized_text = recognized_text_en
                            detected_language = 'en'
                            engine_used = 'google_en'
                            logger.info(f"Detected English speech: {recognized_text[:50]}...")
                except:
                    pass
                
                # If not English, try Urdu
                if not recognized_text:
                    if SPEECH_ENGINE == 'whisper' or (SPEECH_ENGINE == 'auto' and WHISPER_AVAILABLE):
                        # Try Whisper for Urdu
                        if USE_OPENAI_API and OPENAI_AVAILABLE:
                            recognized_text = recognize_with_openai_api(wav_path)
                            engine_used = 'openai_api'
                        else:
                            recognized_text = recognize_with_whisper(wav_path)
                            engine_used = 'whisper_local'
                        
                        # Fallback to Google if Whisper fails
                        if not recognized_text and SPEECH_ENGINE == 'auto':
                            recognized_text = recognize_with_google(audio_data, language=SPEECH_LANGUAGE_GOOGLE)
                            engine_used = 'google_ur'
                    else:
                        recognized_text = recognize_with_google(audio_data, language=SPEECH_LANGUAGE_GOOGLE)
                        engine_used = 'google_ur'
                    
                    if recognized_text:
                        detected_language = 'ur'
                        logger.info(f"Detected Urdu speech: {recognized_text[:50]}...")
            except Exception as e:
                logger.error(f"Recognition error: {str(e)}")
            
            if not recognized_text or len(recognized_text.strip()) == 0:
                return jsonify({
                    'error': 'No speech detected in the audio. Please try again with clearer audio.'
                }), 400
            
            original_text = recognized_text
            logger.info(f"Recognized text ({engine_used}): {original_text[:100]}... (Length: {len(original_text)} chars)")
            
            # Language detection (double-check)
            if detect_language and LANGDETECT_AVAILABLE:
                detected_lang = detect_language(original_text)
                if detected_lang == 'en' and detected_language != 'en':
                    detected_language = 'en'
                    logger.info("Language detection confirmed: English")
                elif detected_lang == 'ur' and detected_language != 'ur':
                    detected_language = 'ur'
                    logger.info("Language detection confirmed: Urdu")
            
            # Check if text looks like Romanized Urdu (even if detected as English)
            romanized_urdu_indicators = ['achcha', 'yah', 'kya', 'hai', 'nahin', 'ka', 'ki', 'se', 'ko', 'mein', 'karega', 'urdu', 'hoga', 'hoga', 'hain', 'ho', 'tha', 'thi', 'the']
            text_lower = original_text.lower()
            looks_like_romanized_urdu = any(indicator in text_lower for indicator in romanized_urdu_indicators)
            
            # Translate if Urdu was detected OR if Urdu engine was used OR if text looks like Romanized Urdu
            # Whisper often returns Romanized Urdu (English letters), which language detection might mistake as English
            english_text = None
            should_translate = (detected_language == 'ur' or 
                              engine_used in ['whisper_local', 'openai_api', 'google_ur'] or
                              looks_like_romanized_urdu)
            
            if should_translate:
                # Translate Urdu to English (even if text is Romanized)
                try:
                    logger.info(f"Translating to English (detected_language: {detected_language}, engine: {engine_used})...")
                    translator = GoogleTranslator(source=TRANSLATION_SOURCE, target=TRANSLATION_TARGET)
                    english_text = translator.translate(original_text)
                    logger.info(f"Translation completed. Original length: {len(original_text)}, Translated length: {len(english_text)}")
                    if len(english_text) < len(original_text) * 0.5:
                        logger.warning(f"Translation may be shortened: Original {len(original_text)} chars -> Translated {len(english_text)} chars")
                except Exception as e:
                    logger.error(f"Translation error: {str(e)}")
                    return jsonify({
                        'error': 'Translation service unavailable. Please try again later.'
                    }), 500
            else:
                # Already in English, no translation needed
                english_text = original_text
                logger.info("Text is already in English, skipping translation")
            
            # Prepare response (prescription parsing is now optional via separate endpoint)
            response_data = {
                'success': True,
                'original_text': original_text,
                'detected_language': detected_language or 'unknown',
                'english_text': english_text,
                'duration': round(duration_seconds, 2),
                'engine_used': engine_used
            }
            
            return jsonify(response_data)
        
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

