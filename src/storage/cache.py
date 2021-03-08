import asyncio
import functools
import re
from datetime import datetime, timedelta
from typing import Optional, Any, Dict, Callable, Tuple, Hashable

from helpers.singleton import Singleton


class _Timer:

    def __init__(self, start_time: datetime):
        self._start_time: datetime = start_time

        self._expiry_str: Optional[str] = None
        self._schedule_str: Optional[str] = None
        self._expiry_date: Optional[datetime] = None

    def set_expiry(self, expires_every: str, schedule: str):
        self._expiry_str = expires_every
        self._schedule_str = schedule
        if self._expiry_str:
            self._expiry_date = self._parse_expiry()
        else:
            self._expiry_date = self._parse_schedule()

    def _parse_expiry(self) -> datetime:
        split_str = self._expiry_str.split(":")
        h = split_str[0]
        m = split_str[1]
        s = split_str[2]

        seconds = 0
        if not re.search("^\\*+$", h):
            seconds += int(h) * 60 * 60

        if not re.search("^\\*+$", m):
            seconds += int(m) * 60

        if not re.search("^\\*+$", s):
            seconds += int(s)

        return self._start_time + timedelta(0, seconds)

    def _parse_schedule(self) -> datetime:
        split_str = self._schedule_str.split(":")
        h = split_str[0]
        m = split_str[1]
        s = split_str[2]

        current = datetime.now()
        days = current.day

        if not re.search("^\\*+$", s):
            seconds = int(s)
        else:
            seconds = current.second

        if not re.search("^\\*+$", m):
            minutes = int(m)
        else:
            minutes = current.minute

        if not re.search("^\\*+$", h):
            hours = int(h)
        else:
            hours = current.hour

        if re.search("^\\*+$", h) and re.search("^\\*+$", m):
            minutes += 1
        elif re.search("^\\*+$", h):
            hours += 1
        else:
            days += 1

        return datetime(current.year, current.month, current.day, hours, minutes, seconds)

    def has_expired(self) -> bool:
        return self._expiry_date < datetime.now()

    def reset(self):
        self._start_time = datetime.now()
        if self._expiry_str:
            self._expiry_date = self._parse_expiry()
        else:
            self._expiry_date = self._parse_schedule()


class CacheEntry:
    def __init__(self):
        self._value: Optional[Any] = None
        self._timer = _Timer(datetime.now())
        self._was_set = False

    @staticmethod
    def _verify_scheduler(expires_every: str, cron_schedule: str) -> None:
        specify_count = 0
        if expires_every:
            specify_count += 1
        if cron_schedule:
            specify_count += 1

        if specify_count != 1:
            raise Exception("Specify exactly one timing method.")

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value):
        self._was_set = True
        self._value = value
        self._timer.reset()

    def is_valid(self) -> bool:
        return self._was_set and not self._timer.has_expired()

    def set_expiry(self, expires_every: str = None, schedule: str = None) -> None:
        CacheEntry._verify_scheduler(expires_every, schedule)
        self._timer.set_expiry(expires_every, schedule)


class FunctionCache:
    def __init__(self, max_cache_entries: int):
        self.max_cache_entries = max_cache_entries
        self.cache: Dict[int, CacheEntry] = {}

    def is_in_cache(self, key: int) -> bool:
        return key in self.cache and \
               self.cache[key].is_valid()

    def get_value_from_cache(self, key: int) -> Any:
        if self.is_in_cache(key):
            return self.cache[key].value
        raise Exception("Value could not be found")

    def add_cache_entry(self,
                        key: int,
                        value: Any,
                        expires_every: str,
                        schedule: str
                        ) -> None:
        if key not in self.cache:
            key_list = list(self.cache.keys())
            if len(key_list) >= self.max_cache_entries:
                del self.cache[key_list[0]]

            self.cache[key] = CacheEntry()
            self.cache[key].set_expiry(expires_every, schedule)
        self.cache[key].value = value


class DataCache:
    __metaclass__ = Singleton

    def __init__(self):
        self.cache: Dict[Callable, FunctionCache] = {}

    @staticmethod
    def hash_args(args: Tuple[Any], kwargs: Dict[str, Any]) -> int:
        hash_key = ()
        for value in args:
            if isinstance(value, Hashable):
                hash_key += (value,)
            else:
                hash_key += (id(value),)

        for key in (sorted(kwargs.keys())):
            value = kwargs[key]

            if isinstance(value, Hashable):
                hash_key += (key, value,)
            else:
                hash_key += (key, id(value),)

        return hash(hash_key)

    def is_in_cache(self, key: int, func: Callable) -> bool:
        return func in self.cache and \
               self.cache[func].is_in_cache(key)

    def get_value_from_cache(self, key: int, func: Callable) -> Any:
        if self.is_in_cache(key, func):
            return self.cache[func].get_value_from_cache(key)
        raise Exception("Value could not be found")

    def add_function_cache(self, func: Callable, function_cache: FunctionCache) -> None:
        if func not in self.cache:
            self.cache[func] = function_cache
        else:
            raise Exception("Function is already in cache")


def cache(expires_every: str = None, schedule: str = None, max_cache_size=50) -> Callable:
    """
    Cache the results of a method or function with the arguments of the function
    :param expires_every: A string which specifies every how many hours/minutes/seconds the cache expires
                          Format: hh:mm:ss | h:mm:s | ...
                          Use * if you dont want to specify.
    :param schedule: A string which describes a schedule
                     Format: hh:mm:ss
                     For example a string like this `**:30:00` will cause the cache to expire every hour at 30 past.
                     For example a string like this `18:30:00` will cause the cache to expire every day at 18:30:00
    :param max_cache_size: The maximal amount of cache results per method which should be cached
    """

    data_cache = DataCache()

    if max_cache_size < 1:
        raise Exception("Max cache size cannot be smaller than 1")

    def function_wrapper(func: Callable):
        func_cache = FunctionCache(max_cache_size)
        data_cache.add_function_cache(func, func_cache)

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            key = DataCache.hash_args(args, kwargs)
            if data_cache.is_in_cache(key, func):
                value = data_cache.get_value_from_cache(key, func)
            else:
                value = func(*args, **kwargs)
                func_cache.add_cache_entry(key, value, expires_every, schedule)
            return value

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            key = DataCache.hash_args(args, kwargs)
            if data_cache.is_in_cache(key, func):
                value = data_cache.get_value_from_cache(key, func)
            else:
                value = await func(*args, **kwargs)
                func_cache.add_cache_entry(key, value, expires_every, schedule)
            return value

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return function_wrapper
