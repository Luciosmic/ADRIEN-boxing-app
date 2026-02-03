"""
Console Audio Service - Infrastructure implementation.
Prints text to console instead of speaking (fallback/testing).
"""
import logging
from src.application.ports.i_audio_service import IAudioService

logger = logging.getLogger(__name__)


class ConsoleAudioService(IAudioService):
    """
    Audio service implementation that prints to console.
    Useful for testing or when TTS is unavailable.
    """
    
    def __init__(self):
        """Initialize console audio service."""
        logger.info("Initialized Console Audio Service (fallback)")

    async def speak(self, text: str, language: str = "en") -> None:
        """
        Print text to console instead of speaking.
        
        Args:
            text: Text to "speak" (print)
            language: Language code (ignored for console output)
        """
        print(f"🔊 [{language.upper()}] {text}")
        logger.debug(f"Console speak: {text}")
