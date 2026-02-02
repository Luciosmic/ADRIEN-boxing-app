from typing import Dict, Optional, TypeVar, Generic
from uuid import UUID
from src.domain.repositories.i_repository import IRepository
from src.domain._base.aggregate_root import AggregateRoot

T = TypeVar('T', bound=AggregateRoot)

class InMemoryRepository(IRepository[T]):
    """
    Generic In-Memory Repository for testing.
    """
    def __init__(self):
        self._store: Dict[UUID, T] = {}

    async def save(self, aggregate: T) -> None:
        self._store[aggregate.id] = aggregate

    async def get_by_id(self, id: UUID) -> Optional[T]:
        return self._store.get(id)
