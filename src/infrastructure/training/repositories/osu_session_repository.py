import os
import json
from typing import Optional
from typing import Optional, List
# from uuid import UUID # Not used in the modified code

from src.domain._base.event_bus import EventBus
from src.domain.training.repositories import ISessionRepository
from src.domain.training.session import TrainingSession
from src.infrastructure.events.store.event_store import EventStore

class OsuSessionRepository(ISessionRepository):
    def __init__(self, event_store: EventStore, base_path: str = ".osu/persistence/sessions", event_bus: Optional[EventBus] = None):
        self.event_store = event_store
        self.base_path = base_path
        self.event_bus = event_bus
        os.makedirs(self.base_path, exist_ok=True)
        # We also need to ensure event store path exists... handled by store itself.

    async def save(self, session: TrainingSession) -> None:
        # 1. Collect Events
        events = session.collect_domain_events()
        
        # 2. Append to Event Store
        if events:
            # Get current version from event store (count of existing events)
            # For new aggregates, version starts at 0
            existing_events = await self.event_store.get(session.id)
            expected_version = len(existing_events)
            
            await self.event_store.append(session.id, events, expected_version)
            
            # 3. Publish to Bus (Side Effects)
            if self.event_bus:
                await self.event_bus.publish(events)
        
        # 4. Save Snapshot (Optimization/Recovery)
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
 
