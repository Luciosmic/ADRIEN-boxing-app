from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from src.domain._base.aggregate_root import AggregateRoot

class SnapshotStore(ABC):
    """
    Interface for storing and retrieving aggregate snapshots.
    """
    @abstractmethod
    def save(self, aggregate: AggregateRoot):
        pass

    @abstractmethod
    def get(self, aggregate_id: UUID) -> Optional[AggregateRoot]:
        pass
