"""
Announcement Listener - Application layer event handler.
Listens to AnnouncementTriggered events and delegates to audio service.
"""
import logging
from src.domain.training.events import AnnouncementTriggered
from src.application.audio_service.audio_service import AudioService
from src.application.audio_service.dtos import SpeakRequest

logger = logging.getLogger(__name__)


class AnnouncementListener:
    """
    Event handler for announcement events.
    Translates domain events into audio service calls.
    """
    
    def __init__(self, audio_service: AudioService):
        """
        Initialize the listener.
        
        Args:
            audio_service: AudioService instance to handle speech
        """
        self.audio_service = audio_service
    
    async def handle(self, event: AnnouncementTriggered):
        """
        Handle an announcement event by speaking the text.
        
        Args:
            event: AnnouncementTriggered domain event
        """
        request = SpeakRequest(text=event.text, language="en")
        response = await self.audio_service.speak(request)
        
        if not response.success:
            logger.warning(f"Failed to announce: {event.text} - {response.message}")
