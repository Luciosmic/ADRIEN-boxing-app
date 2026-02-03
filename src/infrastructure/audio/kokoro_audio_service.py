"""
Kokoro TTS Audio Service - Infrastructure implementation.
Uses MLX-optimized Kokoro model for high-quality speech synthesis.
"""
import asyncio
import os
import tempfile
import logging
import mlx.core as mx
import numpy as np
import soundfile as sf
from mlx_audio.tts import load
from src.application.ports.i_audio_service import IAudioService

logger = logging.getLogger(__name__)


class KokoroAudioService(IAudioService):
    """
    Audio service implementation using Kokoro TTS via MLX.
    Optimized for Apple Silicon with high-quality voice synthesis.
    """
    
    def __init__(
        self, 
        repo_id: str = "prince-canuma/Kokoro-82M", 
        voice: str = "ff_siwis",  # French female voice
        speed: float = 1.0
    ):
        """
        Initialize Kokoro audio service.
        
        Args:
            repo_id: HuggingFace model repository ID
            voice: Voice identifier (e.g., 'ff_siwis' for French Female)
            speed: Speech speed multiplier (1.0 = normal)
        """
        self.repo_id = repo_id
        self.voice = voice
        self.speed = speed
        self._model = None
        logger.info(f"Initialized Kokoro Audio Service (repo={repo_id}, voice={voice})")

    @property
    def model(self):
        """Lazy-load the Kokoro model on first use."""
        if self._model is None:
            logger.info("Loading Kokoro model... this may take a moment.")
            self._model = load(self.repo_id)
            logger.info("Kokoro model loaded successfully.")
        return self._model

    async def speak(self, text: str, language: str = "en") -> None:
        """
        Synthesize and play speech using Kokoro TTS.
        
        Args:
            text: Text to speak
            language: Language code (currently Kokoro uses 'a' for auto-detect)
        """
        if not text:
            return

        logger.info(f"Speaking: {text}")
        
        try:
            # Generate audio in a thread to avoid blocking
            audio_data, sample_rate = await asyncio.to_thread(
                self._generate, text
            )
            
            if audio_data is None:
                logger.warning("No audio generated.")
                return

            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
                tmp_path = tf.name
                
            sf.write(tmp_path, audio_data, sample_rate)
            
            # Play using afplay (macOS)
            process = await asyncio.create_subprocess_shell(
                f"afplay {tmp_path}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                logger.error(f"Error playing audio: {stderr.decode()}")
            
            # Cleanup
            try:
                os.remove(tmp_path)
            except OSError:
                pass
                
        except Exception as e:
            logger.error(f"Error in Kokoro speak: {e}")
            import traceback
            traceback.print_exc()

    def _generate(self, text: str):
        """
        Synchronous generation helper.
        
        Returns:
            Tuple of (numpy_audio, sample_rate)
        """
        generator = self.model.generate(
            text, 
            voice=self.voice, 
            speed=self.speed
        )
        
        all_audio = []
        sample_rate = 24000
        
        for result in generator:
            all_audio.append(result.audio)
            sample_rate = result.sample_rate
            
        if not all_audio:
            return None, sample_rate
            
        full_audio = mx.concatenate(all_audio, axis=0)
        return np.array(full_audio), sample_rate
