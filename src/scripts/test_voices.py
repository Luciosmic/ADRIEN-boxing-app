"""
Test different Kokoro voices.
Available voices:
- ff_siwis: French Female
- af_heart, af_bella, af_sarah, af_nicole, af_sky: American English Female
- bf_emma, bf_isabella: British English Female
"""
import asyncio
from src.infrastructure.audio.kokoro_audio_service import KokoroAudioService

VOICES = {
    "ff_siwis": ("fr", "Bonjour! Bienvenue à votre entraînement de boxe!"),
    "af_heart": ("en", "Hello! Welcome to your boxing training!"),
    "af_bella": ("en", "Hi! Let's start your workout!"),
    "bf_emma": ("en", "Good day! Ready for training?"),
}

async def test_voice(voice_id: str, language: str, text: str):
    print(f"\n🎤 Testing voice: {voice_id} ({language})")
    print(f"   Text: {text}")
    
    service = KokoroAudioService(voice=voice_id)
    await service.speak(text, language=language)
    
    print(f"   ✓ Done")

async def main():
    print("=" * 60)
    print("Kokoro Voice Tester")
    print("=" * 60)
    
    for voice_id, (lang, text) in VOICES.items():
        await test_voice(voice_id, lang, text)
        await asyncio.sleep(0.5)
    
    print("\n" + "=" * 60)
    print("✅ All voices tested!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
