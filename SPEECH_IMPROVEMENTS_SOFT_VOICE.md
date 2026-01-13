# Speech Recognition Improvements for Soft Voice

## Changes Made

### 1. **Audio Amplification**
- Automatically detects if audio is too quiet (below -20 dBFS)
- Amplifies soft recordings by up to 20dB
- Helps with soft speech recognition

### 2. **High-Pass Filtering**
- Removes low-frequency noise (below 80Hz)
- Improves clarity for soft speech
- Reduces background rumble

### 3. **Dynamic Range Compression**
- Evens out volume levels
- Helps soft parts of speech be more audible
- Prevents distortion of loud parts

### 4. **Improved Noise Adjustment**
- Reduced ambient noise adjustment time (0.3s instead of 0.5s)
- Prevents cutting off the beginning of soft speech
- Lower energy threshold (300) for better soft speech detection

### 5. **Audio Level Logging**
- Logs original and processed audio levels
- Helps diagnose if speech is too quiet
- Useful for debugging

## Technical Details

### Audio Processing Pipeline:
1. Convert to mono (if stereo)
2. Apply high-pass filter (remove low-frequency noise)
3. Amplify if too quiet (< -20 dBFS)
4. Normalize (bring peak to 0dB)
5. Apply compression (even out levels)
6. Set sample rate to 16kHz
7. Export for recognition

### Energy Threshold:
- Lower threshold (300) = more sensitive to soft speech
- Default is usually 400-500
- Lower values detect quieter speech better

## Recommendations for Users

1. **Speak clearly** - Even with improvements, clear speech works best
2. **Get closer to microphone** - Reduces background noise
3. **Speak at normal volume** - Doesn't need to be loud, just clear
4. **Reduce background noise** - Quieter environment = better recognition
5. **Speak at consistent pace** - Not too fast or too slow

## Testing

Check the console logs for:
- `Original audio level: X dBFS` - Should be above -30 dBFS for good quality
- `Audio amplified by X dB` - If this appears, your voice was soft
- `Processed audio level: X dBFS` - Should be around -10 to -5 dBFS after processing

If recognition is still poor:
- Try speaking slightly louder
- Get closer to microphone
- Reduce background noise
- Check microphone permissions and settings

