from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable, Dict, Optional

from helpers.singleton import Singleton


@dataclass
class CacheEntry:
    value: Optional[any] = None
    last_called: Optional[datetime] = None
    update_at: Optional[datetime] = None

    def is_expired(self) -> bool:
        if not self.last_called or not self.update_at:
            return True

        if datetime.now() > self.update_at:
            return True

        return False


class DataCache:
    __metaclass__ = Singleton

    def __init__(self):
        self.cache: Dict[Callable, CacheEntry] = {}

    def is_value_in_cache(self, func: Callable) -> bool:
        if func not in self.cache:
            return False

        cache_entry = self.cache[func]
        return not cache_entry.is_expired()

    def save_method_in_cache(self, func: Callable) -> None:
        if func not in self.cache:
            self.cache[func] = CacheEntry()

    def get_value(self, func: Callable) -> any:
        if self.is_value_in_cache(func):
            return self.cache[func].value

    def save_value_in_cache(self, func: Callable, value: any, expires_in: float = None,
                            expires_at: datetime = None) -> None:

        if not expires_in and not expires_at or expires_in and expires_at:
            raise Exception("You have to specify ether expires_in or expires_at")

        if expires_at:
            update_at = expires_at
        else:
            update_at = datetime.now() + timedelta(0, expires_in)

        self.cache[func] = CacheEntry(
            value=value,
            last_called=datetime.now(),
            update_at=update_at
        )


def cache(expires_in: Optional[float] = None, expires_at: Optional[datetime] = None):
    if not expires_in and not expires_at or expires_in and expires_at:
        raise Exception("You have to specify ether expires_in or expires_at")

    data_cache = DataCache()

    def function_wrapper(func: Callable) -> Callable:

        async def wrapper(*args, **kwargs) -> any:
            value: any
            if data_cache.is_value_in_cache(func):
                value = data_cache.get_value(func)
            else:
                value = await func(*args, **kwargs)
                data_cache.save_value_in_cache(func, value, expires_in, expires_at)
            return value

        data_cache.save_method_in_cache(func)
        return wrapper

    return function_wrapper
