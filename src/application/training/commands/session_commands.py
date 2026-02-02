from uuid import UUID
from pydantic import Field
from src.application._base.command import Command
from src.domain.training.repositories import ISessionRepository, IWorkoutRepository
from src.domain.training.session import TrainingSession

# --- Commands ---

class StartSession(Command):
    session_id: str
    workout_id: str

class TickSession(Command):
    session_id: str

class PauseSession(Command):
    session_id: str

class ResumeSession(Command):
    session_id: str

class SkipRound(Command):
    session_id: str

class SkipBlock(Command):
    session_id: str


# --- Handlers ---

class StartSessionHandler:
    def __init__(self, session_repo: ISessionRepository, workout_repo: IWorkoutRepository):
        self.session_repo = session_repo
        self.workout_repo = workout_repo

    async def __call__(self, command: StartSession) -> None:
        # Check if session already exists? (Idempotency)
        existing = await self.session_repo.get_by_id(command.session_id)
        if existing:
            return # Or raise error
        
        workout = await self.workout_repo.get_by_id(command.workout_id)
        if not workout:
            raise ValueError(f"Workout {command.workout_id} not found")

        session = TrainingSession(workout=workout, id=command.session_id)
        session.start()
        
        await self.session_repo.save(session)


class TickSessionHandler:
    def __init__(self, session_repo: ISessionRepository):
        self.session_repo = session_repo

    async def __call__(self, command: TickSession) -> None:
        session = await self.session_repo.get_by_id(command.session_id)
        if not session:
             # If session not found, maybe it finished or invalid ID. Silent fail or error?
             # For a "Tick" loop, error might spam. But strict logic says error.
             raise ValueError(f"Session {command.session_id} not found")
        
        session.tick()
        await self.session_repo.save(session)


class PauseSessionHandler:
    def __init__(self, session_repo: ISessionRepository):
        self.session_repo = session_repo

    async def __call__(self, command: PauseSession) -> None:
        session = await self.session_repo.get_by_id(command.session_id)
        if not session:
            raise ValueError(f"Session {command.session_id} not found")
        
        session.pause()
        await self.session_repo.save(session)


class ResumeSessionHandler:
    def __init__(self, session_repo: ISessionRepository):
        self.session_repo = session_repo

    async def __call__(self, command: ResumeSession) -> None:
        session = await self.session_repo.get_by_id(command.session_id)
        if not session:
            raise ValueError(f"Session {command.session_id} not found")
        
        session.start() # Resume is same as start in our state machine if paused
        await self.session_repo.save(session)


class SkipRoundHandler:
    def __init__(self, session_repo: ISessionRepository):
        self.session_repo = session_repo

    async def __call__(self, command: SkipRound) -> None:
        session = await self.session_repo.get_by_id(command.session_id)
        if not session:
            raise ValueError(f"Session {command.session_id} not found")
        
        session.skip_round()
        await self.session_repo.save(session)


class SkipBlockHandler:
    def __init__(self, session_repo: ISessionRepository):
        self.session_repo = session_repo

    async def __call__(self, command: SkipBlock) -> None:
        session = await self.session_repo.get_by_id(command.session_id)
        if not session:
            raise ValueError(f"Session {command.session_id} not found")
        
        session.skip_block()
        await self.session_repo.save(session)
