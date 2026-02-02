from abc import ABC, abstractmethod
from typing import Dict, Any

class EventUpcaster(ABC):
    """
    Interface for upgrading old event schemas to new ones.
    """
    @abstractmethod
    def upcast(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform the raw event data (e.g., from JSON) to the latest version."""
        pass
