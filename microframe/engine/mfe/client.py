import logging
from typing import Dict

import httpx
from markupsafe import Markup

logger = logging.getLogger(__name__)


class MFEClient:
    """Manages micro-frontend registrations and async fetching.

    Fetches HTML fragments from external HTTP services at render time.
    Fragments are fetched concurrently (per-template) and errors produce
    HTML comments instead of breaking the page.

    Usage:
        client = MFEClient(timeout=5.0)
        client.register("header", "http://header-service/fragment")
        html = await client.fetch("header", user_id=42)
    """

    def __init__(self, timeout: float = 5.0):
        """Initialize the MFE client.

        Args:
            timeout: HTTP request timeout in seconds.
        """
        self.timeout = timeout
        self._registry: Dict[str, str] = {}

    def register(self, name: str, url: str):
        """Register a micro-frontend fragment URL.

        Args:
            name: Short name used in templates (e.g. ``"header"``).
            url: Full URL to the fragment endpoint.
        """
        self._registry[name] = url
        logger.info(f"MFE '{name}' -> {url}")

    def register_many(self, mfes: Dict[str, str]):
        """Register multiple micro-frontends at once.

        Args:
            mfes: Dict mapping names to URLs.
        """
        for name, url in mfes.items():
            self.register(name, url)

    async def fetch(self, name: str, **kwargs) -> str:
        """Fetch a micro-frontend fragment.

        Sends a GET request to the registered URL with kwargs as query
        parameters. Returns the response body as safe HTML, or an HTML
        comment on error.

        Args:
            name: Registered fragment name.
            **kwargs: Query parameters forwarded to the fragment URL.

        Returns:
            The fragment HTML (Markup safe), or a comment on error.
        """
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
