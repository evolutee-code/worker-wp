import functools
from typing import Optional

from mona_package import AbstractRepository
from core.contracts import AbstractRepository as BaseRepository


class ActionDecorator:
    base_repository: AbstractRepository | None

    def __init__(self, base_repository: Optional[BaseRepository]):
        self.base_repository = base_repository

    def create_action_history(self, name: str):
        def decorator_log(func):
            @functools.wraps(func)
            async def wrapper_log_history(*args, **kwargs):
                result = await func(*args, **kwargs)
                try:
                    print(11)
                except Exception:
                    pass
                return result

            return wrapper_log_history

        return decorator_log
