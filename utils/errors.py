import logging
import traceback
from functools import wraps
from typing import Callable, Any, Optional, Dict

logger = logging.getLogger(__name__)


def safe_execute(
    func: Callable,
    fallback_message: str = "An unexpected error occurred.",
    default_return: Any = None,
    *args,
    **kwargs,
) -> Any:
    """
    Safely executes a target function within an error boundary.
    Logs tracebacks on failure and returns fallback default instead of crashing.

    Parameters
    ----------
    func : Callable
        Function to execute.
    fallback_message : str
        User-friendly fallback error message to log.
    default_return : Any
        Default value to return on failure.

    Returns
    -------
    Any
        Result of func or default_return on exception.
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error Boundary caught exception in '{func.__name__}': {e}")
        logger.debug(traceback.format_exc())
        return default_return


def handle_errors(fallback_message: str = "Service error occurred."):
    """
    Decorator for wrapping functions in a safe execution error boundary.
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Handled error in {func.__name__}: {e}")
                logger.debug(traceback.format_exc())
                return {"success": False, "error": str(e), "message": f"⚠️ {fallback_message}: {e}"}

        return wrapper

    return decorator
