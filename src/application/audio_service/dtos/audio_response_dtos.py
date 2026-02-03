"""DTOs for audio service responses."""
from pydantic import BaseModel


class SpeakResponse(BaseModel):
    """Response after speaking text."""
    success: bool
    message: str | None = None
    
    class Config:
        frozen = True


class AudioStatusResponse(BaseModel):
    """Current status of the audio service."""
    enabled: bool
    provider: str  # e.g., "kokoro", "console", "none"
    voice: str | None = None
    
    class Config:
        frozen = True
