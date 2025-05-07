from functools import wraps
import time

from ..logger import logger


def timing_decorator():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Record start time
            start_time = time.time()

            # Call the endpoint function
            response = await func(*args, **kwargs)

            # Calculate processing time
            process_time = time.time() - start_time

            # Log the time
            logger.info(f"{func.__name__} took {process_time:.4f} seconds")

            return response

        return wrapper

    return decorator
