import pytest
from src.domain.training.workout import Workout
from src.domain.training.value_objects import Block, BlockType

def test_workout_creation():
    workout = Workout(name="Test Workout", id="w1")
    assert workout.name == "Test Workout"
    assert len(workout.blocks) == 0

def test_add_block():
    workout = Workout(name="Test", id="w1")
    block = Block(type=BlockType.WARMUP, work_time=60)
    workout.add_block(block)
    assert len(workout.blocks) == 1
    assert workout.blocks[0].type == BlockType.WARMUP

def test_remove_block():
    workout = Workout(name="Test", id="w1")
    block = Block(type=BlockType.WARMUP)
    workout.add_block(block)
    workout.remove_block_at(0)
    assert len(workout.blocks) == 0

def test_duplicate_block():
    workout = Workout(name="Test", id="w1")
    block = Block(type=BlockType.HEAVY_BAG, work_time=120)
    workout.add_block(block)
    workout.duplicate_block_at(0)
    
    assert len(workout.blocks) == 2
    assert workout.blocks[0].type == BlockType.HEAVY_BAG
    assert workout.blocks[1].type == BlockType.HEAVY_BAG
    # IDs should be different
    assert workout.blocks[0].id != workout.blocks[1].id
