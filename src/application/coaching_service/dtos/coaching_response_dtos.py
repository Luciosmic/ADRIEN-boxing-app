"""DTOs for coaching service responses."""
from pydantic import BaseModel
from enum import Enum


class InstructionType(str, Enum):
    """Type of instruction."""
    COUNTDOWN = "countdown"
    TECHNIQUE = "technique"
    REST = "rest"
    COACHING = "coaching"
    EXERCISE = "exercise"


class InstructionResponse(BaseModel):
    """Response containing a coaching instruction."""
    text: str
    type: InstructionType
    priority: int  # Higher = more important (for UI styling)
    
    class Config:
        frozen = True
