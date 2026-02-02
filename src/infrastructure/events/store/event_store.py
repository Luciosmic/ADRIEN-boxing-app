from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from src.domain._base.domain_event import DomainEvent

class EventStore(ABC):
    """
    Interface for appending and retrieving events for an aggregate (Event Sourcing).
    """
    @abstractmethod
    async def append(self, aggregate_id: UUID, events: List[DomainEvent], expected_version: int) -> None:
        """Append events to the stream."""
        pass

    @abstractmethod
    async def get(self, aggregate_id: UUID) -> List[DomainEvent]:
        """Retrieve all events for an aggregate."""
        pass
