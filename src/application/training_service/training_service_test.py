import pytest
import shutil
import os
from src.application.training_service.training_service import TrainingService
from src.application.training_service.dtos.training_request_dtos import (
    CreateWorkoutRequest, StartSessionRequest, TickSessionRequest,
    GetSessionRequest, ListWorkoutsRequest
)
from src.domain.training.value_objects import Block, BlockType
from src.domain.training.session import SessionStatus

@pytest.mark.anyio
async def test_training_service_facade_flow():
    # 1. Setup
    test_root = ".osu_service_test"
    if os.path.exists(test_root):
        shutil.rmtree(test_root)
        
    service = TrainingService(base_path=test_root)
    
    # 2. Create Workout
    block = Block(type=BlockType.JUMP_ROPE, work_time=5)
    create_req = CreateWorkoutRequest(name="Service Workout", blocks=[block])
    create_resp = await service.create_workout(create_req)
    workout_id = create_resp.workout_id
    assert workout_id
    
    # 3. List Workouts
    list_resp = await service.list_workouts(ListWorkoutsRequest())
    assert len(list_resp) == 1
    assert list_resp[0].name == "Service Workout"
    
    # 4. Start Session
    start_req = StartSessionRequest(workout_id=workout_id)
    start_resp = await service.start_session(start_req)
    session_id = start_resp.session_id
    assert session_id
    
    # 5. Get Session State
    get_req = GetSessionRequest(session_id=session_id)
    state_resp = await service.get_session(get_req)
    assert state_resp.status == SessionStatus.RUNNING
    assert state_resp.time_left == 5
    
    # 6. Tick Session
    tick_req = TickSessionRequest(session_id=session_id)
    tick_resp = await service.tick_session(tick_req)
    assert tick_resp.success
    
    state_resp = await service.get_session(get_req)
    assert state_resp.time_left == 4
    
    # 7. Cleanup
    shutil.rmtree(test_root)
