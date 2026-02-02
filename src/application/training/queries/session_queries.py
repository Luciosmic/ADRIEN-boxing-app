from typing import Optional
from pydantic import BaseModel
from src.application._base.query import Query
from src.domain.training.repositories import ISessionRepository
from src.domain.training.session import SessionStatus

# --- DTOs ---

class SessionDTO(BaseModel):
    id: str
    workout_name: str
    status: SessionStatus
    current_block_index: int
    current_round: int
    time_left: int
    is_work_phase: bool

# --- Queries ---

class GetSession(Query):
    session_id: str

# --- Handlers ---

class GetSessionHandler:
    def __init__(self, session_repo: ISessionRepository):
        self.session_repo = session_repo

    async def __call__(self, query: GetSession) -> Optional[SessionDTO]:
        session = await self.session_repo.get_by_id(query.session_id)
        if not session:
            return None
        
        return SessionDTO(
            id=str(session.id),
            workout_name=session.workout.name,
            status=session.status,
            current_block_index=session.current_block_index,
            current_round=session.current_round,
            time_left=session.time_left,
            is_work_phase=session.is_work_phase
        )
