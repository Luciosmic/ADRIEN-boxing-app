"""
Audio verification script.
Tests the audio service with Kokoro TTS.
"""
import asyncio
import os
import logging
from src.infrastructure.audio.kokoro_audio_service import KokoroAudioService
from src.application.audio_service.audio_service import AudioService
from src.application.audio_service.dtos import SpeakRequest

# Configure logging
logging.basicConfig(level=logging.INFO)

async def main():
    print("Testing Kokoro Audio Service...")
    
    # Set environment for phonemizer
    os.environ["PHONEMIZER_ESPEAK_LIBRARY"] = "/opt/homebrew/lib/libespeak-ng.dylib"
    
    # Initialize Kokoro audio provider
    try:
        provider = KokoroAudioService()
        # Trigger model load
        _ = provider.model 
        print("Kokoro provider initialized.")
    except Exception as e:
        print(f"Failed to initialize Kokoro: {e}")
        import traceback
        traceback.print_exc()
        return

    # Create audio service
    audio_service = AudioService(audio_provider=provider)
    
    import sys
    text = sys.argv[1] if len(sys.argv) > 1 else "Architecture refactoring successful!"
    print(f"Speaking: '{text}'")
    
    # Use the service API
    request = SpeakRequest(text=text, language="en")
    response = await audio_service.speak(request)
    
    if response.success:
        print("✓ Audio played successfully")
    else:
        print(f"✗ Failed: {response.message}")
    
    print("Done. Did you hear it?")

if __name__ == "__main__":
    asyncio.run(main())
