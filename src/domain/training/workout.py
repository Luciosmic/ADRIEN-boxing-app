from typing import List, Optional
from datetime import datetime
import uuid
from pydantic import Field

from src.domain._base.entity import Entity
from src.domain.training.value_objects import Block

class Workout(Entity):
    """
    Represents a workout routine consisting of a sequence of training blocks.
    """
    name: str
    blocks: List[Block] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)

    def add_block(self, block: Block):
        self.blocks.append(block)

    def remove_block_at(self, index: int):
        if 0 <= index < len(self.blocks):
            self.blocks.pop(index)

    def update_block_at(self, index: int, block: Block):
        if 0 <= index < len(self.blocks):
            self.blocks[index] = block

    def duplicate_block_at(self, index: int):
        if 0 <= index < len(self.blocks):
            original = self.blocks[index]
            # Create a copy with a new ID
            new_block = original.model_copy(update={"id": str(uuid.uuid4())})
            self.blocks.insert(index + 1, new_block)

    def move_block(self, from_index: int, to_index: int):
        if 0 <= from_index < len(self.blocks) and 0 <= to_index < len(self.blocks):
            block = self.blocks.pop(from_index)
            self.blocks.insert(to_index, block)
