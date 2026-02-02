from typing import Dict, Type, List, Callable
from src.domain._base.domain_event import DomainEvent
from collections import defaultdict

class EventHandlerRegistry:
    """
    Registry for mapping Domain Events to multiple handlers (subscribers).
    """
    def __init__(self):
        self._handlers: Dict[Type[DomainEvent], List[Callable]] = defaultdict(list)

    def subscribe(self, event_type: Type[DomainEvent], handler: Callable):
        """Register a handler for a specific event type."""
        self._handlers[event_type].append(handler)

    def get_handlers(self, event_type: Type[DomainEvent]) -> List[Callable]:
        """Retrieve all handlers for a specific event type."""
        return self._handlers[event_type]
