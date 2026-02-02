import pytest
import shutil
import os
import json
from uuid import uuid4
from src.domain.training.session import TrainingSession
from src.domain.training.workout import Workout
from src.domain.training.value_objects import Block, BlockType
from src.infrastructure.events.store.osu_event_store import OsuFileEventStore

@pytest.mark.anyio
async def test_domain_events_persisted_to_osu():
    # 1. Setup Environment
    test_dir = ".osu_integration_test"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    
    store = OsuFileEventStore(base_path=test_dir)
    
    # 2. Setup Domain
    workout = Workout(name="Integration Workout", id="w-int-1")
    # Short block: 2 seconds work
    block = Block(type=BlockType.WARMUP, work_time=2, rest_time=2, rounds=1)
    workout.add_block(block)
    
    session = TrainingSession(workout=workout, id=uuid4())
    
    # 3. Serialize and Persist Helper
    async def persist_events():
        events = session.collect_domain_events()
        if events:
            # In a real app, we'd read current version first. Here we assume 0 or append-only.
            # Using 0 as expected version for simplicity in this test loop (stateless append for log)
            await store.append(session.id, events, 0)
    
    # 4. Simulation
    
    # START
    session.start()
    await persist_events()
    
    # TICK 1 (Time 2 -> 1)
    session.tick()
    await persist_events()
    
    # TICK 2 (Time 1 -> 0 -> Phase Complete -> Rest Started)
    session.tick()
    await persist_events()
    
    # 5. Verification
    file_path = os.path.join(test_dir, f"{session.id}.jsonl")
    assert os.path.exists(file_path)
    
    with open(file_path, "r") as f:
        lines = [json.loads(line) for line in f.readlines()]
    
    # Print for debugging/viewing in output
    print("\nRecorded Events:")
    for l in lines:
        print(f"[{l['occurred_on']}] {l['event_type']}: {l['event_data']}")

    event_types = [l["event_type"] for l in lines]
    
    # Verify sequence
    # Start: SessionStarted, BlockStarted, RoundStarted
    assert "SessionStarted" in event_types
    assert "BlockStarted" in event_types
    assert "RoundStarted" in event_types
    
    # Ticks might trigger announcements if logic was complex, but here simplistic.
    # Rest transition: RestStarted
    assert "RestStarted" in event_types
    
    # Ensure data integrity
    round_started = next(l for l in lines if l["event_type"] == "RoundStarted")
    rs_data = json.loads(round_started["event_data"])
    assert rs_data["round_number"] == 1
    assert rs_data["duration"] == 2
    
    # Cleanup
    shutil.rmtree(test_dir)
