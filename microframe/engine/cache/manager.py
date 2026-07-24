import time
from abc import ABC, abstractmethod
from typing import Any, Optional


class CacheBackend(ABC):
    """Abstract base class for cache backends.

    Implement this to plug Redis, Memcached, filesystem, etc.

    Methods may be sync (return the value directly, like CacheManager below)
    or async (return a coroutine, like a backend bridging to an async cache
    service). TemplateEngine awaits the result either way via `_maybe_await`,
    so an async-native backend never needs to fake sync behavior with
    `asyncio.run()` — which would deadlock when called from inside the
    running event loop that render() already executes in.
    """

    @abstractmethod
    def get(self, key: str, ttl: Optional[int] = None) -> Optional[Any]:
        pass

    @abstractmethod
    def set(self, key: str, value: Any):
        pass

    @abstractmethod
    def delete(self, key: str):
        pass

    @abstractmethod
    def clear(self):
        pass


class CacheManager(CacheBackend):
    """In-memory cache with TTL support.

    Default backend used by TemplateEngine. Stores values in a dict
    with insertion timestamps for expiration checks.

    Usage:
        cache = CacheManager()
        cache.set("mykey", "<html>...</html>")
        value = cache.get("mykey", ttl=300)  # None if expired
        cache.delete("mykey")
        cache.clear()
    """

    def __init__(self):
        self._store: dict = {}
        self._timestamps: dict = {}

    def get(self, key: str, ttl: Optional[int] = 300) -> Optional[Any]:
        if key not in self._store:
            return None
        if ttl and key in self._timestamps and time.time() - self._timestamps[key] > ttl:
            self.delete(key)
            return None
        return self._store[key]

    def set(self, key: str, value: Any):
        self._store[key] = value
        self._timestamps[key] = time.time()

    def delete(self, key: str):
        self._store.pop(key, None)
        self._timestamps.pop(key, None)

    def clear(self):
        self._store.clear()
        self._timestamps.clear()
