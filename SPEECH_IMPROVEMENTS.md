# Speech Recognition Improvements for Urdu

## Overview

The application now supports multiple speech recognition engines with improved accuracy for Urdu language.

## Available Engines

### 1. **OpenAI Whisper (Recommended)**
   - **Best accuracy** for Urdu and many other languages
   - Supports local models (no API key needed)
   - Can use OpenAI API for cloud-based processing
   - Models: tiny, base, small, medium, large, large-v2, large-v3

### 2. **Google Speech Recognition**
   - Free to use (public API)
   - Good accuracy for Urdu (ur-PK)
   - Requires internet connection
   - Rate limits may apply

### 3. **Auto Mode (Default)**
   - Tries Whisper first (if available)
   - Falls back to Google Speech API if Whisper fails
   - Best of both worlds

## Configuration

Edit `config.py` or set environment variables:

```python
# Choose recognition engine
SPEECH_ENGINE = 'auto'  # Options: 'whisper', 'google', 'auto'

# For local Whisper (default)
WHISPER_MODEL = 'base'  # Options: 'tiny', 'base', 'small', 'medium', 'large'

# For OpenAI API (optional)
USE_OPENAI_API = False  # Set to True to use OpenAI API
OPENAI_API_KEY = ''  # Your OpenAI API key
```

## Installation

### Basic Installation (Google Speech API only)
```bash
pip install -r requirements.txt
```

### With Whisper (Recommended)
```bash
pip install -r requirements.txt
# Whisper will be installed automatically
```

### First Run with Whisper
On first use, Whisper will download the model (base model ~150MB).
This happens automatically and only once.

## Model Comparison

| Model | Size | Speed | Accuracy | Memory |
|-------|------|-------|----------|--------|
| tiny  | ~75MB | Fastest | Good | Low |
| base  | ~150MB | Fast | Very Good | Low |
| small | ~500MB | Medium | Excellent | Medium |
| medium| ~1.5GB | Slow | Excellent | High |
| large | ~3GB | Slowest | Best | Very High |

**Recommendation**: Start with `base` model for best balance of speed and accuracy.

## Audio Processing Improvements

1. **Audio Normalization**: Automatically normalizes audio levels
2. **Mono Conversion**: Converts stereo to mono (better for speech)
3. **Sample Rate Optimization**: Sets optimal 16kHz sample rate
4. **Better Format Handling**: Improved audio format conversion

## Usage

The application automatically uses the best available engine based on your configuration:

1. **If Whisper is installed and SPEECH_ENGINE='auto' or 'whisper'**:
   - Uses Whisper (local or API)
   - Falls back to Google if Whisper fails (in auto mode)

2. **If SPEECH_ENGINE='google'**:
   - Uses Google Speech Recognition API directly

3. **Engine information is returned in the response**:
   ```json
   {
     "success": true,
     "urdu_text": "...",
     "english_text": "...",
     "engine_used": "whisper_local"
   }
   ```

## Performance Tips

1. **For fastest results**: Use `tiny` or `base` Whisper model
2. **For best accuracy**: Use `small` or `medium` Whisper model
3. **For offline use**: Use local Whisper (don't set OPENAI_API_KEY)
4. **For cloud processing**: Use OpenAI API (requires API key and internet)

## Troubleshooting

### Whisper not working
- Install: `pip install openai-whisper`
- Check disk space (models need space)
- Try smaller model if out of memory

### OpenAI API not working
- Install: `pip install openai`
- Set `OPENAI_API_KEY` environment variable
- Set `USE_OPENAI_API=True`

### Google Speech API errors
- Check internet connection
- Verify microphone permissions
- Try speaking more clearly

## Accuracy Improvements

Whisper typically provides:
- **20-30% better accuracy** for Urdu compared to Google Speech API
- Better handling of accents and dialects
- Better punctuation and formatting
- Better handling of mixed languages

## Next Steps

To further improve Urdu recognition:
1. Use larger Whisper models (small, medium, large)
2. Fine-tune Whisper on Urdu-specific data
3. Use specialized Urdu speech models
4. Improve audio quality (better microphone, quieter environment)

