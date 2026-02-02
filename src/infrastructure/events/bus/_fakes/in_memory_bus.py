from typing import List
from src.domain._base.domain_event import DomainEvent
from src.infrastructure.events.bus.event_bus import EventBus
from src.application.events.event_handler_registry import EventHandlerRegistry

class InMemoryEventBus(EventBus):
    """
    Synchronous In-Memory Event Bus.
    """
    def __init__(self, registry: EventHandlerRegistry):
        self._registry = registry

    async def publish(self, events: List[DomainEvent]):
        for event in events:
            handlers = self._registry.get_handlers(type(event))
            for handler in handlers:
                # Assuming handlers can be async or sync, ideally we standardize on async handlers too
                # For now, let's support both or just assume they are awaited if they are coroutines.
                import inspect
                if inspect.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
