# Coaching Service

## Purpose

Generate contextual coaching instructions for training sessions based on session state, block type, and user preferences.

## Responsibilities

- Provide technique instructions (punches, kicks, combos)
- Generate countdown announcements (3, 2, 1)
- Suggest exercise variations (jump rope, strength)
- Manage instruction frequency to avoid spam
- Support multiple languages (fr, en, es)

## Architecture

- **Service**: `CoachingService` (orchestrates instruction generation)
- **DTOs**: Request/Response objects for type safety
- **Content**: Uses domain content (TECHNIQUES, EXERCISES)

## Usage

The coaching service is used by:

- `TrainingPresenter` to get instructions during session tick
- Any component needing contextual coaching guidance

## Instruction Types

- **COUNTDOWN**: High priority (3, 2, 1)
- **REST**: Rest phase announcements
- **TECHNIQUE**: Combat techniques (jab, cross, etc.)
- **EXERCISE**: Strength exercises with reps
- **COACHING**: General coaching cues

## Frequency Management

Instructions are rate-limited based on block type:

- Heavy Bag / Shadow Boxing: Every 5 seconds
- Jump Rope: Every 3 seconds
- Strength: Every 10 seconds
- Warmup: Every 7 seconds
