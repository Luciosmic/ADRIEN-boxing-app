from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any

Request = TypeVar('Request')
Response = TypeVar('Response')

class UseCase(ABC, Generic[Request, Response]):
    """
    Base class for Use Cases.
    Use Cases orchestrate the flow of data for a specific business requirement.
    """
    
    @abstractmethod
    def execute(self, request: Request) -> Response:
        """Execute the use case logic."""
        pass
