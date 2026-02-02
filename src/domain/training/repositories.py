from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.training.workout import Workout
from src.domain.training.session import TrainingSession

class IWorkoutRepository(ABC):
    @abstractmethod
    async def save(self, workout: Workout) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, workout_id: str) -> Optional[Workout]:
        pass

    @abstractmethod
    async def list_all(self) -> List[Workout]:
        pass

    @abstractmethod
    async def delete(self, workout_id: str) -> None:
        pass

class ISessionRepository(ABC):
    @abstractmethod
    async def save(self, session: TrainingSession) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, session_id: str) -> Optional[TrainingSession]:
        pass
