import unittest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from src.infrastructure.audio.piper_announcer import PiperAnnouncer

class TestPiperAnnouncer(unittest.IsolatedAsyncioTestCase):
    async def test_piper_announcer_command_construction(self):
        """Verify PiperAnnouncer calls subprocess with correct args."""
        with patch("src.infrastructure.audio.piper_announcer.asyncio.create_subprocess_shell") as mock_exec:
            # Define mock process return
            mock_process = AsyncMock()
            mock_process.communicate.return_value = (b"", b"")
            mock_process.return_value = 0
            mock_exec.return_value = mock_process
            
            announcer = PiperAnnouncer(piper_path="/custom/piper", model_path="model.onnx")
            await announcer.announce("Hello World")
            
            # Check command
            mock_exec.assert_called_once()
            cmd = mock_exec.call_args[0][0]
            self.assertIn("/custom/piper", cmd)
            self.assertIn("--model model.onnx", cmd)
            self.assertIn("echo 'Hello World'", cmd)
