from typing import List
from pydantic import PrivateAttr
from .entity import Entity
from .domain_event import DomainEvent

class AggregateRoot(Entity):
    """
    Base class for Aggregate Roots.
    Aggregates act as a consistency boundary and enforce invariants.
    They also capture and hold domain events.
    """
    # Use PrivateAttr so it's not serialized, not part of the model fields
    _domain_events: List[DomainEvent] = PrivateAttr(default_factory=list)

    def add_domain_event(self, event: DomainEvent):
        """Register a domain event that occurred within this aggregate."""
        self._domain_events.append(event)

    def collect_domain_events(self) -> List[DomainEvent]:
        """Return and clear the collected domain events."""
        events = list(self._domain_events)
        self._domain_events.clear()
        return events
    
    def clear_domain_events(self):
        """Clear all domain events."""
        self._domain_events.clear()
