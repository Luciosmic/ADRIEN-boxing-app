# Audio Service

## Purpose

Orchestrate audio functionality for the application, providing text-to-speech capabilities for announcements and notifications.

## Responsibilities

- Provide a high-level API for speaking text
- Manage audio configuration (enable/disable, voice selection)
- Abstract away infrastructure details (Kokoro TTS, console output, etc.)
- Handle errors gracefully with fallback behavior

## Architecture

- **Port**: `IAudioService` (defined in `application/ports`)
- **Service**: `AudioService` (orchestrates audio operations)
- **DTOs**: Request/Response objects for type safety
- **Infrastructure**: Concrete implementations (KokoroAudioService, ConsoleAudioService)

## Usage

The audio service is used by:

- `AnnouncementListener` to handle `AnnouncementTriggered` events
- UI components for direct audio feedback
- Any application component needing TTS functionality
