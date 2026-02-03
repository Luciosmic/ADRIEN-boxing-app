from abc import ABC, abstractmethod
from typing import List, Optional
from src.application.training_service.dtos.training_request_dtos import (
    CreateWorkoutRequest, StartSessionRequest, TickSessionRequest,
    PauseSessionRequest, ResumeSessionRequest, SkipBlockRequest,
    GetSessionRequest, ListWorkoutsRequest, GetWorkoutRequest,
    MoveBlockRequest
)
from src.application.training_service.dtos.training_response_dtos import (
    CreateWorkoutResponse, StartSessionResponse, ActionResponse,
    SessionStateResponse, WorkoutSummaryResponse, WorkoutDetailResponse
)

class ITrainingService(ABC):
    @abstractmethod
    async def create_workout(self, request: CreateWorkoutRequest) -> CreateWorkoutResponse:
        pass

    @abstractmethod
    async def list_workouts(self, request: ListWorkoutsRequest) -> List[WorkoutSummaryResponse]:
        pass

    @abstractmethod
    async def get_workout(self, request: GetWorkoutRequest) -> Optional[WorkoutDetailResponse]:
        pass

    @abstractmethod
    async def start_session(self, request: StartSessionRequest) -> StartSessionResponse:
        pass

    @abstractmethod
    async def get_session(self, request: GetSessionRequest) -> Optional[SessionStateResponse]:
        pass

    @abstractmethod
    async def tick_session(self, request: TickSessionRequest) -> ActionResponse:
        pass

    @abstractmethod
    async def pause_session(self, request: PauseSessionRequest) -> ActionResponse:
        pass

    @abstractmethod
    async def resume_session(self, request: ResumeSessionRequest) -> ActionResponse:
        pass

    @abstractmethod
    async def skip_block(self, request: SkipBlockRequest) -> ActionResponse:
        pass

    @abstractmethod
    async def move_block(self, request: MoveBlockRequest) -> ActionResponse:
        pass
