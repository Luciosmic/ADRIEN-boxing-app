import pytest
from uuid import uuid4

# Mocks
from src.infrastructure.training.repositories.in_memory_workout_repository import InMemoryWorkoutRepository
from src.infrastructure.training.repositories.in_memory_session_repository import InMemorySessionRepository
from src.infrastructure.events.store.in_memory_event_store import InMemoryEventStore

# Commands
from src.application.training.commands.workout_commands import CreateWorkout, CreateWorkoutHandler
from src.application.training.commands.session_commands import (
    StartSession, StartSessionHandler, 
    TickSession, TickSessionHandler,
    SkipBlock, SkipBlockHandler
)
# Queries
from src.application.training.queries.session_queries import GetSession, GetSessionHandler

from src.domain.training.value_objects import Block, BlockType
from src.domain.training.session import SessionStatus

@pytest.mark.anyio
async def test_commands_with_mocks():
    # 1. Setup Mocks
    workout_repo = InMemoryWorkoutRepository()
    event_store = InMemoryEventStore()
    session_repo = InMemorySessionRepository(event_store)

    # 2. Setup Handlers
    create_workout = CreateWorkoutHandler(workout_repo)
    start_session = StartSessionHandler(session_repo, workout_repo)
    tick_session = TickSessionHandler(session_repo)
    skip_block = SkipBlockHandler(session_repo)
    get_session = GetSessionHandler(session_repo)

    # 3. Create Workout
    block1 = Block(type=BlockType.JUMP_ROPE, work_time=10)
    workout_cmd = CreateWorkout(name="Mock Workout", blocks=[block1])
    workout_id = await create_workout(workout_cmd)
    
    assert workout_id is not None
    # Verify mock state
    stored_workout = await workout_repo.get_by_id(workout_id)
    assert stored_workout.name == "Mock Workout"

    # 4. Start Session
    session_id = str(uuid4())
    await start_session(StartSession(session_id=session_id, workout_id=workout_id))
    
    # Verify session in mock repo
    stored_session = await session_repo.get_by_id(session_id)
    assert stored_session is not None
    assert stored_session.status == SessionStatus.RUNNING
    assert stored_session.time_left == 10

    # 5. Tick Session
    await tick_session(TickSession(session_id=session_id))
    
    stored_session = await session_repo.get_by_id(session_id)
    assert stored_session.time_left == 9
    
    # 6. Skip Block
    await skip_block(SkipBlock(session_id=session_id))
    stored_session = await session_repo.get_by_id(session_id)
    # Since only 1 block, session should complete? 
    # Logic in session: skip_block -> completes current block -> next block. If no next block -> Completed.
    # Wait, skip_block behavior might depend on implementation details.
    
    # Let's check status via Query
    s_dto = await get_session(GetSession(session_id=session_id))
    assert s_dto.status == SessionStatus.COMPLETED

    # 7. Check Events in Mock Store
    events = await event_store.get(stored_session.id)
    assert len(events) > 0
    # Should have SessionStarted, BlockStarted, SessionCompleted etc.
