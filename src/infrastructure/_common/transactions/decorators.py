import functools
import logging
from typing import Callable, Type, Any
from src.infrastructure._common.transactions.unit_of_work import AbstractUnitOfWork

logger = logging.getLogger(__name__)

def transactional(uow: AbstractUnitOfWork):
    """
    Decorator to wrap a function execution in a Unit of Work transaction.
    
    Usage:
        @transactional(uow=my_uow_instance)
        def my_use_case(...): ...
        
    Note: Ideally, the UoW is injected into the class, and the decorator 
    handles looking it up. But for a simple functional decorator, we might 
    need to handle 'self'.
    """
    import inspect

    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Attempt to find uow in args[0] (self) if it's a method
            instance = args[0] if args else None
            actual_uow = getattr(instance, 'uow', None)
            
            if not actual_uow:
                logger.warning(f"No 'uow' attribute found on {instance}. Transactional skipped.")
                # If func is async, await it
                if inspect.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                return func(*args, **kwargs)

            async with actual_uow:
                try:
                    if inspect.iscoroutinefunction(func):
                        result = await func(*args, **kwargs)
                    else:
                        result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    logger.error(f"Transaction failed: {e}")
                    raise e
                    
        return wrapper
    return decorator
