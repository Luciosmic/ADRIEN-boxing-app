"""DTOs for coaching service requests."""
from pydantic import BaseModel
from src.domain.training.value_objects import BlockType, TechniqueCategory
from typing import List, Dict


class GetInstructionRequest(BaseModel):
    """Request to get a coaching instruction."""
    session_id: str
    block_type: BlockType
    time_left: int
    is_work_phase: bool
    language: str = "en"
    techniques: List[TechniqueCategory] | None = None
    exercises: Dict[str, int] | None = None
    
    class Config:
        frozen = True
