from abc import ABC, abstractmethod
from src.domain._base.domain_event import DomainEvent

class Projection(ABC):
    """
    Base class for Projections (Read Models).
    Projections listen to events and update read-optimized models.
    """
    
    @abstractmethod
    def handle(self, event: DomainEvent):
        """Update the projection based on the event."""
        pass
    
    @abstractmethod
    def clear(self):
        """Clear the projection data."""
        pass
