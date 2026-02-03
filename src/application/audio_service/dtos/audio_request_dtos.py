"""DTOs for audio service requests."""
from pydantic import BaseModel


class SpeakRequest(BaseModel):
    """Request to speak text via audio synthesis."""
    text: str
    language: str = "en"
    
    class Config:
        frozen = True


class ConfigureAudioRequest(BaseModel):
    """Request to configure audio settings."""
    voice: str | None = None
    speed: float = 1.0
    enabled: bool = True
    
    class Config:
        frozen = True
