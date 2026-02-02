import pytest
import os
import json
import shutil
from uuid import uuid4
from datetime import datetime
from src.infrastructure.events.store.osu_event_store import OsuFileEventStore
from src.domain._base.domain_event import DomainEvent

class MockEvent(DomainEvent):
    some_data: str

@pytest.mark.anyio
async def test_osu_event_store_append():
    test_dir = ".osu_test"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    
    store = OsuFileEventStore(base_path=test_dir)
    
    agg_id = uuid4()
    event = MockEvent(some_data="hello")
    
    await store.append(agg_id, [event], 0)
    
    file_path = os.path.join(test_dir, f"{agg_id}.jsonl")
    assert os.path.exists(file_path)
    
    with open(file_path, "r") as f:
        lines = f.readlines()
        assert len(lines) == 1
        data = json.loads(lines[0])
        assert data["event_type"] == "MockEvent"
        assert "hello" in data["event_data"]
    
    # Cleanup
    shutil.rmtree(test_dir)
