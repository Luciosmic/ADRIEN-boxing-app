from enum import Enum
from typing import List, Dict, Optional, Literal
from pydantic import BaseModel, Field
import uuid

class BlockType(str, Enum):
    WARMUP = "warmup"
    JUMP_ROPE = "jumpRope"
    SHADOW_BOXING = "shadowBoxing"
    HEAVY_BAG = "heavyBag"
    SPARRING = "sparring"
    STRENGTH = "strength"
    COOLDOWN = "cooldown"

class Frequency(str, Enum):
    SLOW = "slow"
    NORMAL = "normal"
    FAST = "fast"

class Sport(str, Enum):
    MUAY_THAI = "muayThai"
    KARATE_WKF = "karateWKF"
    BOXING = "boxing"
    FULL_CONTACT = "fullContact"
    KICKBOXING = "kickboxing"

class VoiceProfile(str, Enum):
    DEFAULT = "default"
    GANDALF = "gandalf"
    DUMBLEDORE = "dumbledore"
    APOLLO_CREED = "apolloCreed"
    ROCKY = "rocky"

# Using string literals for techniques and exercises for flexibility, 
# but could be Enums if strictness is required.
class TechniqueCategory(str, Enum):
    PUNCHES = "punches"
    KICKS = "kicks"
    KNEES = "knees"
    ELBOWS = "elbows"
    COMBOS = "combos"

class ExerciseType(str, Enum):
    PLANK = "plank"
    ABS = "abs"
    PUSHUPS = "pushups"
    BURPEES = "burpees"
    SQUATS = "squats"
    JUMPING_JACKS = "jumpingJacks"

class Block(BaseModel):
    """
    Represents a configurable segment of a workout.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: BlockType
    rounds: int = 1
    work_time: int = 60 # seconds
    rest_time: int = 30 # seconds
    
    # Optional fields depending on BlockType
    frequency: Frequency = Frequency.NORMAL
    techniques: List[TechniqueCategory] = Field(default_factory=list)
    exercises: Dict[str, int] = Field(default_factory=dict) # ExerciseType -> reps
    sport: Optional[Sport] = None

    class Config:
        use_enum_values = True
