import logging
import json
from typing import Any, Dict

class StructuredLogger:
    """
    Logger that outputs JSON structure for better observability.
    """
    def __init__(self, name: str):
        self._logger = logging.getLogger(name)
        # Configure basics if not already done
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.INFO)

    def info(self, message: str, **kwargs):
        self._log(logging.INFO, message, **kwargs)

    def error(self, message: str, **kwargs):
        self._log(logging.ERROR, message, **kwargs)

    def warning(self, message: str, **kwargs):
        self._log(logging.WARNING, message, **kwargs)

    def _log(self, level: int, message: str, **kwargs):
        entry = {
            "message": message,
            "level": logging.getLevelName(level),
            **kwargs
        }
        # In a real app, you might use a JSONFormater
        self._logger.log(level, json.dumps(entry))
