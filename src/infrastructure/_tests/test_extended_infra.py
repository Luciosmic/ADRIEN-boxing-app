import unittest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from src.infrastructure.workers.session_ticker import SessionTickerWorker
from src.infrastructure.events.bus.in_memory_event_bus import InMemoryEventBus
from src.domain._base.domain_event import DomainEvent
from src.application.training_service.dtos.training_request_dtos import TickSessionRequest

# --- mocked events ---
class MockDomainEvent(DomainEvent):
    pass

class TestExtendedInfra(unittest.IsolatedAsyncioTestCase):
    async def test_session_ticker_worker(self):
        """Verify TickerWorker calls tick_session periodically."""
        mock_service = AsyncMock()
        mock_service.tick_session.return_value = MagicMock(success=True)
        
        worker = SessionTickerWorker(service=mock_service, interval=0.05)
        
        # Start worker for a session
        await worker.start("sess_123")
        
        # Wait for a bit (enough for 2-3 ticks)
        await asyncio.sleep(0.2)
        
        # Stop
        await worker.stop()
        
        # Verify calls
        self.assertGreaterEqual(mock_service.tick_session.call_count, 2)
        # Check arguments
        call_args = mock_service.tick_session.call_args[0][0]
        self.assertIsInstance(call_args, TickSessionRequest)
        self.assertEqual(call_args.session_id, "sess_123")

    async def test_event_bus_subscription_flow(self):
        """Verify InMemoryEventBus handles subscription and publishing logic."""
        bus = InMemoryEventBus()
        
        received_events = []
        async def handler(event):
            received_events.append(event)
            
        bus.subscribe(MockDomainEvent, handler)
        
        evt = MockDomainEvent()
        await bus.publish([evt])
        
        self.assertEqual(len(received_events), 1)
        self.assertEqual(received_events[0], evt)
