import time
from abc import ABC, abstractmethod
from typing import Any, Optional


class CacheBackend(ABC):
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
    """In-memory cache with TTL support."""

    def __init__(self):
        self._store: dict = {}
        self._timestamps: dict = {}

    def get(self, key: str, ttl: Optional[int] = None) -> Optional[Any]:
        if key not in self._store:
            return None
        if ttl and key in self._timestamps:
            if time.time() - self._timestamps[key] > ttl:
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
