class AppError(Exception):
    """Base exception for all application errors."""
    pass

class FatalError(AppError):
    """
    Errors that cannot be recovered from by retrying.
    Examples: Invalid Configuration, Logic Bugs, Data Corruption.
    """
    pass

class TransientError(AppError):
    """
    Errors that might be resolved by retrying.
    Examples: Network Timeouts, Temporary Service Unavailability, Rate Limits.
    """
    pass

class CircuitOpenError(TransientError):
    """Raised when a circuit breaker is open."""
    pass
