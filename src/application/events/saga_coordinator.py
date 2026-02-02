from abc import ABC, abstractmethod
from src.domain._base.domain_event import DomainEvent

class SagaCoordinator(ABC):
    """
    Base class for Saga Coordinators.
    Sagas manage long-running processes by listening to events and dispatching commands.
    """
    
    @abstractmethod
    def handle(self, event: DomainEvent):
        """Handle an incoming event and decide on next steps."""
        pass
