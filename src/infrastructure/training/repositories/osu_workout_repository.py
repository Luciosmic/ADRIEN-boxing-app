import os
import json
from typing import List, Optional
from src.domain.training.repositories import IWorkoutRepository
from src.domain.training.workout import Workout

class OsuWorkoutRepository(IWorkoutRepository):
    def __init__(self, base_path: str = ".osu/persistence/workouts"):
        self.base_path = base_path
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    async def save(self, workout: Workout) -> None:
        file_path = os.path.join(self.base_path, f"{workout.id}.json")
        with open(file_path, "w") as f:
            f.write(workout.model_dump_json(indent=2))

    async def get_by_id(self, workout_id: str) -> Optional[Workout]:
        file_path = os.path.join(self.base_path, f"{workout_id}.json")
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, "r") as f:
            data = json.load(f)
            return Workout(**data)

    async def list_all(self) -> List[Workout]:
        workouts = []
        if not os.path.exists(self.base_path):
            return []
            
        for filename in os.listdir(self.base_path):
            if filename.endswith(".json"):
                try:
                    with open(os.path.join(self.base_path, filename), "r") as f:
                        data = json.load(f)
                        workouts.append(Workout(**data))
                except Exception:
                    continue # specific error handling could be better
        return workouts

    async def delete(self, workout_id: str) -> None:
        file_path = os.path.join(self.base_path, f"{workout_id}.json")
        if os.path.exists(file_path):
            os.remove(file_path)
