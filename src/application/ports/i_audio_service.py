"""
Port for audio services.
The application layer defines this interface,
and the infrastructure layer provides concrete implementations.
"""
from abc import ABC, abstractmethod


class IAudioService(ABC):
    """
    Port for text-to-speech audio services.
    Implementations handle the technical details of audio synthesis and playback.
    """
    
    @abstractmethod
    async def speak(self, text: str, language: str = "en") -> None:
        """
        Synthesize and play the given text.
        
        Args:
            text: The text to speak
            language: Language code (e.g., 'en', 'fr', 'es')
        """
        pass
