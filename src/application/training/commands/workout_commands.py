from typing import List
from uuid import uuid4
from src.application._base.command import Command
from src.domain.training.repositories import IWorkoutRepository
from src.domain.training.workout import Workout
from src.domain.training.value_objects import Block

# --- Command ---

class CreateWorkout(Command):
    name: str
    blocks: List[Block]

# --- Handler ---

class CreateWorkoutHandler:
    def __init__(self, workout_repo: IWorkoutRepository):
        self.workout_repo = workout_repo

    async def __call__(self, command: CreateWorkout) -> str:
        # Generate ID or assume command has it if we wanted CQRS strictness (Void return).
        # But practical app usually needs ID back.
        # Ideally: ID is passed in command.
        # If not present, we generate.
        workout_id = str(uuid4())
        
        workout = Workout(
            id=workout_id,
            name=command.name,
            blocks=command.blocks
        )
        
        await self.workout_repo.save(workout)
        return workout_id
