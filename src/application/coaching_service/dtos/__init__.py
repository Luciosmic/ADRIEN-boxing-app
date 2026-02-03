"""DTOs for coaching service."""
from .coaching_request_dtos import GetInstructionRequest
from .coaching_response_dtos import InstructionResponse, InstructionType

__all__ = [
    "GetInstructionRequest",
    "InstructionResponse",
    "InstructionType",
]
