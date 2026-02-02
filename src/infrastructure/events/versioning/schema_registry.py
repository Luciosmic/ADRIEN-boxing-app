from typing import Dict, Type
from src.infrastructure.events.versioning.event_upcaster import EventUpcaster

class SchemaRegistry:
    """
    Registry for managing event schemas and their upcasters.
    """
    def __init__(self):
        self._upcasters: Dict[str, EventUpcaster] = {}

    def register_upcaster(self, event_type: str, upcaster: EventUpcaster):
        self._upcasters[event_type] = upcaster
    
    def get_upcaster(self, event_type: str) -> EventUpcaster:
        return self._upcasters.get(event_type)
