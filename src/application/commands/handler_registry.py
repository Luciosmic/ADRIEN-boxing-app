from typing import Dict, Type, Callable, Any

class HandlerRegistry:
    """
    Registry for mapping messages (Commands/Queries/Events) to their handlers.
    """
    def __init__(self):
        self._handlers: Dict[Type, Callable] = {}

    def register(self, message_type: Type, handler: Callable):
        """Register a handler for a specific message type."""
        self._handlers[message_type] = handler

    def get_handler(self, message_type: Type) -> Callable:
        """Retrieve the handler for a message type."""
        handler = self._handlers.get(message_type)
        if not handler:
            raise ValueError(f"No handler registered for {message_type.__name__}")
        return handler
