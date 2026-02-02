
from src.interface.presenters.mock_presenter import MockPresenter
from src.interface.presenters.base import WorkoutViewModel

def verify():
    print("Initializing MockPresenter...")
    presenter = MockPresenter(language='en')
    
    vm = presenter.get_current_view_model()
    print(f"Initial State: Time={vm.time_display}, Status={vm.status_text}, Block={vm.current_block_name}")
    
    # Test Start
    print("Starting workout...")
    presenter.start_workout()
    
    # Test Tick
    print("Ticking...")
    presenter.tick()
    vm = presenter.get_current_view_model()
    print(f"After 1 tick: Time={vm.time_display}, Running={vm.is_running}")
    
    if not vm.is_running:
        print("ERROR: Should be running")
        return

    # Simulate 5 ticks to trigger instruction change
    for _ in range(5):
        presenter.tick()
    
    vm = presenter.get_current_view_model()
    print(f"After 6 ticks: Instruction={vm.current_instruction}")
    
    print("MVP Verification Successful")

if __name__ == "__main__":
    verify()
