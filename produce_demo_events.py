import asyncio
import os
from uuid import uuid4
from src.domain.training.session import TrainingSession
from src.domain.training.workout import Workout
from src.domain.training.value_objects import Block, BlockType
from src.infrastructure.events.store.osu_event_store import OsuFileEventStore

async def main():
    # Use the real .osu directory
    store = OsuFileEventStore(base_path=".osu")
    
    print("Creating Demo Workout...")
    workout = Workout(name="Demo Workout", id="demo-workout-1")
    block = Block(type=BlockType.JUMP_ROPE, work_time=5, rest_time=2, rounds=1)
    workout.add_block(block)
    
    session_id = uuid4()
    session = TrainingSession(workout=workout, id=session_id)
    print(f"Starting Session {session_id}...")
    
    # Helper to persist
    async def persist():
        events = session.collect_domain_events()
        if events:
            print(f"Persisting {len(events)} events...")
            await store.append(session.id, events, 0)

    session.start()
    await persist()
    
    # Simulate a few ticks
    for i in range(7):
        session.tick()
        await persist()
        
    print(f"\nDone! Events saved to .osu/{session_id}.jsonl")

if __name__ == "__main__":
    asyncio.run(main())
