from typing import List, Dict
from uuid import UUID
from src.infrastructure.events.store.event_store import EventStore
from src.domain._base.domain_event import DomainEvent

class InMemoryEventStore(EventStore):
    def __init__(self):
        self._store: Dict[UUID, List[DomainEvent]] = {}

    async def append(self, aggregate_id: UUID, events: List[DomainEvent], expected_version: int = None) -> None:
        if aggregate_id not in self._store:
            self._store[aggregate_id] = []
        
        # Concurrency check could be mocked here using expected_version vs len(self._store[aggregate_id])
        
        self._store[aggregate_id].extend(events)

    async def get(self, aggregate_id: UUID) -> List[DomainEvent]:
        return self._store.get(aggregate_id, [])
