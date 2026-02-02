from datetime import datetime
from uuid import uuid4, UUID
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class DomainEvent(BaseModel):
    """
    Base class for all domain events.
    Events are immutable facts that happened in the past.
    """
    # Unique identifier for the event occurrence
    event_id: UUID = Field(default_factory=uuid4)
    # When the event occurred
    occurred_on: datetime = Field(default_factory=datetime.utcnow)
    # Version of the event schema
    version: int = 1
    # Optional correlation ID for tracing
    correlation_id: Optional[str] = None
    
    class Config:
        frozen = True # Events are immutable
        arbitrary_types_allowed = True

    @property
    def event_name(self) -> str:
        return self.__class__.__name__

    def to_dict(self) -> dict:
        """
        Serialize the event to a dictionary.
        Separates metadata from the actual event payload.
        """
        # Pydantic's model_dump (v2) or dict (v1). Using v1 style for broader compat or v2 calls if standard.
        # Let's assume Pydantic V2 is preferred for new projects.
        try:
            data = self.model_dump()
        except AttributeError:
            data = self.dict()

        # Extract metadata
        metadata = {
            "event_id": str(self.event_id),
            "event_name": self.event_name,
            "occurred_on": self.occurred_on.isoformat(),
            "version": self.version,
            "correlation_id": self.correlation_id
        }
        
        # Remove metadata fields from payload
        for key in metadata.keys():
            if key in data and key != "event_name":
                del data[key]
        
        return {
            "metadata": metadata,
            "payload": data
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Deserialize from a dictionary structure.
        """
        metadata = data.get("metadata", {})
        payload = data.get("payload", {})
        
        # Reconstruct arguments
        kwargs = payload.copy()
        if "event_id" in metadata:
            kwargs["event_id"] = metadata["event_id"]
        if "occurred_on" in metadata:
            kwargs["occurred_on"] = metadata["occurred_on"]
        if "version" in metadata:
            kwargs["version"] = metadata["version"]
        if "correlation_id" in metadata:
            kwargs["correlation_id"] = metadata["correlation_id"]
            
        return cls(**kwargs)
