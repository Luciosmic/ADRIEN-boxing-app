from abc import ABC, abstractmethod
from typing import Any, Type

class Serializer(ABC):
    @abstractmethod
    def serialize(self, obj: Any) -> str:
        pass

    @abstractmethod
    def deserialize(self, data: str, cls: Type) -> Any:
        pass
