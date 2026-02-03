from typing import List, Callable, Dict, Type
from src.domain._base.domain_event import DomainEvent
from src.domain._base.event_bus import EventBus

class InMemoryEventBus(EventBus):
    def __init__(self):
        self._subscribers: Dict[Type[DomainEvent], List[Callable]] = {}

    def subscribe(self, event_type: Type[DomainEvent], handler: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    async def publish(self, events: List[DomainEvent]):
        for event in events:
            event_type = type(event)
            if event_type in self._subscribers:
                for handler in self._subscribers[event_type]:
                    # Execute handler. If handlers are async, await them.
                    # Assuming async handlers for now.
                    await handler(event)
