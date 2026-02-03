"""Quick test to verify audio works with presenter."""
import asyncio
from src.composition_root import CompositionRoot
from src.application.training_service.dtos.training_request_dtos import CreateWorkoutRequest
from src.domain.training.value_objects import Block, BlockType

async def test_audio():
    print("Creating presenter with audio...")
    presenter = CompositionRoot.create_presenter(use_audio=True, language='fr')
    
    await presenter.initialize()
    
    # Start workout
    print("\nStarting workout...")
    await presenter.start_workout()
    
    # Tick a few times
    for i in range(10):
        print(f"\nTick {i+1}...")
        vm = await presenter.tick()
        print(f"  Time: {vm.time_display}")
        print(f"  Instruction: {vm.current_instruction}")
        await asyncio.sleep(1)
    
    print("\n✓ Test complete!")

if __name__ == "__main__":
    asyncio.run(test_audio())
