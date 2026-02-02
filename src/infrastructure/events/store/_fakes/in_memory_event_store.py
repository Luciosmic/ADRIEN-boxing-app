from typing import List, Dict, Tuple
from uuid import UUID
from src.domain._base.domain_event import DomainEvent
from src.infrastructure.events.store.event_store import EventStore

class InMemoryEventStore(EventStore):
    def __init__(self):
        # Map aggregate_id -> List[(version, event)]
        self._streams: Dict[UUID, List[DomainEvent]] = {}
    
    async def append(self, aggregate_id: UUID, events: List[DomainEvent], expected_version: int) -> None:
        if aggregate_id not in self._streams:
            self._streams[aggregate_id] = []
        
        current_stream = self._streams[aggregate_id]
        current_version = len(current_stream) # Simplified versioning
        
        if current_version != expected_version and expected_version != -1:
            raise Exception(f"Concurrency mismatch. Expected {expected_version}, got {current_version}")

        self._streams[aggregate_id].extend(events)

    async def get(self, aggregate_id: UUID) -> List[DomainEvent]:
        return self._streams.get(aggregate_id, [])
