
import asyncio
import os
import shutil
from src.application.training_service.training_service import TrainingService
from src.interface.presenters.training_presenter import TrainingPresenter

async def verify():
    # Setup clean env
    test_path = ".osu_test_verify"
    if os.path.exists(test_path):
        shutil.rmtree(test_path)
        
    print("Initializing Service & Presenter...")
    service = TrainingService(base_path=test_path)
    presenter = TrainingPresenter(service)
    
    await presenter.initialize()
    print(f"Initialized. Workouts found: {len(presenter.workouts_summary)}")
    
    if not presenter.workouts_summary:
        print("ERROR: No workouts seeded")
        return

    workout_id = presenter.workouts_summary[0].id
    await presenter.select_workout(workout_id)
    
    blocks = presenter._cached_workout_detail.blocks
    print(f"Original Blocks: {[b.type for b in blocks]}")
    
    # Move index 1 (JumpRope) to index 0 (Warmup) -> Swap
    print("Moving block at index 1 to index 0...")
    await presenter.move_block(from_index=1, to_index=0)
    
    blocks_after = presenter._cached_workout_detail.blocks
    print(f"Blocks after move: {[b.type for b in blocks_after]}")
    
    if blocks_after[0].type == "jumpRope":
        print("SUCCESS: Block moved correctly")
    else:
        print("FAILURE: Block did not move")

    # Cleanup
    if os.path.exists(test_path):
        shutil.rmtree(test_path)

if __name__ == "__main__":
    asyncio.run(verify())
