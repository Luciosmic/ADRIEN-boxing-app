import pytest
from src.application.training_service.training_service import TrainingService
from src.infrastructure.training.repositories.in_memory_workout_repository import InMemoryWorkoutRepository
from src.infrastructure.training.repositories.in_memory_session_repository import InMemorySessionRepository
from src.infrastructure.events.store.in_memory_event_store import InMemoryEventStore
from src.application.training_service.dtos.training_request_dtos import CreateWorkoutRequest, StartSessionRequest, TickSessionRequest
from src.domain.training.value_objects import Block, BlockType

@pytest.mark.anyio
async def test_training_service_with_mocks():
    # 1. Setup Mocks
    workout_repo = InMemoryWorkoutRepository()
    event_store = InMemoryEventStore()
    session_repo = InMemorySessionRepository(event_store)

    # 2. Inject Mocks into Service
    service = TrainingService(
        workout_repo=workout_repo,
        session_repo=session_repo,
        event_store=event_store
    )

    # 3. Use Service API
    # Create Workout
    create_resp = await service.create_workout(CreateWorkoutRequest(
        name="Service Mock Workout", 
        blocks=[Block(type=BlockType.SHADOW_BOXING, work_time=5)]
    ))
    workout_id = create_resp.workout_id

    # Start Session
    start_resp = await service.start_session(StartSessionRequest(workout_id=workout_id))
    session_id = start_resp.session_id

    # Tick
    tick_resp = await service.tick_session(TickSessionRequest(session_id=session_id))
    assert tick_resp.success

    # Verify State directly in Repos (White box verification)
    session = await session_repo.get_by_id(session_id)
    assert session.time_left == 4
    
    # Verify Events
    events = await event_store.get(session.id)
    assert len(events) > 0
