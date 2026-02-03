import sys
try:
    import mlx_audio
    print("mlx_audio imported successfully")
    print("mlx_audio dir:", dir(mlx_audio))
    
    # Check for TTS or Kokoro
    if hasattr(mlx_audio, 'tts'):
        print("mlx_audio.tts dir:", dir(mlx_audio.tts))
        import mlx_audio.tts
        print("mlx_audio.tts package dir:", dir(mlx_audio.tts))
    else:
        print("No 'tts' attribute in mlx_audio")

    # Try importing common submodules directly
    try:
        from mlx_audio.tts import tts
        print("Found mlx_audio.tts.tts")
        print(dir(tts))
    except ImportError as e:
        print(f"ImportError mlx_audio.tts.tts: {e}")

except ImportError as e:
    print(f"Could not import mlx_audio: {e}")
