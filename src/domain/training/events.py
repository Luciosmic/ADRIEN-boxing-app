from datetime import datetime
from typing import Optional
from src.domain._base.domain_event import DomainEvent
from src.domain.training.value_objects import BlockType

class SessionStarted(DomainEvent):
    session_id: str
    workout_id: str
    started_at: datetime

class SessionPaused(DomainEvent):
    session_id: str
    paused_at: datetime

class SessionResumed(DomainEvent):
    session_id: str
    resumed_at: datetime

class SessionCompleted(DomainEvent):
    session_id: str
    completed_at: datetime

class SessionTicked(DomainEvent):
    """
    Event emitted on every tick of the session.
    Listeners can use this to generate coaching instructions.
    """
    session_id: str
    current_block_index: int
    block_type: BlockType
    current_round: int
    time_left: int
    is_work_phase: bool

class BlockStarted(DomainEvent):
    session_id: str
    block_index: int
    block_type: BlockType
    block_name: str # Translated name or type name

class RoundStarted(DomainEvent):
    session_id: str
    round_number: int
    total_rounds: int
    duration: int # work_time

class RestStarted(DomainEvent):
    session_id: str
    duration: int

class AnnouncementTriggered(DomainEvent):
    """
    Event to trigger a voice announcement.
    Infrastructure will listen to this and use TTS.
    """
    session_id: str
    text: str
    # Context hints for voice modulation
    is_instruction: bool = False 
    is_encouragement: bool = False
    language_code: str = "en"
