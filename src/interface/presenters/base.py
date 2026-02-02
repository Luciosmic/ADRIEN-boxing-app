
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class WorkoutViewModel:
    time_display: str  # "03:00"
    status_text: str   # "Work" / "Rest"
    current_round: int
    total_rounds: int
    current_block_name: str # "Jump Rope"
    current_instruction: str # "Speed up!" or "Jab - Cross" or ""
    is_running: bool
    is_work_phase: bool
    progress: float # 0.0 to 1.0 for progress bar
    background_color: str # CSS color or class hint
    
class BasePresenter(ABC):
    
    @abstractmethod
    def start_workout(self):
        pass

    @abstractmethod
    def pause_workout(self):
        pass

    @abstractmethod
    def reset_workout(self):
        pass
        
    @abstractmethod
    def tick(self) -> WorkoutViewModel:
        """
        Calculates the new state and returns the view model.
        Should be called periodically by the view.
        """
        pass
    
    @abstractmethod
    def set_language(self, language_code: str):
        pass

    @abstractmethod
    def get_current_view_model(self) -> WorkoutViewModel:
        pass
