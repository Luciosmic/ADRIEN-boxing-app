from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional
from src.domain._base.aggregate_root import AggregateRoot

T = TypeVar('T', bound=AggregateRoot)

class IRepository(ABC, Generic[T]):
    """
    Generic Repository Interface.
    Repositories mediate between the domain and data mapping layers.
    """
    
    @abstractmethod
    async def save(self, aggregate: T) -> None:
        """Save the aggregate state."""
        pass

    @abstractmethod
    async def get_by_id(self, id) -> Optional[T]:
        """Retrieve an aggregate by its ID."""
        pass
