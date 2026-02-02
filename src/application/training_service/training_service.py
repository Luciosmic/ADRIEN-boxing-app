import os
from uuid import uuid4
from typing import List, Optional

from src.application.training_service.i_api_training_service import ITrainingService
# DTOs
from src.application.training_service.dtos.training_request_dtos import (
    CreateWorkoutRequest, StartSessionRequest, TickSessionRequest,
    PauseSessionRequest, ResumeSessionRequest, SkipBlockRequest,
    GetSessionRequest, ListWorkoutsRequest, GetWorkoutRequest
)
from src.application.training_service.dtos.training_response_dtos import (
    CreateWorkoutResponse, StartSessionResponse, ActionResponse,
    SessionStateResponse, WorkoutSummaryResponse, WorkoutDetailResponse
)
# Handlers & Repos
from src.infrastructure.training.repositories.osu_workout_repository import OsuWorkoutRepository
from src.infrastructure.training.repositories.osu_session_repository import OsuSessionRepository
from src.infrastructure.events.store.osu_event_store import OsuFileEventStore
from src.application.training.commands.workout_commands import CreateWorkout, CreateWorkoutHandler
from src.application.training.commands.session_commands import (
    StartSession, StartSessionHandler,
    TickSession, TickSessionHandler,
    PauseSession, PauseSessionHandler,
    ResumeSession, ResumeSessionHandler,
    SkipBlock, SkipBlockHandler
)
from src.application.training.queries.workout_queries import (
    ListWorkouts, ListWorkoutsHandler,
    GetWorkout, GetWorkoutHandler
)
from src.application.training.queries.session_queries import GetSession, GetSessionHandler

class TrainingService(ITrainingService):
    def __init__(
        self, 
        base_path: str = ".osu",
        workout_repo = None,
        session_repo = None,
        event_store = None
    ):
        # Wiring up the infrastructure and handlers manually (Composition Root equivalent)
        # If repos are provided (e.g. Mocks), use them. Otherwise default to Osu/File implementations.
        
        self.workout_repo = workout_repo or OsuWorkoutRepository(base_path=os.path.join(base_path, "persistence", "workouts"))
        
        if not event_store:
            self.event_store = OsuFileEventStore(base_path=os.path.join(base_path, "persistence", "events"))
        else:
            self.event_store = event_store
            
        if not session_repo:
            self.session_repo = OsuSessionRepository(event_store=self.event_store, base_path=os.path.join(base_path, "persistence", "sessions"))
        else:
            self.session_repo = session_repo

        # Handlers
        self._create_workout = CreateWorkoutHandler(self.workout_repo)
        self._list_workouts = ListWorkoutsHandler(self.workout_repo)
        self._get_workout = GetWorkoutHandler(self.workout_repo)
        
        self._start_session = StartSessionHandler(self.session_repo, self.workout_repo)
        self._get_session = GetSessionHandler(self.session_repo)
        self._tick_session = TickSessionHandler(self.session_repo)
        self._pause_session = PauseSessionHandler(self.session_repo)
        self._resume_session = ResumeSessionHandler(self.session_repo)
        self._skip_block = SkipBlockHandler(self.session_repo)

    async def create_workout(self, request: CreateWorkoutRequest) -> CreateWorkoutResponse:
        cmd = CreateWorkout(name=request.name, blocks=request.blocks)
        workout_id = await self._create_workout(cmd)
        return CreateWorkoutResponse(workout_id=workout_id)

    async def list_workouts(self, request: ListWorkoutsRequest) -> List[WorkoutSummaryResponse]:
        dtos = await self._list_workouts(ListWorkouts())
        return [WorkoutSummaryResponse(id=d.id, name=d.name) for d in dtos]

    async def get_workout(self, request: GetWorkoutRequest) -> Optional[WorkoutDetailResponse]:
        dto = await self._get_workout(GetWorkout(workout_id=request.workout_id))
        if not dto:
            return None
        return WorkoutDetailResponse(id=dto.id, name=dto.name, blocks=dto.blocks)

    async def start_session(self, request: StartSessionRequest) -> StartSessionResponse:
        s_id = request.session_id or str(uuid4())
        await self._start_session(StartSession(session_id=s_id, workout_id=request.workout_id))
        return StartSessionResponse(session_id=s_id)

    async def get_session(self, request: GetSessionRequest) -> Optional[SessionStateResponse]:
        dto = await self._get_session(GetSession(session_id=request.session_id))
        if not dto:
            return None
        return SessionStateResponse(
            id=dto.id,
            workout_name=dto.workout_name,
            status=dto.status,
            current_block_index=dto.current_block_index,
            current_round=dto.current_round,
            time_left=dto.time_left,
            is_work_phase=dto.is_work_phase
        )

    async def tick_session(self, request: TickSessionRequest) -> ActionResponse:
        try:
            await self._tick_session(TickSession(session_id=request.session_id))
            return ActionResponse(success=True)
        except ValueError as e:
            return ActionResponse(success=False, message=str(e))

    async def pause_session(self, request: PauseSessionRequest) -> ActionResponse:
        try:
            await self._pause_session(PauseSession(session_id=request.session_id))
            return ActionResponse(success=True)
        except ValueError as e:
            return ActionResponse(success=False, message=str(e))

    async def resume_session(self, request: ResumeSessionRequest) -> ActionResponse:
        try:
            await self._resume_session(ResumeSession(session_id=request.session_id))
            return ActionResponse(success=True)
        except ValueError as e:
            return ActionResponse(success=False, message=str(e))

    async def skip_block(self, request: SkipBlockRequest) -> ActionResponse:
        try:
            await self._skip_block(SkipBlock(session_id=request.session_id))
            return ActionResponse(success=True)
        except ValueError as e:
            return ActionResponse(success=False, message=str(e))
