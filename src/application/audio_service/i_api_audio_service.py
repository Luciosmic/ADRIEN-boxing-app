"""
Audio Service API Interface.
Defines the contract for audio-related operations.
"""
from abc import ABC, abstractmethod
from src.application.audio_service.dtos import (
    SpeakRequest, SpeakResponse,
    ConfigureAudioRequest, AudioStatusResponse
)


class IApiAudioService(ABC):
    """
    High-level API for audio operations.
    This service orchestrates audio functionality for the application.
    """
    
    @abstractmethod
    async def speak(self, request: SpeakRequest) -> SpeakResponse:
        """
        Speak the given text using the configured audio provider.
        
        Args:
            request: SpeakRequest with text and language
            
        Returns:
            SpeakResponse indicating success/failure
        """
        pass
    
    @abstractmethod
    async def configure(self, request: ConfigureAudioRequest) -> AudioStatusResponse:
        """
        Configure audio settings (voice, speed, enabled/disabled).
        
        Args:
            request: ConfigureAudioRequest with settings
            
        Returns:
            AudioStatusResponse with current status
        """
        pass
    
    @abstractmethod
    async def get_status(self) -> AudioStatusResponse:
        """
        Get current audio service status.
        
        Returns:
            AudioStatusResponse with current configuration
        """
        pass
