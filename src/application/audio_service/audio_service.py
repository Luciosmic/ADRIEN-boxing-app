"""
Audio Service Implementation.
Orchestrates audio functionality using the IAudioService port.
"""
import logging
from src.application.audio_service.i_api_audio_service import IApiAudioService
from src.application.audio_service.dtos import (
    SpeakRequest, SpeakResponse,
    ConfigureAudioRequest, AudioStatusResponse
)
from src.application.ports.i_audio_service import IAudioService

logger = logging.getLogger(__name__)


class AudioService(IApiAudioService):
    """
    Application service for audio operations.
    Delegates to infrastructure implementations via IAudioService port.
    """
    
    def __init__(self, audio_provider: IAudioService | None = None):
        """
        Initialize the audio service.
        
        Args:
            audio_provider: Implementation of IAudioService (e.g., KokoroAudioService)
                           If None, audio is disabled.
        """
        self._provider = audio_provider
        self._enabled = audio_provider is not None
        self._provider_name = (
            type(audio_provider).__name__ if audio_provider else "none"
        )
    
    async def speak(self, request: SpeakRequest) -> SpeakResponse:
        """Speak text using the configured provider."""
        if not self._enabled or not self._provider:
            logger.debug(f"Audio disabled, skipping: {request.text}")
            return SpeakResponse(
                success=False,
                message="Audio is disabled"
            )
        
        try:
            await self._provider.speak(request.text, request.language)
            return SpeakResponse(success=True)
        except Exception as e:
            logger.error(f"Failed to speak: {e}")
            return SpeakResponse(
                success=False,
                message=str(e)
            )
    
    async def configure(self, request: ConfigureAudioRequest) -> AudioStatusResponse:
        """Configure audio settings."""
        self._enabled = request.enabled
        # Note: Voice/speed configuration would require extending IAudioService
        # For now, we just track enabled state
        return await self.get_status()
    
    async def get_status(self) -> AudioStatusResponse:
        """Get current audio status."""
        voice = None
        if hasattr(self._provider, 'voice'):
            voice = self._provider.voice
            
        return AudioStatusResponse(
            enabled=self._enabled,
            provider=self._provider_name,
            voice=voice
        )
