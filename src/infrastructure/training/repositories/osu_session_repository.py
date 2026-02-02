import os
import json
from typing import Optional
from uuid import UUID

from src.domain.training.repositories import ISessionRepository
from src.domain.training.session import TrainingSession
from src.infrastructure.events.store.event_store import EventStore

class OsuSessionRepository(ISessionRepository):
    def __init__(self, event_store: EventStore, base_path: str = ".osu/persistence/sessions"):
        self.event_store = event_store
        self.base_path = base_path
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    async def save(self, session: TrainingSession) -> None:
        # 1. Event Log (Semantic Tracking)
        events = session.collect_domain_events()
        if events:
            await self.event_store.append(session.id, events, expected_version=0)
            
        # 2. State Snapshot (Recovery)
        # We assume TrainingSession (and its sub-models) are Pydantic models
        file_path = os.path.join(self.base_path, f"{session.id}.json")
        with open(file_path, "w") as f:
            f.write(session.model_dump_json(indent=2))

    async def get_by_id(self, session_id: str) -> Optional[TrainingSession]:
        file_path = os.path.join(self.base_path, f"{session_id}.json")
        if not os.path.exists(file_path):
            return None
            
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                return TrainingSession(**data)
        except Exception as e:
            print(f"Error loading session {session_id}: {e}")
            return None
 
