from abc import ABC, abstractmethod
from typing import Type
from src.application._base.command import Command

class CommandBus(ABC):
    """
    Interface for dispatching commands to their appropriate handlers.
    """
    @abstractmethod
    async def dispatch(self, command: Command) -> None:
        """Dispatch a command to its handler."""
        pass
