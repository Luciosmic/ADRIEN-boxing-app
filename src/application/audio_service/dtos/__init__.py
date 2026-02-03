"""DTOs for audio service."""
from .audio_request_dtos import SpeakRequest, ConfigureAudioRequest
from .audio_response_dtos import SpeakResponse, AudioStatusResponse

__all__ = [
    "SpeakRequest",
    "ConfigureAudioRequest",
    "SpeakResponse",
    "AudioStatusResponse",
]
