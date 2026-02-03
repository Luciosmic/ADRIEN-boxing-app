"""E2E tests for TrainingService API."""
import pytest
import shutil
import os
from src.application.training_service.training_service import TrainingService
from src.application.training_service.dtos.training_request_dtos import (
    CreateWorkoutRequest, StartSessionRequest, TickSessionRequest,
    GetSessionRequest, ListWorkoutsRequest, PauseSessionRequest,
    ResumeSessionRequest, MoveBlockRequest, GetWorkoutRequest
)
from src.domain.training.value_objects import Block, BlockType, TechniqueCategory
from src.domain.training.session import SessionStatus


@pytest.mark.anyio
class TestTrainingServiceE2E:
    """End-to-end tests for TrainingService using the API interface."""
    
    @pytest.fixture
    async def service(self):
        """Create a TrainingService instance for testing."""
        test_root = ".osu_e2e_test"
        if os.path.exists(test_root):
            shutil.rmtree(test_root)
        
        service = TrainingService(base_path=test_root, event_bus=None)
        yield service
        
        # Cleanup
        if os.path.exists(test_root):
            shutil.rmtree(test_root)
    
    async def test_create_and_list_workouts(self, service):
        """Test creating and listing workouts."""
        # Create workout
        block = Block(type=BlockType.JUMP_ROPE, work_time=60, rest_time=30, rounds=3)
        create_req = CreateWorkoutRequest(name="Jump Rope Workout", blocks=[block])
        create_resp = await service.create_workout(create_req)
        
        assert create_resp.workout_id is not None
        
        # List workouts
        list_resp = await service.list_workouts(ListWorkoutsRequest())
        assert len(list_resp) == 1
        assert list_resp[0].name == "Jump Rope Workout"
        assert list_resp[0].id == create_resp.workout_id
    
    async def test_get_workout_details(self, service):
        """Test retrieving workout details."""
        # Create workout
        blocks = [
            Block(type=BlockType.WARMUP, work_time=300),
            Block(type=BlockType.HEAVY_BAG, work_time=180, rest_time=60, rounds=5),
            Block(type=BlockType.COOLDOWN, work_time=300)
        ]
        create_req = CreateWorkoutRequest(name="Full Workout", blocks=blocks)
        create_resp = await service.create_workout(create_req)
        
        # Get workout details
        get_req = GetWorkoutRequest(workout_id=create_resp.workout_id)
        workout = await service.get_workout(get_req)
        
        assert workout.id == create_resp.workout_id
        assert workout.name == "Full Workout"
        assert len(workout.blocks) == 3
        assert workout.blocks[0].type == BlockType.WARMUP
        assert workout.blocks[1].type == BlockType.HEAVY_BAG
        assert workout.blocks[2].type == BlockType.COOLDOWN
    
    async def test_session_lifecycle(self, service):
        """Test complete session lifecycle: start, tick, pause, resume, complete."""
        # Create workout
        block = Block(type=BlockType.JUMP_ROPE, work_time=5, rest_time=3, rounds=2)
        create_req = CreateWorkoutRequest(name="Quick Workout", blocks=[block])
        create_resp = await service.create_workout(create_req)
        
        # Start session
        start_req = StartSessionRequest(
            session_id="test-session",
            workout_id=create_resp.workout_id
        )
        start_resp = await service.start_session(start_req)
        assert start_resp.session_id == "test-session"
        
        # Get initial state
        get_req = GetSessionRequest(session_id="test-session")
        state = await service.get_session(get_req)
        assert state.status == SessionStatus.RUNNING
        assert state.time_left == 5
        assert state.is_work_phase is True
        assert state.current_round == 1
        
        # Tick session
        tick_req = TickSessionRequest(session_id="test-session")
        for _ in range(3):
            tick_resp = await service.tick_session(tick_req)
            assert tick_resp.success is True
        
        state = await service.get_session(get_req)
        assert state.time_left == 2
        
        # Pause session
        pause_req = PauseSessionRequest(session_id="test-session")
        pause_resp = await service.pause_session(pause_req)
        assert pause_resp.success is True
        
        state = await service.get_session(get_req)
        assert state.status == SessionStatus.PAUSED
        
        # Resume session
        resume_req = ResumeSessionRequest(session_id="test-session")
        resume_resp = await service.resume_session(resume_req)
        assert resume_resp.success is True
        
        state = await service.get_session(get_req)
        assert state.status == SessionStatus.RUNNING
    
    async def test_session_work_rest_transition(self, service):
        """Test transition from work to rest phase."""
        # Create workout with short times
        block = Block(type=BlockType.HEAVY_BAG, work_time=3, rest_time=2, rounds=2)
        create_req = CreateWorkoutRequest(name="Transition Test", blocks=[block])
        create_resp = await service.create_workout(create_req)
        
        # Start session
        start_req = StartSessionRequest(
            session_id="transition-session",
            workout_id=create_resp.workout_id
        )
        await service.start_session(start_req)
        
        get_req = GetSessionRequest(session_id="transition-session")
        tick_req = TickSessionRequest(session_id="transition-session")
        
        # Tick through work phase
        for _ in range(3):
            await service.tick_session(tick_req)
        
        # Should now be in rest phase
        state = await service.get_session(get_req)
        assert state.is_work_phase is False
        assert state.time_left == 2
        assert state.current_round == 1
        
        # Tick through rest phase
        for _ in range(2):
            await service.tick_session(tick_req)
        
        # Should be in round 2, work phase
        state = await service.get_session(get_req)
        assert state.is_work_phase is True
        assert state.current_round == 2
        assert state.time_left == 3
    
    async def test_move_block(self, service):
        """Test moving blocks within a workout."""
        # Create workout with multiple blocks
        blocks = [
            Block(type=BlockType.WARMUP, work_time=300),
            Block(type=BlockType.JUMP_ROPE, work_time=180),
            Block(type=BlockType.HEAVY_BAG, work_time=180),
            Block(type=BlockType.COOLDOWN, work_time=300)
        ]
        create_req = CreateWorkoutRequest(name="Reorder Test", blocks=blocks)
        create_resp = await service.create_workout(create_req)
        
        # Move JUMP_ROPE (index 1) to position 2
        move_req = MoveBlockRequest(
            workout_id=create_resp.workout_id,
            from_index=1,
            to_index=2
        )
        move_resp = await service.move_block(move_req)
        assert move_resp.success is True
        
        # Verify new order
        get_req = GetWorkoutRequest(workout_id=create_resp.workout_id)
        workout = await service.get_workout(get_req)
        
        assert workout.blocks[0].type == BlockType.WARMUP
        assert workout.blocks[1].type == BlockType.HEAVY_BAG
        assert workout.blocks[2].type == BlockType.JUMP_ROPE
        assert workout.blocks[3].type == BlockType.COOLDOWN
    
    async def test_multiple_workouts(self, service):
        """Test managing multiple workouts."""
        # Create multiple workouts
        workout1 = CreateWorkoutRequest(
            name="Beginner",
            blocks=[Block(type=BlockType.JUMP_ROPE, work_time=60)]
        )
        workout2 = CreateWorkoutRequest(
            name="Advanced",
            blocks=[Block(type=BlockType.HEAVY_BAG, work_time=180, rounds=5)]
        )
        workout3 = CreateWorkoutRequest(
            name="Strength",
            blocks=[Block(type=BlockType.STRENGTH, work_time=120)]
        )
        
        resp1 = await service.create_workout(workout1)
        resp2 = await service.create_workout(workout2)
        resp3 = await service.create_workout(workout3)
        
        # List all workouts
        list_resp = await service.list_workouts(ListWorkoutsRequest())
        assert len(list_resp) == 3
        
        names = {w.name for w in list_resp}
        assert names == {"Beginner", "Advanced", "Strength"}
    
    async def test_session_completion(self, service):
        """Test session completes after all blocks."""
        # Create workout with single short block
        block = Block(type=BlockType.JUMP_ROPE, work_time=2, rest_time=1, rounds=1)
        create_req = CreateWorkoutRequest(name="Complete Test", blocks=[block])
        create_resp = await service.create_workout(create_req)
        
        # Start session
        start_req = StartSessionRequest(
            session_id="complete-session",
            workout_id=create_resp.workout_id
        )
        await service.start_session(start_req)
        
        # Tick through entire workout
        tick_req = TickSessionRequest(session_id="complete-session")
        get_req = GetSessionRequest(session_id="complete-session")
        
        # Work phase (2 seconds)
        for _ in range(2):
            await service.tick_session(tick_req)
        
        # Rest phase (1 second)
        await service.tick_session(tick_req)
        
        # Should be completed
        state = await service.get_session(get_req)
        assert state.status == SessionStatus.COMPLETED
    
    async def test_concurrent_sessions(self, service):
        """Test multiple concurrent sessions."""
        # Create workout
        block = Block(type=BlockType.HEAVY_BAG, work_time=60)
        create_req = CreateWorkoutRequest(name="Concurrent Test", blocks=[block])
        create_resp = await service.create_workout(create_req)
        
        # Start two sessions
        await service.start_session(StartSessionRequest(
            session_id="session-1",
            workout_id=create_resp.workout_id
        ))
        await service.start_session(StartSessionRequest(
            session_id="session-2",
            workout_id=create_resp.workout_id
        ))
        
        # Tick session 1
        await service.tick_session(TickSessionRequest(session_id="session-1"))
        await service.tick_session(TickSessionRequest(session_id="session-1"))
        
        # Verify states are independent
        state1 = await service.get_session(GetSessionRequest(session_id="session-1"))
        state2 = await service.get_session(GetSessionRequest(session_id="session-2"))
        
        assert state1.time_left == 58
        assert state2.time_left == 60
