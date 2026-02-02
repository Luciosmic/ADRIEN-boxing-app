from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class Command(BaseModel):
    """
    Base class for Commands.
    Commands represent an intent to change the system's state.
    """
    correlation_id: Optional[str] = None
    
    model_config = ConfigDict(frozen=True)


