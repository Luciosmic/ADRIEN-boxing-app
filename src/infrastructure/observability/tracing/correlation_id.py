import contextvars
from uuid import uuid4

_correlation_id_ctx = contextvars.ContextVar("correlation_id", default=None)

def get_correlation_id() -> str:
    """Get the current correlation ID or generate a new one if not set."""
    cid = _correlation_id_ctx.get()
    if not cid:
        cid = str(uuid4())
        set_correlation_id(cid)
    return cid

def set_correlation_id(cid: str):
    """Set the correlation ID for the current context."""
    _correlation_id_ctx.set(cid)
