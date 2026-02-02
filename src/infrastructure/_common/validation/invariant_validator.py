from functools import wraps
from typing import Callable, Any

def validate_invariants(method: Callable) -> Callable:
    """
    Decorator to run invariant validation after a method call.
    Assumes the object has a check_invariants() method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        if hasattr(self, 'check_invariants'):
            self.check_invariants()
        return result
    return wrapper

class InvariantError(Exception):
    pass
