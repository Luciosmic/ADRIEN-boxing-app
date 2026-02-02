import asyncio
import logging
import random
from typing import Callable, Type, Optional, Any
from functools import wraps
from datetime import datetime, timedelta
from .errors import TransientError, CircuitOpenError

logger = logging.getLogger(__name__)

class RetryPolicy:
    """
    Configurable Retry Policy with Exponential Backoff and Jitter.
    """
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 10.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    async def execute(self, func: Callable, *args, **kwargs):
        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)
            except Exception as e:
                # Only retry on TransientError or if the user configured a list of retryable exceptions
                # For simplicity here, we assume standard Exceptions are potential candidates if wrapped,
                # but STRICTLY we should check for TransientError.
                # Let's check if it's NOT Fatal.
                # If we don't know the type, we might retry networky things.
                # To fail safe: retry if it is explicitly TransientError.
                
                is_transient = isinstance(e, TransientError)
                if not is_transient:
                     # Check some common ones? TimeoutError?
                     if isinstance(e, (TimeoutError, ConnectionError)):
                         is_transient = True
                
                if not is_transient:
                    raise e

                last_exception = e
                if attempt < self.max_retries:
                    delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                    # Add jitter (0-10% of delay)
                    jitter = delay * random.uniform(0, 0.1)
                    sleep_time = delay + jitter
                    
                    logger.warning(f"Operation failed with {e}. Retrying in {sleep_time:.2f}s (Attempt {attempt+1}/{self.max_retries})")
                    await asyncio.sleep(sleep_time)
                else:
                    logger.error(f"Operation failed after {self.max_retries} retries.")
                    
        raise last_exception

class CircuitBreaker:
    """
    Circuit Breaker State Machine.
    Protects downstream systems from overload.
    """
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state = "CLOSED"
        self.last_failure_time = None

    async def execute(self, func: Callable, *args, **kwargs):
        if self.state == "OPEN":
            if datetime.utcnow() - self.last_failure_time > timedelta(seconds=self.recovery_timeout):
                logger.info("Circuit Breaker probing... (HALF-OPEN)")
                self.state = "HALF-OPEN"
            else:
                raise CircuitOpenError("Circuit is OPEN. Fast fail.")

        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            # Success
            if self.state == "HALF-OPEN":
                logger.info("Circuit Breaker recovered. (CLOSED)")
                self.state = "CLOSED"
                self.failure_count = 0
            
            return result

        except Exception as e:
            # Logic: If it's a TransientError, count it. Fatal errors might not trip breaker?
            # Usually Connectivity errors trip breakers.
            self.failure_count += 1
            self.last_failure_time = datetime.utcnow()
            
            if self.failure_count >= self.failure_threshold:
                if self.state != "OPEN":
                    logger.critical(f"Circuit Breaker TRIPPED to OPEN after {self.failure_count} failures.")
                self.state = "OPEN"
            
            raise e
