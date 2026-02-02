import pytest
from src.domain.training.session import TrainingSession, SessionStatus
from src.domain.training.workout import Workout
from src.domain.training.value_objects import Block, BlockType

def test_session_start():
    workout = Workout(name="Test", id="w1")
    block = Block(type=BlockType.WARMUP, work_time=10, rest_time=5)
    workout.add_block(block)
    
    session = TrainingSession(workout=workout, id="s1")
    assert session.status == SessionStatus.IDLE
    
    session.start()
    assert session.status == SessionStatus.RUNNING
    assert session.current_block_index == 0
    assert session.time_left == 10
    
    events = session.collect_domain_events()
    assert any(e.__class__.__name__ == "SessionStarted" for e in events)
    assert any(e.__class__.__name__ == "BlockStarted" for e in events)
    assert any(e.__class__.__name__ == "RoundStarted" for e in events)

def test_session_tick_transition():
    workout = Workout(name="Test", id="w1")
    block = Block(type=BlockType.WARMUP, work_time=2, rest_time=2, rounds=2)
    workout.add_block(block)
    
    session = TrainingSession(workout=workout, id="s1")
    session.start()
    session.clear_domain_events()

    # Tick 1: 2 -> 1
    session.tick()
    assert session.time_left == 1
    
    # Tick 2: 1 -> 0 -> Phase Complete (Work -> Rest)
    session.tick() # time becomes 0, handle_phase_complete triggers
    # Logic in tick: decrement then check. 
    # tick() call 1: time 2->1.
    # tick() call 2: time 1->0. handle_phase_complete -> transitions to rest, sets time to rest_time (2)
    
    assert session.time_left == 2
    assert not session.is_work_phase
    
    events = session.collect_domain_events()
    assert any(e.__class__.__name__ == "RestStarted" for e in events)

def test_skip_block():
    workout = Workout(name="Test", id="w1")
    block1 = Block(type=BlockType.WARMUP)
    block2 = Block(type=BlockType.HEAVY_BAG)
    workout.add_block(block1)
    workout.add_block(block2)
    
    session = TrainingSession(workout=workout, id="s1")
    session.start()
    assert session.current_block_index == 0
    
    session.skip_block()
    assert session.current_block_index == 1
    # Check if BlockStarted event fired for second block
    events = session.collect_domain_events()
    block_starts = [e for e in events if e.__class__.__name__ == "BlockStarted"]
    assert len(block_starts) > 0
    assert block_starts[-1].block_type == BlockType.HEAVY_BAG
