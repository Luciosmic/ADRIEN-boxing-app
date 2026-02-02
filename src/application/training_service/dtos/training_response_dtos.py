from dataclasses import dataclass
from typing import List, Optional
from src.domain.training.session import SessionStatus
from src.domain.training.value_objects import Block

@dataclass(frozen=True)
class CreateWorkoutResponse:
    workout_id: str

@dataclass(frozen=True)
class StartSessionResponse:
    session_id: str

@dataclass(frozen=True)
class ActionResponse:
    """Generic response for void actions (Tick, Pause, Resume, etc.)"""
    success: bool = True
    message: Optional[str] = None

@dataclass(frozen=True)
class SessionStateResponse:
    id: str
    workout_name: str
    status: SessionStatus
    current_block_index: int
    current_round: int
    time_left: int
    is_work_phase: bool

@dataclass(frozen=True)
class WorkoutSummaryResponse:
    id: str
    name: str

@dataclass(frozen=True)
class WorkoutDetailResponse:
    id: str
    name: str
    blocks: List[Block]
