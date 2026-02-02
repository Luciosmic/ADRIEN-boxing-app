# Training Service Intention

## Purpose

The `TrainingService` orchestrates the core loop of the boxing application. It provides a simplified, high-level API for Agents and UI components to manage training sessions and workouts without interacting directly with granular Command Handlers or Domain Repositories.

## Responsibilities

- **Session Lifecycle**: Start, Pause, Resume, Tick (Heartbeat).
- **Workout Management**: Create and Retrieve workouts.
- **State exposure**: Provide read-only Session and Workout state DTOs.
- **Persistence**: Ensure all logic delegates to the underlying Infrastructure via CQRS handlers.

## Usage

Clients (e.g., Streamlit UI, CLI, or other Agents) should use `ITrainingService` to drive the application.
