"""
Test the complete integration chain:
Presenter -> Service -> Commands -> Repository -> EventStore
"""
import asyncio
import os
import shutil
from src.composition_root import CompositionRoot

async def test_complete_chain():
    # Clean test environment
    test_path = ".osu_integration_test"
    if os.path.exists(test_path):
        shutil.rmtree(test_path)
    
    print("=" * 60)
    print("INTEGRATION TEST - Complete Chain")
    print("=" * 60)
    
    # 1. Create presenter via composition root
    print("\n1. Creating presenter via CompositionRoot...")
    presenter = CompositionRoot.create_presenter(
        language='fr',
        base_path=test_path,
        use_audio=False  # Disable audio for test
    )
    
    # 2. Initialize (seed workouts)
    print("2. Initializing (seeding workouts)...")
    await presenter.initialize()
    print(f"   ✓ Workouts seeded: {len(presenter.workouts_summary)}")
    
    # 3. Get initial view model
    print("\n3. Getting initial view model...")
    vm = presenter.get_current_view_model()
    print(f"   Time: {vm.time_display}")
    print(f"   Status: {vm.status_text}")
    print(f"   Running: {vm.is_running}")
    
    # 4. Start workout
    print("\n4. Starting workout...")
    await presenter.start_workout()
    print("   ✓ Workout started")
    
    # 5. Get view model after start
    print("\n5. Getting view model after start...")
    vm = await presenter.tick()
    print(f"   Time: {vm.time_display}")
    print(f"   Status: {vm.status_text}")
    print(f"   Running: {vm.is_running}")
    print(f"   Block: {vm.current_block_name}")
    print(f"   Instruction: {vm.current_instruction}")
    
    # 6. Tick a few times
    print("\n6. Ticking 5 times...")
    for i in range(5):
        await asyncio.sleep(0.1)  # Small delay
        vm = await presenter.tick()
        print(f"   Tick {i+1}: {vm.time_display} - {vm.current_instruction}")
    
    # 7. Pause
    print("\n7. Pausing...")
    await presenter.pause_workout()
    vm = presenter.get_current_view_model()
    print(f"   Running: {vm.is_running}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    
    # Cleanup
    if os.path.exists(test_path):
        shutil.rmtree(test_path)

if __name__ == "__main__":
    asyncio.run(test_complete_chain())
