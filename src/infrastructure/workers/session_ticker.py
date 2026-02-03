import asyncio
import logging
from typing import List
from src.application.training_service.i_api_training_service import ITrainingService
from src.application.training_service.dtos.training_request_dtos import TickSessionRequest, ListWorkoutsRequest
# Note: We need a way to list *active sessions*. 
# The current Service API has `list_workouts` but not `list_active_sessions`.
# For MVP, we might assume the UI/User provides the Session ID to the worker, 
# or the worker manages the *current* session ID.
# Let's assume the Worker is started *for* a specific session, or monitors a shared state.

# Design: A SessionTicker that is instantiated with a Session ID.
# Or a Global Worker that finds running sessions.
# Given the "Osu" file repo, we can list files in `sessions/` and check status?
# But logic should be in Service.

# Let's add `list_active_sessions` to Service? 
# Or simpler: The UI starts the worker when it starts a session.
# User Request: "backend worker to deal with the ticking".

# Approach: A class TickerWorker that runs a loop for a specific session_id.

logger = logging.getLogger(__name__)

class SessionTickerWorker:
    def __init__(self, service: ITrainingService, interval: float = 1.0):
        self.service = service
        self.interval = interval
        self._running = False
        self._task = None

    async def start(self, session_id: str):
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._loop(session_id))
        logger.info(f"Ticker started for session {session_id}")

    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Ticker stopped")

    async def _loop(self, session_id: str):
        while self._running:
            try:
                # 1. Tick
                result = await self.service.tick_session(TickSessionRequest(session_id=session_id))
                
                # 2. Check result
                if not result.success:
                    # Session might be paused or finished?
                    # The Service returns success=True/False. 
                    # If finished, we should probably stop?
                    # We need to query state to know WHY it failed or if it's done.
                    pass
                
                # 3. Check Status to auto-stop?
                # Optimization: GetSession request to ensure we stop if COMPLETED.
                # state = await self.service.get_session(...)
                # if state.status == COMPLETED: break
                
            except Exception as e:
                logger.error(f"Ticker error: {e}")
            
            await asyncio.sleep(self.interval)
