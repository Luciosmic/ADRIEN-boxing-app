"""
Composition Root - Dependency Injection Container.
Wires up all dependencies for the application.
"""
import os
import sys
from src.application.training_service.training_service import TrainingService
from src.interface.presenters.training_presenter import TrainingPresenter


class CompositionRoot:
    """
    Factory for creating fully-wired application components.
    Handles all infrastructure setup and dependency injection.
    """
    
    @staticmethod
    def create_presenter(language='fr', base_path='.osu', use_audio=True):
        """
        Create a fully configured TrainingPresenter with all dependencies.
        
        Args:
            language: Initial language for the presenter
            base_path: Path for file-based persistence
            use_audio: Whether to enable audio announcements
            
        Returns:
            TrainingPresenter: Fully configured presenter
        """
        # Setup event bus and listeners if audio is enabled
        event_bus = None
        coaching_listener = None
        
        if use_audio:
            event_bus, audio_service, coaching_listener = CompositionRoot._setup_audio_infrastructure_with_service()
            # Set language on coaching listener
            if coaching_listener:
                coaching_listener.language = language
        
        # Create training service with optional event bus
        training_service = TrainingService(base_path=base_path, event_bus=event_bus)
        
        # Create coaching service (for presenter to get instructions for UI display)
        from src.application.coaching_service.coaching_service import CoachingService
        coaching_service = CoachingService()
        
        # Create and return presenter with services and listener
        presenter = TrainingPresenter(
            training_service=training_service,
            coaching_service=coaching_service,
            coaching_listener=coaching_listener,  # Pass listener for context management
            language=language
        )
        return presenter
    
    
    @staticmethod
    def _setup_audio_infrastructure():
        """
        Setup audio infrastructure.
        Returns configured event bus with audio listener attached.
        """
        event_bus, _, _ = CompositionRoot._setup_audio_infrastructure_with_service()
        return event_bus
    
    @staticmethod
    def _setup_audio_infrastructure_with_service():
        """
        Setup audio infrastructure.
        Returns tuple of (event_bus, audio_service, coaching_listener).
        """
        from src.infrastructure.events.bus.in_memory_event_bus import InMemoryEventBus
        from src.application.listeners.announcement_listener import AnnouncementListener
        from src.application.listeners.coaching_listener import CoachingListener
        from src.application.audio_service.audio_service import AudioService
        from src.application.coaching_service.coaching_service import CoachingService
        from src.domain.training.events import AnnouncementTriggered, SessionTicked
        
        # Environment setup for Mac (espeak-ng for phonemizer)
        if sys.platform == "darwin":
            os.environ["PHONEMIZER_ESPEAK_LIBRARY"] = "/opt/homebrew/lib/libespeak-ng.dylib"
        
        # Create event bus
        event_bus = InMemoryEventBus()
        
        # Try to create Kokoro audio provider, fallback to console
        audio_provider = None
        try:
            from src.infrastructure.audio.kokoro_audio_service import KokoroAudioService
            audio_provider = KokoroAudioService(
                repo_id="prince-canuma/Kokoro-82M", 
                voice="ff_siwis"  # French female voice
            )
            print("✓ Using Kokoro TTS (MLX) - French voice")
        except Exception as e:
            print(f"⚠ Failed to load Kokoro: {e}")
            try:
                from src.infrastructure.audio.console_audio_service import ConsoleAudioService
                audio_provider = ConsoleAudioService()
                print("✓ Using Console Audio (fallback)")
            except Exception as e2:
                print(f"✗ Failed to create any audio provider: {e2}")
                return None, None, None
        
        # Create audio service
        audio_service = AudioService(audio_provider=audio_provider)
        
        # Create coaching service
        coaching_service = CoachingService()
        
        # Wire up announcement listener for domain events (e.g., "Rest", "10 seconds")
        announcement_listener = AnnouncementListener(audio_service)
        event_bus.subscribe(AnnouncementTriggered, announcement_listener.handle)
        
        # Wire up coaching listener for session ticks (instructions)
        coaching_listener = CoachingListener(
            coaching_service=coaching_service,
            audio_service=audio_service,
            language="fr"  # Default, can be changed later
        )
        event_bus.subscribe(SessionTicked, coaching_listener.handle)
        
        return event_bus, audio_service, coaching_listener
