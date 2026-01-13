"""
Configuration settings for the Urdu Voice Translation App
"""
import os

# Flask configuration
DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
PORT = int(os.getenv('FLASK_PORT', '5001'))
HOST = os.getenv('FLASK_HOST', '127.0.0.1')

# Audio processing configuration
MAX_AUDIO_SIZE_MB = 10  # Maximum audio file size in MB
MAX_AUDIO_DURATION_SECONDS = 100  # Maximum recording duration
SUPPORTED_AUDIO_FORMATS = ['.webm', '.wav', '.mp3', '.ogg', '.m4a']

# Speech recognition configuration
SPEECH_LANGUAGE = 'ur'  # Urdu
SPEECH_LANGUAGE_GOOGLE = 'ur-PK'  # Urdu (Pakistan) for Google Speech API
TRANSLATION_SOURCE = 'ur'  # Urdu
TRANSLATION_TARGET = 'en'  # English

# Speech recognition engine selection
# Options: 'whisper' (recommended), 'google', 'auto' (try whisper first, fallback to google)
SPEECH_ENGINE = os.getenv('SPEECH_ENGINE', 'auto')

# Whisper model configuration (for local Whisper)
# Options: 'tiny', 'base', 'small', 'medium', 'large', 'large-v2', 'large-v3'
# Larger models = better accuracy but slower and more memory
# Recommended: 'small' for best balance (changed from 'base' for better accuracy)
WHISPER_MODEL = os.getenv('WHISPER_MODEL', 'small')

# Advanced Whisper transcription parameters (for improved accuracy)
WHISPER_TEMPERATURE = float(os.getenv('WHISPER_TEMPERATURE', '0.0'))  # 0.0 = deterministic (best for accuracy)
WHISPER_BEAM_SIZE = int(os.getenv('WHISPER_BEAM_SIZE', '5'))  # Beam search width (higher = better accuracy but slower)
WHISPER_BEST_OF = int(os.getenv('WHISPER_BEST_OF', '5'))  # Number of candidates to generate
WHISPER_PATIENCE = float(os.getenv('WHISPER_PATIENCE', '1.0'))  # Beam search patience
WHISPER_CONDITION_ON_PREVIOUS_TEXT = os.getenv('WHISPER_CONDITION_ON_PREVIOUS_TEXT', 'True').lower() == 'true'

# OpenAI API configuration (if using OpenAI API instead of local Whisper)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')  # Set this if using OpenAI API
USE_OPENAI_API = os.getenv('USE_OPENAI_API', 'False').lower() == 'true'

# Logging configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Medical prescription configuration
ENABLE_MEDICAL_PARSING = os.getenv('ENABLE_MEDICAL_PARSING', 'True').lower() == 'true'
USE_MEDICAL_NLP = os.getenv('USE_MEDICAL_NLP', 'False').lower() == 'true'  # BioBERT/ClinicalBERT

