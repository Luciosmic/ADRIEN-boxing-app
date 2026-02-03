"""E2E tests for CoachingService API."""
import pytest
from src.application.coaching_service.coaching_service import CoachingService
from src.application.coaching_service.dtos import (
    GetInstructionRequest,
    InstructionResponse,
    InstructionType
)
from src.domain.training.value_objects import BlockType, TechniqueCategory


@pytest.mark.anyio
class TestCoachingServiceE2E:
    """End-to-end tests for CoachingService using the API interface."""
    
    async def test_countdown_instruction(self):
        """Test countdown instructions (highest priority)."""
        # Arrange
        service = CoachingService()
        
        # Act & Assert - Test countdown 3, 2, 1
        for time_left in [3, 2, 1]:
            request = GetInstructionRequest(
                session_id="test-session",
                block_type=BlockType.HEAVY_BAG,
                time_left=time_left,
                is_work_phase=True,
                language="en"
            )
            response = await service.get_instruction(request)
            
            assert isinstance(response, InstructionResponse)
            assert response.text == str(time_left)
            assert response.type == InstructionType.COUNTDOWN
            assert response.priority == 10
    
    async def test_rest_instruction(self):
        """Test rest phase instructions."""
        # Arrange
        service = CoachingService()
        
        # Test French
        fr_request = GetInstructionRequest(
            session_id="test-session",
            block_type=BlockType.HEAVY_BAG,
            time_left=30,
            is_work_phase=False,
            language="fr"
        )
        fr_response = await service.get_instruction(fr_request)
        assert fr_response.text == "Repos"
        assert fr_response.type == InstructionType.REST
        assert fr_response.priority == 5
        
        # Test English
        en_request = GetInstructionRequest(
            session_id="test-session",
            block_type=BlockType.HEAVY_BAG,
            time_left=30,
            is_work_phase=False,
            language="en"
        )
        en_response = await service.get_instruction(en_request)
        assert en_response.text == "Rest"
        assert en_response.type == InstructionType.REST
        
        # Test Spanish
        es_request = GetInstructionRequest(
            session_id="test-session",
            block_type=BlockType.HEAVY_BAG,
            time_left=30,
            is_work_phase=False,
            language="es"
        )
        es_response = await service.get_instruction(es_request)
        assert es_response.text == "Descanso"
        assert es_response.type == InstructionType.REST
    
    async def test_technique_instruction_heavy_bag(self):
        """Test technique instructions for heavy bag."""
        # Arrange
        service = CoachingService()
        request = GetInstructionRequest(
            session_id="test-session",
            block_type=BlockType.HEAVY_BAG,
            time_left=60,
            is_work_phase=True,
            language="en",
            techniques=[TechniqueCategory.PUNCHES, TechniqueCategory.KICKS]
        )
        
        # Act
        response = await service.get_instruction(request)
        
        # Assert
        assert isinstance(response, InstructionResponse)
        assert response.text != ""  # Should have a technique
        assert response.type == InstructionType.TECHNIQUE
        assert response.priority == 3
    
    async def test_technique_instruction_shadow_boxing(self):
        """Test technique instructions for shadow boxing."""
        # Arrange
        service = CoachingService()
        request = GetInstructionRequest(
            session_id="test-session",
            block_type=BlockType.SHADOW_BOXING,
            time_left=90,
            is_work_phase=True,
            language="fr",
            techniques=[TechniqueCategory.COMBOS]
        )
        
        # Act
        response = await service.get_instruction(request)
        
        # Assert
        assert isinstance(response, InstructionResponse)
        assert response.text != ""
        assert response.type == InstructionType.TECHNIQUE
    
    async def test_jump_rope_instruction(self):
        """Test jump rope variation instructions."""
        # Arrange
        service = CoachingService()
        request = GetInstructionRequest(
            session_id="test-session",
            block_type=BlockType.JUMP_ROPE,
            time_left=120,
            is_work_phase=True,
            language="fr"
        )
        
        # Act
        response = await service.get_instruction(request)
        
        # Assert
        assert isinstance(response, InstructionResponse)
        assert response.text in ["Sauts simples", "Sauts alternés", "Double saut", "Croisés"]
        assert response.type == InstructionType.COACHING
        assert response.priority == 3
    
    async def test_strength_instruction(self):
        """Test strength exercise instructions."""
        # Arrange
        service = CoachingService()
        exercises = {"Push-ups": 20, "Squats": 30}
        request = GetInstructionRequest(
            session_id="test-session",
            block_type=BlockType.STRENGTH,
            time_left=60,
            is_work_phase=True,
            language="en",
            exercises=exercises
        )
        
        # Act
        response = await service.get_instruction(request)
        
        # Assert
        assert isinstance(response, InstructionResponse)
        assert "Push-ups" in response.text or "Squats" in response.text
        assert "reps" in response.text
        assert response.type == InstructionType.EXERCISE
        assert response.priority == 3
    
    async def test_frequency_management(self):
        """Test that instructions respect frequency limits."""
        # Arrange
        service = CoachingService()
        session_id = "frequency-test"
        
        # First instruction
        request1 = GetInstructionRequest(
            session_id=session_id,
            block_type=BlockType.HEAVY_BAG,
            time_left=60,
            is_work_phase=True,
            language="en",
            techniques=[TechniqueCategory.PUNCHES]
        )
        response1 = await service.get_instruction(request1)
        assert response1.text != ""
        
        # Immediate second request (should be empty due to frequency limit)
        request2 = GetInstructionRequest(
            session_id=session_id,
            block_type=BlockType.HEAVY_BAG,
            time_left=59,
            is_work_phase=True,
            language="en",
            techniques=[TechniqueCategory.PUNCHES]
        )
        response2 = await service.get_instruction(request2)
        assert response2.text == ""  # Too soon
        assert response2.priority == 0
    
    async def test_multiple_sessions(self):
        """Test that different sessions are tracked independently."""
        # Arrange
        service = CoachingService()
        
        # Session 1
        request1 = GetInstructionRequest(
            session_id="session-1",
            block_type=BlockType.HEAVY_BAG,
            time_left=60,
            is_work_phase=True,
            language="en"
        )
        response1 = await service.get_instruction(request1)
        assert response1.text != ""
        
        # Session 2 (different session, should get instruction)
        request2 = GetInstructionRequest(
            session_id="session-2",
            block_type=BlockType.HEAVY_BAG,
            time_left=60,
            is_work_phase=True,
            language="en"
        )
        response2 = await service.get_instruction(request2)
        assert response2.text != ""
    
    async def test_no_techniques_provided(self):
        """Test instruction generation when no specific techniques are provided."""
        # Arrange
        service = CoachingService()
        request = GetInstructionRequest(
            session_id="test-session",
            block_type=BlockType.WARMUP,
            time_left=120,
            is_work_phase=True,
            language="en",
            techniques=None  # No specific techniques
        )
        
        # Act
        response = await service.get_instruction(request)
        
        # Assert
        assert isinstance(response, InstructionResponse)
        # Should still get a technique from all available
        assert response.type == InstructionType.TECHNIQUE
    
    async def test_cooldown_block(self):
        """Test instructions for cooldown block."""
        # Arrange
        service = CoachingService()
        request = GetInstructionRequest(
            session_id="test-session",
            block_type=BlockType.COOLDOWN,
            time_left=180,
            is_work_phase=True,
            language="en"
        )
        
        # Act
        response = await service.get_instruction(request)
        
        # Assert
        assert isinstance(response, InstructionResponse)
        # Cooldown has low frequency, might be empty initially
        assert response.priority in [0, 1]
