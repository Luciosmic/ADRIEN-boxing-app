from dataclasses import dataclass
from typing import List, Optional
from src.domain.training.value_objects import Block

@dataclass(frozen=True)
class CreateWorkoutRequest:
    name: str
    blocks: List[Block]

@dataclass(frozen=True)
class StartSessionRequest:
    workout_id: str
    session_id: Optional[str] = None # Optional, service can generate if not provided

@dataclass(frozen=True)
class TickSessionRequest:
    session_id: str

@dataclass(frozen=True)
class PauseSessionRequest:
    session_id: str

@dataclass(frozen=True)
class ResumeSessionRequest:
    session_id: str

@dataclass(frozen=True)
class SkipBlockRequest:
    session_id: str

@dataclass(frozen=True)
class MoveBlockRequest:
    workout_id: str
    from_index: int
    to_index: int

@dataclass(frozen=True)
class GetSessionRequest:
    session_id: str

@dataclass(frozen=True)
class ListWorkoutsRequest:
    pass

@dataclass(frozen=True)
class GetWorkoutRequest:
    workout_id: str
