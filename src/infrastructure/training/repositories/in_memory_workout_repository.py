from typing import List, Optional, Dict
from src.domain.training.repositories import IWorkoutRepository
from src.domain.training.workout import Workout

class InMemoryWorkoutRepository(IWorkoutRepository):
    def __init__(self):
        self._store: Dict[str, Workout] = {}

    async def save(self, workout: Workout) -> None:
        self._store[workout.id] = workout

    async def get_by_id(self, workout_id: str) -> Optional[Workout]:
        # Return a copy to mimic persistence boundary? 
        # For simple mocks, returning reference is often okay but copy is safer.
        # Assuming Pydantic models are immutable-ish or we don't care about reference mutation in mocks for now.
        return self._store.get(workout_id)

    async def list_all(self) -> List[Workout]:
        return list(self._store.values())

    async def delete(self, workout_id: str) -> None:
        if workout_id in self._store:
            del self._store[workout_id]
