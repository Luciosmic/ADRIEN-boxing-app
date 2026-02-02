import pytest
import shutil
import os
from uuid import uuid4

# Repositories
from src.infrastructure.training.repositories.osu_workout_repository import OsuWorkoutRepository
from src.infrastructure.training.repositories.osu_session_repository import OsuSessionRepository
from src.infrastructure.events.store.osu_event_store import OsuFileEventStore

# Commands & Queries
from src.application.training.commands.workout_commands import CreateWorkout, CreateWorkoutHandler
from src.application.training.commands.session_commands import (
    StartSession, StartSessionHandler, 
    TickSession, TickSessionHandler,
    SkipBlock, SkipBlockHandler,
    PauseSession, PauseSessionHandler
)
from src.application.training.queries.session_queries import GetSession, GetSessionHandler, SessionStatus
from src.application.training.queries.workout_queries import GetWorkout, GetWorkoutHandler

from src.domain.training.value_objects import Block, BlockType

@pytest.mark.anyio
async def test_training_application_flow():
    # 1. Setup Infrastructure
    test_root = ".osu_app_test"
    if os.path.exists(test_root):
        shutil.rmtree(test_root)
        
    workout_repo = OsuWorkoutRepository(base_path=os.path.join(test_root, "workouts"))
    event_store = OsuFileEventStore(base_path=os.path.join(test_root, "events"))
    session_repo = OsuSessionRepository(event_store=event_store, base_path=os.path.join(test_root, "sessions"))
    
    # 2. Wire Handlers
    create_workout = CreateWorkoutHandler(workout_repo)
    start_session = StartSessionHandler(session_repo, workout_repo)
    tick_session = TickSessionHandler(session_repo)
    skip_block = SkipBlockHandler(session_repo)
    pause_session = PauseSessionHandler(session_repo)
    get_session = GetSessionHandler(session_repo)
    get_workout = GetWorkoutHandler(workout_repo)
    
    # 3. Create Workout
    block1 = Block(type=BlockType.JUMP_ROPE, work_time=5, rest_time=2)
    block2 = Block(type=BlockType.SHADOW_BOXING, work_time=5)
    
    workout_cmd = CreateWorkout(name="App Test Workout", blocks=[block1, block2])
    workout_id = await create_workout(workout_cmd)
    
    # Verify Workout Created
    w_dto = await get_workout(GetWorkout(workout_id=workout_id))
    assert w_dto.name == "App Test Workout"
    assert len(w_dto.blocks) == 2
    
    # 4. Start Session
    session_id = str(uuid4())
    await start_session(StartSession(session_id=session_id, workout_id=workout_id))
    
    # Verify Session Started
    s_dto = await get_session(GetSession(session_id=session_id))
    assert s_dto.status == SessionStatus.RUNNING
    assert s_dto.current_block_index == 0
    assert s_dto.time_left == 5
    
    # 5. Tick Loop (Simulate 3 seconds)
    await tick_session(TickSession(session_id=session_id)) # 5 -> 4
    await tick_session(TickSession(session_id=session_id)) # 4 -> 3
    await tick_session(TickSession(session_id=session_id)) # 3 -> 2
    
    s_dto = await get_session(GetSession(session_id=session_id))
    assert s_dto.time_left == 2
    
    # 6. Skip Block
    await skip_block(SkipBlock(session_id=session_id))
    
    s_dto = await get_session(GetSession(session_id=session_id))
    assert s_dto.current_block_index == 1
    assert s_dto.time_left == 5 # Start of next block
    
    # 7. Pause
    await pause_session(PauseSession(session_id=session_id))
    s_dto = await get_session(GetSession(session_id=session_id))
    assert s_dto.status == SessionStatus.PAUSED
    
    # 8. Verify Persistence Files Exist
    assert os.path.exists(os.path.join(test_root, "workouts", f"{workout_id}.json"))
    assert os.path.exists(os.path.join(test_root, "sessions", f"{session_id}.json"))
    assert os.path.exists(os.path.join(test_root, "events", f"{session_id}.jsonl"))
    
    # Cleanup
    shutil.rmtree(test_root)
