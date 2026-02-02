from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class StoredEvent:
    """
    Representation of an event as stored in the database.
    This is an internal storage format, separate from the DomainEvent.
    """
    event_id: UUID
    aggregate_id: UUID
    aggregate_version: int
    event_type: str
    event_data: str  # Serialized JSON
    occurred_on: datetime
    correlation_id: str = None
