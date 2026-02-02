import json
from typing import Any, Type, Dict
from src.infrastructure._common.serialization.serializer import Serializer
from src.domain._base.domain_event import DomainEvent
# Register Domain Events here (Manually for now, or via decorator later)
from src.domain.training.events import (
    SessionStarted, SessionPaused, SessionResumed, SessionCompleted,
    BlockStarted, RoundStarted, RestStarted, AnnouncementTriggered
)

EVENT_REGISTRY: Dict[str, Type[DomainEvent]] = {
    "SessionStarted": SessionStarted,
    "SessionPaused": SessionPaused,
    "SessionResumed": SessionResumed,
    "SessionCompleted": SessionCompleted,
    "BlockStarted": BlockStarted,
    "RoundStarted": RoundStarted,
    "RestStarted": RestStarted,
    "AnnouncementTriggered": AnnouncementTriggered
}

class EventSerializer(Serializer):
    """
    JSON Serializer for Domain Events.
    Uses dataclasses.asdict or similar mechanism.
    """
    def serialize(self, event: DomainEvent) -> str:
        # Simple implementation, can be robustified
        return json.dumps(event.model_dump(), default=str)

    def deserialize(self, data: str, cls: Type[DomainEvent] = None, event_type: str = None) -> DomainEvent:
        if cls is None and event_type:
            cls = EVENT_REGISTRY.get(event_type)
        
        if not cls:
            raise ValueError(f"Unknown event type: {event_type}")

        data_dict = json.loads(data)
        # Handle datetime conversion if needed, but Pydantic might handle ISO strings automatically
        return cls(**data_dict)
