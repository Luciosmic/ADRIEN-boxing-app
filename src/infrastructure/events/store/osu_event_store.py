import os
import json
from typing import List
from uuid import UUID
from datetime import datetime

from src.infrastructure.events.store.event_store import EventStore
from src.infrastructure.events.store.stored_event import StoredEvent
from src.domain._base.domain_event import DomainEvent
from src.infrastructure._common.serialization.event_serializer import EventSerializer

class OsuFileEventStore(EventStore):
    def __init__(self, base_path: str = ".osu"):
        self.base_path = base_path
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
        self.serializer = EventSerializer()

    async def append(self, aggregate_id: UUID, events: List[DomainEvent], expected_version: int) -> None:
        file_path = os.path.join(self.base_path, f"{aggregate_id}.jsonl")
        
        # In a real file store, we would check versions (optimistic locking) by reading the file line count.
        # For this prototype, we just append.
        
        new_version = expected_version
        
        with open(file_path, "a") as f:
            for event in events:
                new_version += 1
                stored = StoredEvent(
                    event_id=UUID(int=0), # Generate or use event.id if available? DomainEvent usually doesn't have ID. generated here.
                    aggregate_id=aggregate_id,
                    aggregate_version=new_version,
                    event_type=event.__class__.__name__,
                    event_data=event.model_dump_json() if hasattr(event, "model_dump_json") else self.serializer.serialize(event),
                    occurred_on=datetime.now(), # Or event.occurred_on if available? DomainEvent usually expects us to track store time.
                    correlation_id=None
                )
                
                # We store the StoredEvent as a JSON line
                # We need to serialize StoredEvent (dataclass) to dict
                data = {
                    "event_id": str(stored.event_id),
                    "aggregate_id": str(stored.aggregate_id),
                    "aggregate_version": stored.aggregate_version,
                    "event_type": stored.event_type,
                    "event_data": stored.event_data,
                    "occurred_on": stored.occurred_on.isoformat(),
                    "correlation_id": stored.correlation_id
                }
                f.write(json.dumps(data) + "\n")

    async def get(self, aggregate_id: UUID) -> List[DomainEvent]:
        file_path = os.path.join(self.base_path, f"{aggregate_id}.jsonl")
        if not os.path.exists(file_path):
            return []
            
        events = []
        with open(file_path, "r") as f:
            for line in f:
                if not line.strip(): continue
                
                # StoredEvent JSON
                stored_data = json.loads(line)
                
                # Deserialize the inner event_data
                try:
                    domain_event = self.serializer.deserialize(
                        stored_data["event_data"], 
                        event_type=stored_data["event_type"]
                    )
                    events.append(domain_event)
                except ValueError as e:
                    print(f"Skipping unknown event type: {e}")
                    continue
                    
        return events
