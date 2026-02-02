# This file seems redundant with `src/application/projections/_fakes/in_memory_projection.py`
# But let's provide a generic store for projections if they need persistence separate from the logic.

from typing import Dict, Any

class InMemoryProjectionStore:
    def __init__(self):
        self._data: Dict[str, Any] = {}

    def save(self, key: str, data: Any):
        self._data[key] = data

    def load(self, key: str) -> Any:
        return self._data.get(key)
