
import asyncio
from src.application.training_service.i_api_training_service import ITrainingService
from src.application.training_service.dtos.training_request_dtos import CreateWorkoutRequest, ListWorkoutsRequest
from src.domain.training.value_objects import Block, BlockType, Frequency, ExerciseType, TechniqueCategory

class WorkoutSeeder:
    """
    Seeds standard workouts into the repositories via the API service.
    """
    def __init__(self, service: ITrainingService):
        self.service = service

    async def seed(self):
        # Check if workouts already exist
        existing = await self.service.list_workouts(ListWorkoutsRequest())
        if existing:
            return existing

        # Seed standard workouts
        presets = [30, 60, 90]
        created_ids = []
        
        for duration in presets:
            blocks = self._create_blocks(duration)
            response = await self.service.create_workout(CreateWorkoutRequest(
                name=f"Séance {duration} minutes",
                blocks=blocks
            ))
            created_ids.append(response.workout_id)
            
        return await self.service.list_workouts(ListWorkoutsRequest())

    def _create_blocks(self, duration_minutes: int) -> list[Block]:
        if duration_minutes == 30:
            return [
                Block(type=BlockType.WARMUP, rounds=2, work_time=120, rest_time=30, frequency=Frequency.NORMAL),
                Block(type=BlockType.JUMP_ROPE, rounds=2, work_time=180, rest_time=60, frequency=Frequency.NORMAL),
                Block(type=BlockType.STRENGTH, rounds=2, exercises={ExerciseType.PUSHUPS: 15, ExerciseType.SQUATS: 20}),
                Block(type=BlockType.HEAVY_BAG, rounds=3, work_time=120, rest_time=60, 
                      techniques=[TechniqueCategory.PUNCHES, TechniqueCategory.KICKS, TechniqueCategory.COMBOS], 
                      frequency=Frequency.NORMAL),
                Block(type=BlockType.SHADOW_BOXING, rounds=2, work_time=60, rest_time=30, frequency=Frequency.NORMAL),
                Block(type=BlockType.COOLDOWN, rounds=1, work_time=60, rest_time=0, frequency=Frequency.NORMAL)
            ]
        elif duration_minutes == 60:
             return [
                Block(type=BlockType.WARMUP, rounds=2, work_time=180, rest_time=60, frequency=Frequency.NORMAL),
                Block(type=BlockType.JUMP_ROPE, rounds=4, work_time=180, rest_time=60, frequency=Frequency.NORMAL),
                Block(type=BlockType.STRENGTH, rounds=3, exercises={ExerciseType.PUSHUPS: 20, ExerciseType.SQUATS: 25, ExerciseType.BURPEES: 10}),
                Block(type=BlockType.HEAVY_BAG, rounds=5, work_time=180, rest_time=60, 
                      techniques=[TechniqueCategory.PUNCHES, TechniqueCategory.KICKS, TechniqueCategory.KNEES, TechniqueCategory.COMBOS], 
                      frequency=Frequency.NORMAL),
                Block(type=BlockType.SHADOW_BOXING, rounds=3, work_time=120, rest_time=60, frequency=Frequency.NORMAL),
                Block(type=BlockType.COOLDOWN, rounds=2, work_time=60, rest_time=30, frequency=Frequency.NORMAL)
            ]
        elif duration_minutes == 90:
             return [
                Block(type=BlockType.WARMUP, rounds=3, work_time=180, rest_time=60, frequency=Frequency.NORMAL),
                Block(type=BlockType.JUMP_ROPE, rounds=6, work_time=180, rest_time=60, frequency=Frequency.NORMAL),
                Block(type=BlockType.STRENGTH, rounds=4, exercises={ExerciseType.PUSHUPS: 25, ExerciseType.SQUATS: 30, ExerciseType.BURPEES: 15, ExerciseType.ABS: 30}),
                Block(type=BlockType.HEAVY_BAG, rounds=8, work_time=180, rest_time=60, 
                      techniques=[TechniqueCategory.PUNCHES, TechniqueCategory.KICKS, TechniqueCategory.KNEES, TechniqueCategory.ELBOWS, TechniqueCategory.COMBOS], 
                      frequency=Frequency.NORMAL),
                Block(type=BlockType.SHADOW_BOXING, rounds=4, work_time=120, rest_time=60, frequency=Frequency.NORMAL),
                Block(type=BlockType.COOLDOWN, rounds=2, work_time=90, rest_time=30, frequency=Frequency.NORMAL)
            ]
        return []
