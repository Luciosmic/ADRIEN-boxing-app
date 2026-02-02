from typing import List
from src.domain._base.domain_event import DomainEvent
from src.infrastructure.events.outbox.outbox import Outbox
from src.infrastructure.events.bus.event_bus import EventBus

class InMemoryOutbox(Outbox):
    def __init__(self, event_bus: EventBus):
        self._queue: List[DomainEvent] = []
        self._event_bus = event_bus

    async def save(self, events: List[DomainEvent]):
        self._queue.extend(events)

    async def publish_pending(self):
        if self._queue:
            # Publish all pending events
            await self._event_bus.publish(self._queue)
            self._queue.clear()
