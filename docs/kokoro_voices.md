# Kokoro TTS Voice Configuration

## Available Voices

Kokoro-82M supports multiple voices across different languages:

### French 🇫🇷

- **ff_siwis** - French Female (Default)

### American English 🇺🇸

- **af_heart** - American Female (Heart)
- **af_bella** - American Female (Bella)
- **af_sarah** - American Female (Sarah)
- **af_nicole** - American Female (Nicole)
- **af_sky** - American Female (Sky)

### British English 🇬🇧

- **bf_emma** - British Female (Emma)
- **bf_isabella** - British Female (Isabella)

## Current Configuration

The application is configured to use **ff_siwis** (French Female) by default.

Location: `src/infrastructure/audio/kokoro_audio_service.py`

```python
voice: str = "ff_siwis"  # French female voice
```

## Changing Voice

To change the voice, update `src/composition_root.py`:

```python
audio_provider = KokoroAudioService(
    repo_id="prince-canuma/Kokoro-82M",
    voice="ff_siwis"  # Change this to any voice above
)
```

## Testing Voices

Run the voice tester:

```bash
PYTHONPATH=. python3 src/scripts/test_voices.py
```

## Notes

- The warning "Language mismatch, loading ff_siwis voice into American English pipeline" is normal and can be ignored
- All voices work correctly despite the warning
- The model auto-detects language based on the voice selected
