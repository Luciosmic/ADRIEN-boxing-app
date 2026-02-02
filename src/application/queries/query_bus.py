from abc import ABC, abstractmethod
from typing import Type, Any
from src.application._base.query import Query

class QueryBus(ABC):
    """
    Interface for dispatching queries to their appropriate handlers.
    """
    @abstractmethod
    async def ask(self, query: Query) -> Any:
        """Dispatch a query to its handler and return the result."""
        pass
