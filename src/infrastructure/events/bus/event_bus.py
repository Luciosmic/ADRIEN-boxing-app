from abc import ABC, abstractmethod
from typing import List
from src.domain._base.domain_event import DomainEvent

class EventBus(ABC):
    """
    Interface for publishing events.
    """
    @abstractmethod
    async def publish(self, events: List[DomainEvent]):
        """Publish a list of events."""
        pass
