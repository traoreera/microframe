import logging
from typing import Dict

import httpx
from markupsafe import Markup

logger = logging.getLogger(__name__)


class MFEClient:
    """Manages micro-frontend registrations and async fetching."""

    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout
        self._registry: Dict[str, str] = {}

    def register(self, name: str, url: str):
        self._registry[name] = url
        logger.info(f"MFE '{name}' -> {url}")

    def register_many(self, mfes: Dict[str, str]):
        for name, url in mfes.items():
            self.register(name, url)

    async def fetch(self, name: str, **kwargs) -> str:
        url = self._registry.get(name)
        if not url:
            logger.warning(f"MFE '{name}' not registered")
            return f"<!-- MFE '{name}' not found -->"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=kwargs)
                response.raise_for_status()
                return Markup(response.text)
        except httpx.TimeoutException:
            logger.error(f"MFE '{name}' timeout after {self.timeout}s")
            return f"<!-- MFE '{name}' timeout -->"
        except httpx.HTTPError as e:
            logger.error(f"MFE '{name}' HTTP error: {e}")
            return f"<!-- MFE '{name}' error: {e} -->"
        except Exception:
            logger.exception(f"MFE '{name}' unexpected error")
            return f"<!-- MFE '{name}' error -->"
