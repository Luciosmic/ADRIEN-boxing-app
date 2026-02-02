from abc import ABC, abstractmethod

class AbstractUnitOfWork(ABC):
    """
    Interface for Unit of Work.
    Manages atomic transactions.
    """
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    @abstractmethod
    async def commit(self):
        """Commit the transaction."""
        pass

    @abstractmethod
    async def rollback(self):
        """Rollback the transaction."""
        pass
