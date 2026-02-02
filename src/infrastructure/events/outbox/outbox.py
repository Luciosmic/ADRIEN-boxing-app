from abc import ABC, abstractmethod
from typing import List
from src.domain._base.domain_event import DomainEvent

class Outbox(ABC):
    """
    Interface for the Outbox pattern.
    Ensures that events are published eventually even if the app crashes after local commit.
    """
    @abstractmethod
    async def save(self, events: List[DomainEvent]):
        """Persist events to the outbox storage."""
        pass

    @abstractmethod
    async def publish_pending(self):
        """Publish pending events from the outbox."""
        pass
