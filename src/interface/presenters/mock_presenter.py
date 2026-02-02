
import time
import random
from src.interface.presenters.base import BasePresenter, WorkoutViewModel
from src.interface.view.resources import TRANSLATIONS, THEMES

class MockPresenter(BasePresenter):
    def __init__(self, language='fr'):
        self.language = language
        self.is_running = False
        self.time_left = 180
        self.total_time = 180
        self.current_round = 1
        self.total_rounds = 3
        self.is_work_phase = True
        self.current_block_name = "Mock Block"
        self.instruction = "Ready?"
        self.blocks = ["warmup", "shadowBoxing", "heavyBag"]
        self.block_index = 0
        
    def set_language(self, language_code: str):
        self.language = language_code

    def start_workout(self):
        self.is_running = True

    def pause_workout(self):
        self.is_running = False

    def reset_workout(self):
        self.is_running = False
        self.time_left = 180
        self.current_round = 1
        self.block_index = 0
        self.is_work_phase = True
        self.instruction = "Reset"
        
    def tick(self) -> WorkoutViewModel:
        if self.is_running:
            if self.time_left > 0:
                self.time_left -= 1
                # Mock instruction change
                if self.time_left % 5 == 0 and self.is_work_phase:
                     self.instruction = random.choice(["Jab", "Cross", "Hook", "Low Kick", "Move!"])
            else:
                # Phase switch logic for mock
                if self.is_work_phase:
                    self.is_work_phase = False
                    self.time_left = 30 # Rest
                    self.total_time = 30
                    self.instruction = "Rest"
                else:
                    self.is_work_phase = True
                    self.time_left = 180
                    self.total_time = 180
                    self.current_round += 1
                    if self.current_round > self.total_rounds:
                        self.current_round = 1
                        self.block_index = (self.block_index + 1) % len(self.blocks)
                        
        return self.get_current_view_model()

    def get_current_view_model(self) -> WorkoutViewModel:
        t = TRANSLATIONS.get(self.language, TRANSLATIONS['en'])
        
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        
        status_text = t['work'] if self.is_work_phase else t['rest']
        
        progress = 1.0 - (self.time_left / self.total_time) if self.total_time > 0 else 0
        
        # Simple theme logic
        theme = THEMES['muayThaiCamp']
        bg_color = theme['colors']['cardBg']

        return WorkoutViewModel(
            time_display=time_str,
            status_text=status_text,
            current_round=self.current_round,
            total_rounds=self.total_rounds,
            current_block_name=t.get(self.blocks[self.block_index], self.blocks[self.block_index]),
            current_instruction=self.instruction,
            is_running=self.is_running,
            is_work_phase=self.is_work_phase,
            progress=progress,
            background_color=bg_color
        )
