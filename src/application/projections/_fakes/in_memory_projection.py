from typing import Dict, Any, List
from src.domain._base.domain_event import DomainEvent
from src.application.projections.projection_base import Projection

class InMemoryProjection(Projection):
    """
    A simple in-memory key-value projection for testing/prototyping.
    """
    def __init__(self):
        self._data: Dict[str, Any] = {}

    def handle(self, event: DomainEvent):
        # Base implementation doesn't know how to handle specific events.
        # Subclasses should override or extend this.
        pass

    def get(self, key: str) -> Any:
        return self._data.get(key)
    
    def set(self, key: str, value: Any):
        self._data[key] = value

    def get_all(self) -> Dict[str, Any]:
        return self._data.copy()

    def clear(self):
        self._data.clear()
