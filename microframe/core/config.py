"""
Core configuration management
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class AppConfig:
    """Application configuration"""

    title: str = "MicroFramework"
    version: str = "1.0.0"
    description: str = ""
    debug: bool = False

    # OpenAPI configuration
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"
    include_in_schema: bool = True

    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8000

    # Security
    secret_key: Optional[str] = None
    allowed_hosts: list = field(default_factory=lambda: ["*"])

    # CORS
    cors_origins: list = field(default_factory=lambda: ["*"])
    cors_methods: list = field(default_factory=lambda: ["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    cors_headers: list = field(default_factory=lambda: ["*"])
    middleware: list = field(default_factory=lambda: [])

    # Rate limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_window: int = 60

    # Payload limits
    max_request_size: int = 10_000_000  # 10MB

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "title": self.title,
            "version": self.version,
            "description": self.description,
            "debug": self.debug,
        }
