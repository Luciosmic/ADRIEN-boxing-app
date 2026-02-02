from typing import List
from uuid import UUID
from src.domain._base.domain_event import DomainEvent
from src.infrastructure.events.store.event_store import EventStore

# Placeholder for real persistence
class SQLiteEventStore(EventStore):
    async def append(self, aggregate_id: UUID, events: List[DomainEvent], expected_version: int) -> None:
        pass

    async def get(self, aggregate_id: UUID) -> List[DomainEvent]:
        return []
