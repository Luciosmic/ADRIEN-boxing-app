from enum import Enum
from typing import Optional, List
from pydantic import Field, PrivateAttr
from datetime import datetime
import random

from src.domain._base.aggregate_root import AggregateRoot
from src.domain.training.workout import Workout
from src.domain.training.value_objects import Block, BlockType, TechniqueCategory, ExerciseType
from src.domain.training.events import (
    SessionStarted, SessionPaused, SessionResumed, SessionCompleted,
    BlockStarted, RoundStarted, RestStarted, AnnouncementTriggered
)

class SessionStatus(str, Enum):
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"

class TrainingSession(AggregateRoot):
    workout: Workout
    status: SessionStatus = SessionStatus.IDLE
    current_block_index: int = 0
    current_round: int = 1
    time_left: int = 0
    is_work_phase: bool = True
    
    # Internal state for timers/logic
    _last_announcement_time: int = PrivateAttr(default=0)
    _current_exercise_index: int = PrivateAttr(default=0)
    _current_rep_count: int = PrivateAttr(default=1)

    def start(self):
        if self.status == SessionStatus.IDLE:
            self.status = SessionStatus.RUNNING
            self._initialize_current_block()
            self.add_domain_event(SessionStarted(
                session_id=str(self.id), 
                workout_id=str(self.workout.id),
                started_at=datetime.now()
            ))
        elif self.status == SessionStatus.PAUSED:
            self.status = SessionStatus.RUNNING
            self.add_domain_event(SessionResumed(
                session_id=str(self.id),
                resumed_at=datetime.now()
            ))

    def pause(self):
        if self.status == SessionStatus.RUNNING:
            self.status = SessionStatus.PAUSED
            self.add_domain_event(SessionPaused(
                session_id=str(self.id),
                paused_at=datetime.now()
            ))

    def tick(self):
        """
        Advance the session state by 1 second.
        Should be called by a periodic task/loop in the application layer.
        """
        if self.status != SessionStatus.RUNNING:
            return

        if self.time_left > 0:
            self.time_left -= 1
            self._handle_timer_logic()

        if self.time_left == 0:
            self._handle_phase_complete()
        
        # Emit tick event for listeners (coaching, etc.)
        from src.domain.training.events import SessionTicked
        if self.current_block_index < len(self.workout.blocks):
            self.add_domain_event(SessionTicked(
                session_id=str(self.id),
                current_block_index=self.current_block_index,
                block_type=self.workout.blocks[self.current_block_index].type,
                current_round=self.current_round,
                time_left=self.time_left,
                is_work_phase=self.is_work_phase
            ))

    def _initialize_current_block(self):
        if self.current_block_index >= len(self.workout.blocks):
            self.status = SessionStatus.COMPLETED
            self.add_domain_event(SessionCompleted(
                session_id=str(self.id),
                completed_at=datetime.now()
            ))
            return

        block = self.workout.blocks[self.current_block_index]
        self.current_round = 1
        self.is_work_phase = True
        self._current_exercise_index = 0
        self._current_rep_count = 1
        
        self.add_domain_event(BlockStarted(
            session_id=str(self.id),
            block_index=self.current_block_index,
            block_type=block.type,
            block_name=block.type # Could be mapped to human readable
        ))

        self._set_phase_time(block)

    def _set_phase_time(self, block: Block):
        if block.type == BlockType.STRENGTH:
             # Logic for strength training time/reps calculation
             # Simplified: If work phase, use calculated time for reps? or manual?
             # React code: setTimeLeft(Math.ceil(reps * 2));
             exercises = list(block.exercises.items())
             if exercises:
                 ex_name, reps = exercises[0]
                 self.time_left =  int(reps * 2)
             else:
                 self.time_left = 60
        else:
             self.time_left = block.work_time
        
        self.add_domain_event(RoundStarted(
            session_id=str(self.id),
            round_number=self.current_round,
            total_rounds=block.rounds,
            duration=self.time_left
        ))

    def _handle_timer_logic(self):
        # 1. Countdown announcements (10s, 3s, 2s, 1s)
        if self.time_left == 10 and self.is_work_phase:
            self._announce("10")
        elif self.time_left <= 3 and self.time_left > 0:
             self._announce(str(self.time_left))
        
        # 2. Random announcements based on frequency/block type
        # This logic mimics the react `handleTimerLogic`
        # We need a way to track "ticks since last announcement" properly.
        # For now, simplistic approximation.
        # React used `Date.now()`. Here we rely on `tick` being 1s.
        pass # TODO: Implement complex announcement logic (combos, coaching)

    def _handle_phase_complete(self):
        block = self.workout.blocks[self.current_block_index]

        # Use generic logic for standard blocks
        if block.type in [BlockType.JUMP_ROPE, BlockType.HEAVY_BAG, BlockType.SPARRING, BlockType.SHADOW_BOXING, BlockType.WARMUP, BlockType.COOLDOWN]:
            if self.is_work_phase:
                # End of Work -> Rest
                self.is_work_phase = False
                self.time_left = block.rest_time
                self.add_domain_event(RestStarted(
                    session_id=str(self.id),
                    duration=self.time_left
                ))
                self._announce("Rest")
            else:
                # End of Rest -> Next Round or Next Block
                if self.current_round < block.rounds:
                    self.current_round += 1
                    self.is_work_phase = True
                    self.time_left = block.work_time
                    self.add_domain_event(RoundStarted(
                        session_id=str(self.id),
                        round_number=self.current_round,
                        total_rounds=block.rounds,
                        duration=self.time_left
                    ))
                    self._announce(f"Round {self.current_round}")
                else:
                    self._go_to_next_block()
        
        elif block.type == BlockType.STRENGTH:
             # Strength logic (Exercise -> Rest -> Next Exercise)
             # This requires iterating through exercises list
             # React logic:
             # isWorkPhase (doing reps) -> Rest -> Next Round (Same exercise? or Next exercise?)
             # React code: One exercise per round-ish cycle? 
             # "const exerciseIndex = (currentRound - 1) % exercises.length;"
             
             if self.is_work_phase:
                 # Finished reps
                 if self.current_round < block.rounds:
                     self.current_round += 1
                     self.is_work_phase = False
                     self.time_left = block.rest_time
                     self.add_domain_event(RestStarted(session_id=str(self.id), duration=self.time_left))
                     self._announce("Rest")
                 else:
                     self._go_to_next_block()
             else:
                 # Finished Rest -> Next Set
                 self.is_work_phase = True
                 exercises = list(block.exercises.items())
                 if exercises:
                     idx = (self.current_round - 1) % len(exercises)
                     name, reps = exercises[idx]
                     self.time_left = int(reps * 2)
                     self._announce(f"Set {self.current_round}: {name}")
                     self.add_domain_event(RoundStarted(
                         session_id=str(self.id),
                         round_number=self.current_round,
                         total_rounds=block.rounds,
                         duration=self.time_left
                     ))
        else:
            self._go_to_next_block()


    def _go_to_next_block(self):
        self.current_block_index += 1
        self._initialize_current_block()

    def skip_block(self):
        self._go_to_next_block()

    def skip_round(self):
        block = self.workout.blocks[self.current_block_index]
        if self.current_round < block.rounds:
             self.current_round += 1
             # Reset to WORK phase of next round
             self.is_work_phase = True
             # Recalculate time based on block type
             if block.type == BlockType.STRENGTH:
                 exercises = list(block.exercises.items())
                 if exercises:
                     idx = (self.current_round - 1) % len(exercises)
                     name, reps = exercises[idx]
                     self.time_left = int(reps * 2)
             else:
                 self.time_left = block.work_time
                 
             self.add_domain_event(RoundStarted(
                session_id=str(self.id),
                round_number=self.current_round,
                total_rounds=block.rounds,
                duration=self.time_left
             ))
        else:
            self._go_to_next_block()

    def _announce(self, text: str):
        self.add_domain_event(AnnouncementTriggered(
            session_id=str(self.id),
            text=text
        ))
