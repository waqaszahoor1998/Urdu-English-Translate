"""
Utility functions for language detection and text processing
"""
import logging

logger = logging.getLogger(__name__)

def detect_language(text):
    """
    Detect the language of the input text
    Returns: 'en' for English, 'ur' for Urdu, or 'unknown'
    """
    if not text or len(text.strip()) < 3:
        return 'unknown'
    
    try:
        from langdetect import detect, LangDetectException
        detected_lang = detect(text)
        logger.info(f"Language detected: {detected_lang} for text: {text[:50]}...")
        return detected_lang
    except Exception as e:
        logger.warning(f"Language detection failed: {str(e)}")
        # Fallback: simple heuristic for English
        # English typically has more Latin characters
        latin_chars = sum(1 for c in text if ord(c) < 128)
        total_chars = len(text.replace(' ', ''))
        if total_chars > 0 and latin_chars / total_chars > 0.7:
            return 'en'
        return 'unknown'

def recognize_english_speech(audio_data):
    """Recognize speech in English"""
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    try:
        text = recognizer.recognize_google(audio_data, language='en-US')
        return text.strip() if text else None
    except Exception as e:
        logger.error(f"English recognition error: {str(e)}")
        return None

