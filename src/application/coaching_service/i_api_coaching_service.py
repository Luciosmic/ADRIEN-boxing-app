"""
Coaching Service API Interface.
Defines the contract for coaching-related operations.
"""
from abc import ABC, abstractmethod
from src.application.coaching_service.dtos import (
    GetInstructionRequest,
    InstructionResponse
)


class IApiCoachingService(ABC):
    """
    High-level API for coaching operations.
    This service generates contextual instructions for training sessions.
    """
    
    @abstractmethod
    async def get_instruction(
        self, 
        request: GetInstructionRequest
    ) -> InstructionResponse:
        """
        Generate a coaching instruction based on session state.
        
        Args:
            request: GetInstructionRequest with session context
            
        Returns:
            InstructionResponse with instruction text and metadata
        """
        pass
