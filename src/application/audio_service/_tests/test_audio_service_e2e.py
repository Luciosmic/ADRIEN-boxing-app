"""E2E tests for AudioService API."""
import pytest
from src.application.audio_service.audio_service import AudioService
from src.application.audio_service.dtos import (
    SpeakRequest,
    ConfigureAudioRequest,
    SpeakResponse,
    AudioStatusResponse
)
from src.infrastructure.audio.console_audio_service import ConsoleAudioService


@pytest.mark.anyio
class TestAudioServiceE2E:
    """End-to-end tests for AudioService using the API interface."""
    
    async def test_speak_with_console_provider(self):
        """Test speaking text using console audio provider."""
        # Arrange
        provider = ConsoleAudioService()
        service = AudioService(audio_provider=provider)
        request = SpeakRequest(text="Hello from E2E test", language="en")
        
        # Act
        response = await service.speak(request)
        
        # Assert
        assert isinstance(response, SpeakResponse)
        assert response.success is True
        assert response.message is None
    
    async def test_speak_multiple_languages(self):
        """Test speaking in different languages."""
        provider = ConsoleAudioService()
        service = AudioService(audio_provider=provider)
        
        # Test French
        fr_request = SpeakRequest(text="Bonjour", language="fr")
        fr_response = await service.speak(fr_request)
        assert fr_response.success is True
        
        # Test English
        en_request = SpeakRequest(text="Hello", language="en")
        en_response = await service.speak(en_request)
        assert en_response.success is True
        
        # Test Spanish
        es_request = SpeakRequest(text="Hola", language="es")
        es_response = await service.speak(es_request)
        assert es_response.success is True
    
    async def test_speak_without_provider(self):
        """Test speaking when no audio provider is configured."""
        # Arrange
        service = AudioService(audio_provider=None)
        request = SpeakRequest(text="This should not play", language="en")
        
        # Act
        response = await service.speak(request)
        
        # Assert
        assert isinstance(response, SpeakResponse)
        assert response.success is False
        assert response.message == "Audio is disabled"
    
    async def test_get_status_with_provider(self):
        """Test getting audio service status."""
        # Arrange
        provider = ConsoleAudioService()
        service = AudioService(audio_provider=provider)
        
        # Act
        status = await service.get_status()
        
        # Assert
        assert isinstance(status, AudioStatusResponse)
        assert status.enabled is True
        assert status.provider == "ConsoleAudioService"
    
    async def test_get_status_without_provider(self):
        """Test getting status when audio is disabled."""
        # Arrange
        service = AudioService(audio_provider=None)
        
        # Act
        status = await service.get_status()
        
        # Assert
        assert isinstance(status, AudioStatusResponse)
        assert status.enabled is False
        assert status.provider == "none"
    
    async def test_configure_audio(self):
        """Test configuring audio settings."""
        # Arrange
        provider = ConsoleAudioService()
        service = AudioService(audio_provider=provider)
        
        # Act - Disable audio
        config_request = ConfigureAudioRequest(enabled=False)
        status = await service.configure(config_request)
        
        # Assert
        assert isinstance(status, AudioStatusResponse)
        assert status.enabled is False
        
        # Verify speaking is disabled
        speak_request = SpeakRequest(text="Should not play", language="en")
        speak_response = await service.speak(speak_request)
        assert speak_response.success is False
    
    async def test_empty_text_handling(self):
        """Test handling of empty text."""
        # Arrange
        provider = ConsoleAudioService()
        service = AudioService(audio_provider=provider)
        request = SpeakRequest(text="", language="en")
        
        # Act
        response = await service.speak(request)
        
        # Assert
        # Empty text should still succeed (provider handles it)
        assert isinstance(response, SpeakResponse)
    
    async def test_long_text_handling(self):
        """Test handling of long text."""
        # Arrange
        provider = ConsoleAudioService()
        service = AudioService(audio_provider=provider)
        long_text = "This is a very long text. " * 50
        request = SpeakRequest(text=long_text, language="en")
        
        # Act
        response = await service.speak(request)
        
        # Assert
        assert isinstance(response, SpeakResponse)
        assert response.success is True
