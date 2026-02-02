from typing import Optional, Dict
from uuid import UUID
from src.domain.training.repositories import ISessionRepository
from src.domain.training.session import TrainingSession
from src.infrastructure.events.store.event_store import EventStore

class InMemorySessionRepository(ISessionRepository):
    def __init__(self, event_store: EventStore):
        self.event_store = event_store
        self._store: Dict[str, TrainingSession] = {}

    async def save(self, session: TrainingSession) -> None:
        # 1. Event Log
        events = session.collect_domain_events()
        if events:
            await self.event_store.append(session.id, events, expected_version=0)
            
        # 2. State Snapshot (In Memory)
        self._store[str(session.id)] = session

    async def get_by_id(self, session_id: str) -> Optional[TrainingSession]:
        return self._store.get(str(session_id))
