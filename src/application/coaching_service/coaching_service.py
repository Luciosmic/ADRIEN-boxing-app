"""
Coaching Service Implementation.
Generates contextual instructions for training sessions.
"""
import logging
import random
import time
from typing import Dict
from src.application.coaching_service.i_api_coaching_service import IApiCoachingService
from src.application.coaching_service.dtos import (
    GetInstructionRequest,
    InstructionResponse,
    InstructionType
)
from src.domain.training.value_objects import BlockType, TechniqueCategory
from src.domain.training.content import TECHNIQUES

logger = logging.getLogger(__name__)


class CoachingService(IApiCoachingService):
    """
    Application service for generating coaching instructions.
    Provides contextual guidance based on session state.
    """
    
    def __init__(self):
        """Initialize the coaching service."""
        # Track last instruction time per session to avoid spam
        self._last_instruction_time: Dict[str, float] = {}
    
    async def get_instruction(
        self, 
        request: GetInstructionRequest
    ) -> InstructionResponse:
        """Generate a coaching instruction based on session state."""
        
        # Priority 1: Countdown (highest priority)
        if request.time_left <= 3 and request.time_left > 0:
            return InstructionResponse(
                text=str(request.time_left),
                type=InstructionType.COUNTDOWN,
                priority=10
            )
        
        # Priority 2: Rest phase
        if not request.is_work_phase:
            rest_text = self._get_rest_text(request.language)
            return InstructionResponse(
                text=rest_text,
                type=InstructionType.REST,
                priority=5
            )
        
        # Priority 3: Work phase instructions
        # Check if enough time has passed since last instruction
        now = time.time()
        last_time = self._last_instruction_time.get(request.session_id, 0)
        
        # Frequency based on block type
        freq_map = {
            BlockType.HEAVY_BAG: 5,
            BlockType.SHADOW_BOXING: 5,
            BlockType.WARMUP: 7,
            BlockType.JUMP_ROPE: 3,
            BlockType.STRENGTH: 10,
            BlockType.SPARRING: 5,
            BlockType.COOLDOWN: 10
        }
        interval = freq_map.get(request.block_type, 5)
        
        # Don't announce too frequently, and avoid countdown zone
        if (now - last_time < interval) or request.time_left <= 3:
            return InstructionResponse(
                text="",
                type=InstructionType.COACHING,
                priority=0
            )
        
        # Generate instruction based on block type
        instruction = self._generate_work_instruction(request)
        
        if instruction.text:
            self._last_instruction_time[request.session_id] = now
        
        return instruction
    
    def _generate_work_instruction(
        self, 
        request: GetInstructionRequest
    ) -> InstructionResponse:
        """Generate work phase instruction based on block type."""
        
        # Technique-based blocks
        if request.block_type in [
            BlockType.HEAVY_BAG, 
            BlockType.SHADOW_BOXING, 
            BlockType.WARMUP,
            BlockType.SPARRING
        ]:
            return self._get_technique_instruction(
                request.techniques,
                request.language
            )
        
        # Jump rope
        elif request.block_type == BlockType.JUMP_ROPE:
            return self._get_jump_rope_instruction(request.language)
        
        # Strength training
        elif request.block_type == BlockType.STRENGTH:
            return self._get_strength_instruction(
                request.exercises,
                request.language
            )
        
        # Default
        return InstructionResponse(
            text="",
            type=InstructionType.COACHING,
            priority=1
        )
    
    def _get_technique_instruction(
        self,
        techniques: list[TechniqueCategory] | None,
        language: str
    ) -> InstructionResponse:
        """Get a random technique instruction."""
        
        # Get techniques for language
        lang_techniques = TECHNIQUES.get(language, TECHNIQUES.get('en', {}))
        
        if not lang_techniques:
            return InstructionResponse(
                text="",
                type=InstructionType.TECHNIQUE,
                priority=3
            )
        
        # If specific techniques are provided, use those
        if techniques:
            # Convert enum to string keys
            technique_keys = [t.value if hasattr(t, 'value') else str(t).lower() 
                            for t in techniques]
            available = {k: v for k, v in lang_techniques.items() 
                        if k in technique_keys}
            
            if available:
                category = random.choice(list(available.keys()))
                moves = available[category]
            else:
                # Fallback to all techniques
                category = random.choice(list(lang_techniques.keys()))
                moves = lang_techniques[category]
        else:
            # Use all available techniques
            category = random.choice(list(lang_techniques.keys()))
            moves = lang_techniques[category]
        
        if moves:
            technique = random.choice(moves)
            return InstructionResponse(
                text=technique,
                type=InstructionType.TECHNIQUE,
                priority=3
            )
        
        return InstructionResponse(
            text="",
            type=InstructionType.TECHNIQUE,
            priority=3
        )
    
    def _get_jump_rope_instruction(self, language: str) -> InstructionResponse:
        """Get a jump rope variation instruction."""
        
        variations = {
            'fr': ["Sauts simples", "Sauts alternés", "Double saut", "Croisés"],
            'en': ["Single jumps", "Alternate jumps", "Double unders", "Crossovers"],
            'es': ["Saltos simples", "Saltos alternados", "Doble salto", "Cruzados"]
        }
        
        lang_variations = variations.get(language, variations['en'])
        variation = random.choice(lang_variations)
        
        return InstructionResponse(
            text=variation,
            type=InstructionType.COACHING,
            priority=3
        )
    
    def _get_strength_instruction(
        self,
        exercises: Dict[str, int] | None,
        language: str
    ) -> InstructionResponse:
        """Get a strength exercise instruction."""
        
        if not exercises:
            return InstructionResponse(
                text="",
                type=InstructionType.EXERCISE,
                priority=3
            )
        
        # Pick a random exercise
        exercise_name = random.choice(list(exercises.keys()))
        reps = exercises[exercise_name]
        
        reps_text = {
            'fr': 'reps',
            'en': 'reps',
            'es': 'reps'
        }
        
        text = f"{exercise_name}: {reps} {reps_text.get(language, 'reps')}"
        
        return InstructionResponse(
            text=text,
            type=InstructionType.EXERCISE,
            priority=3
        )
    
    def _get_rest_text(self, language: str) -> str:
        """Get rest phase text."""
        rest_texts = {
            'fr': 'Repos',
            'en': 'Rest',
            'es': 'Descanso'
        }
        return rest_texts.get(language, 'Rest')
