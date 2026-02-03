"""
Coaching Listener - Application layer event handler.
Listens to SessionTicked events and generates coaching instructions.
"""
import logging
from typing import Dict, Optional
from src.domain.training.events import SessionTicked
from src.application.coaching_service.i_api_coaching_service import IApiCoachingService
from src.application.audio_service.audio_service import AudioService
from src.application.coaching_service.dtos import GetInstructionRequest
from src.application.audio_service.dtos import SpeakRequest

logger = logging.getLogger(__name__)


class CoachingListener:
    """
    Event handler for session tick events.
    Generates coaching instructions and speaks them via audio service.
    """
    
    def __init__(
        self, 
        coaching_service: IApiCoachingService,
        audio_service: AudioService,
        language: str = "fr"
    ):
        """
        Initialize the listener.
        
        Args:
            coaching_service: CoachingService instance to generate instructions
            audio_service: AudioService instance to handle speech
            language: Default language for instructions
        """
        self.coaching_service = coaching_service
        self.audio_service = audio_service
        self.language = language
        
        # Track last spoken instruction per session to avoid repetition
        self._last_instructions: Dict[str, str] = {}
        
        # Track workout details per session (needed for techniques/exercises)
        self._session_contexts: Dict[str, dict] = {}
    
    def set_session_context(self, session_id: str, workout_detail):
        """
        Set workout context for a session.
        This should be called when a session starts.
        
        Args:
            session_id: Session identifier
            workout_detail: WorkoutDetailResponse with blocks info
        """
        self._session_contexts[session_id] = {
            'workout_detail': workout_detail
        }
    
    async def handle(self, event: SessionTicked):
        """
        Handle a session tick event by generating and speaking instruction.
        
        Args:
            event: SessionTicked domain event
        """
        # Get workout context
        context = self._session_contexts.get(event.session_id)
        if not context:
            logger.warning(f"No context for session {event.session_id}")
            return
        
        workout_detail = context['workout_detail']
        
        # Get current block
        if event.current_block_index >= len(workout_detail.blocks):
            return
        
        block = workout_detail.blocks[event.current_block_index]
        
        # Build request for coaching service
        request = GetInstructionRequest(
            session_id=event.session_id,
            block_type=event.block_type,
            time_left=event.time_left,
            is_work_phase=event.is_work_phase,
            language=self.language,
            techniques=getattr(block, 'techniques', None),
            exercises=getattr(block, 'exercises', None)
        )
        
        # Get instruction
        response = await self.coaching_service.get_instruction(request)
        
        # Speak if instruction changed
        if response.text and response.text != self._last_instructions.get(event.session_id, ""):
            await self._speak_instruction(response.text)
            self._last_instructions[event.session_id] = response.text
    
    async def _speak_instruction(self, text: str):
        """Speak instruction via AudioService."""
        try:
            request = SpeakRequest(text=text, language=self.language)
            response = await self.audio_service.speak(request)
            
            if not response.success:
                logger.warning(f"Failed to speak: {text} - {response.message}")
        except Exception as e:
            # Don't crash if audio fails
            logger.error(f"Audio error: {e}")
    
    def cleanup_session(self, session_id: str):
        """Clean up session context when session ends."""
        self._last_instructions.pop(session_id, None)
        self._session_contexts.pop(session_id, None)
