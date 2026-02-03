
import asyncio
import uuid
from typing import Optional, List

from src.interface.presenters.base import BasePresenter, WorkoutViewModel
from src.application.training_service.i_api_training_service import ITrainingService
from src.application.coaching_service.i_api_coaching_service import IApiCoachingService
from src.application.training_service.dtos.training_request_dtos import (
    StartSessionRequest, TickSessionRequest, PauseSessionRequest,
    ResumeSessionRequest, GetSessionRequest, CreateWorkoutRequest,
    MoveBlockRequest, GetWorkoutRequest
)
from src.application.coaching_service.dtos import GetInstructionRequest
from src.domain.training.session import SessionStatus
from src.domain.training.value_objects import BlockType
from src.interface.view.resources import TRANSLATIONS, THEMES

class TrainingPresenter(BasePresenter):
    def __init__(
        self, 
        training_service: ITrainingService,
        coaching_service: IApiCoachingService,
        coaching_listener: Optional[object] = None,  # CoachingListener for context management
        language='fr'
    ):
        self.training_service = training_service
        self.coaching_service = coaching_service
        self.coaching_listener = coaching_listener
        self.language = language
        self.session_id = str(uuid.uuid4())
        self.current_workout_id: Optional[str] = None
        self.workouts_summary: List = [] 
        
        # Cached state
        self._cached_session_state = None
        self._cached_workout_detail = None
    
    def set_language(self, language_code: str):
        self.language = language_code

    async def initialize(self):
        # Load workouts
        from src.interface.services.workout_seeder import WorkoutSeeder
        from src.application.training_service.dtos.training_request_dtos import ListWorkoutsRequest
        
        # Seed if empty
        seeder = WorkoutSeeder(self.training_service)
        self.workouts_summary = await seeder.seed()
        
        if self.workouts_summary:
             self.current_workout_id = self.workouts_summary[0].id
             await self.load_workout_detail(self.current_workout_id)

    async def load_workout_detail(self, workout_id: str):
        self.current_workout_id = workout_id
        detail = await self.training_service.get_workout(GetWorkoutRequest(workout_id=workout_id))
        self._cached_workout_detail = detail

    async def select_workout(self, workout_id: str):
        await self.load_workout_detail(workout_id)

    async def move_block(self, from_index: int, to_index: int):
        if not self.current_workout_id:
            return
            
        await self.training_service.move_block(MoveBlockRequest(
            workout_id=self.current_workout_id,
            from_index=from_index,
            to_index=to_index
        ))
        # Refresh detail
        await self.load_workout_detail(self.current_workout_id)

    # --- Synchronous wrappers for Streamlit buttons (delegated to async runner in View) --
    # In Streamlit, we usually run loop.run_until_complete, but here we define async methods 
    # and let the view handle the execution.

    async def start_workout(self):
        if not self.current_workout_id:
            return
            
        # Start new session
        response = await self.training_service.start_session(StartSessionRequest(
            session_id=self.session_id,
            workout_id=self.current_workout_id
        ))
        
        # Refresh state immediately
        state = await self.training_service.get_session(GetSessionRequest(session_id=self.session_id))
        self._cached_session_state = state
        
        # Set coaching listener context if available
        if self.coaching_listener and self._cached_workout_detail:
            self.coaching_listener.set_session_context(
                self.session_id,
                self._cached_workout_detail
            )

    async def pause_workout(self):
        await self.training_service.pause_session(PauseSessionRequest(session_id=self.session_id))
        # Refresh state
        state = await self.training_service.get_session(GetSessionRequest(session_id=self.session_id))
        self._cached_session_state = state

    async def resume_workout(self):
        await self.training_service.resume_session(ResumeSessionRequest(session_id=self.session_id))
        # Refresh state
        state = await self.training_service.get_session(GetSessionRequest(session_id=self.session_id))
        self._cached_session_state = state
        
    async def reset_workout(self):
        # Reset by creating new session ID
        self.session_id = str(uuid.uuid4())
        self._cached_session_state = None

    async def tick(self) -> WorkoutViewModel:
        # 1. Send Tick Command (this will emit SessionTicked event → CoachingListener handles audio)
        await self.training_service.tick_session(TickSessionRequest(session_id=self.session_id))
        
        # 2. Get State
        state = await self.training_service.get_session(GetSessionRequest(session_id=self.session_id))
        self._cached_session_state = state
        
        # 3. Get instruction from CoachingService (for UI display only)
        instruction_text = ""
        if state and state.status == SessionStatus.RUNNING:
            instruction_text = await self._get_instruction(state)
            
        return self.get_current_view_model(instruction_text)
    
    async def _get_instruction(self, state) -> str:
        """Get coaching instruction from CoachingService."""
        if not self._cached_workout_detail:
            return ""
        
        # Get current block
        if state.current_block_index >= len(self._cached_workout_detail.blocks):
            return ""
        
        block = self._cached_workout_detail.blocks[state.current_block_index]
        
        # Build request
        request = GetInstructionRequest(
            session_id=self.session_id,
            block_type=block.type,
            time_left=state.time_left,
            is_work_phase=state.is_work_phase,
            language=self.language,
            techniques=getattr(block, 'techniques', None),
            exercises=getattr(block, 'exercises', None)
        )
        
        # Get instruction from service
        response = await self.coaching_service.get_instruction(request)
        return response.text

    def get_current_view_model(self, instruction_text: str = "") -> WorkoutViewModel:
        t = TRANSLATIONS.get(self.language, TRANSLATIONS['en'])
        
        if not self._cached_session_state:
            # Idle state
            return WorkoutViewModel(
                time_display="00:00",
                status_text="Ready",
                current_round=1,
                total_rounds=0,
                current_block_name="",
                current_instruction=instruction_text or "Ready",
                is_running=False,
                is_work_phase=True,
                progress=0.0,
                background_color=THEMES['muayThaiCamp']['colors']['cardBg']
            )

        state = self._cached_session_state
        
        # Block Name
        block_name = ""
        current_block = None
        if self._cached_workout_detail and state.current_block_index < len(self._cached_workout_detail.blocks):
            current_block = self._cached_workout_detail.blocks[state.current_block_index]
            block_name = t.get(current_block.type, current_block.type)
        else:
             block_name = "Finished"

        minutes = state.time_left // 60
        seconds = state.time_left % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        
        status_text = t['work'] if state.is_work_phase else t['rest']
        if state.status == SessionStatus.COMPLETED:
            status_text = t['trainingComplete']
            
        total_time = 0
        if current_block:
             total_time = current_block.work_time if state.is_work_phase else current_block.rest_time
        
        progress = 0.0
        if total_time > 0:
            progress = 1.0 - (state.time_left / total_time)

        return WorkoutViewModel(
            time_display=time_str,
            status_text=status_text,
            current_round=state.current_round,
            total_rounds=current_block.rounds if current_block else 0,
            current_block_name=block_name,
            current_instruction=instruction_text,
            is_running=state.status == SessionStatus.RUNNING,
            is_work_phase=state.is_work_phase,
            progress=max(0.0, min(1.0, progress)),
            background_color=THEMES['muayThaiCamp']['colors']['cardBg']
        )
