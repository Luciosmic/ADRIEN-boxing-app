from typing import List, Optional
from pydantic import BaseModel
from src.application._base.query import Query
from src.domain.training.repositories import IWorkoutRepository
from src.domain.training.value_objects import Block

# --- DTOs ---

class WorkoutSummaryDTO(BaseModel):
    id: str
    name: str

class WorkoutDetailDTO(WorkoutSummaryDTO):
    blocks: List[Block]

# --- Queries ---

class ListWorkouts(Query):
    pass

class GetWorkout(Query):
    workout_id: str

# --- Handlers ---

class ListWorkoutsHandler:
    def __init__(self, workout_repo: IWorkoutRepository):
        self.workout_repo = workout_repo

    async def __call__(self, query: ListWorkouts) -> List[WorkoutSummaryDTO]:
        workouts = await self.workout_repo.list_all()
        return [WorkoutSummaryDTO(id=str(w.id), name=w.name) for w in workouts]


class GetWorkoutHandler:
    def __init__(self, workout_repo: IWorkoutRepository):
        self.workout_repo = workout_repo

    async def __call__(self, query: GetWorkout) -> Optional[WorkoutDetailDTO]:
        workout = await self.workout_repo.get_by_id(query.workout_id)
        if not workout:
            return None
            
        return WorkoutDetailDTO(
            id=str(workout.id),
            name=workout.name,
            blocks=workout.blocks
        )
