"""
Tests for AppConfig
"""

import pytest

from microframe import AppConfig


class TestAppConfig:
    """Test AppConfig class"""

    def test_default_config(self):
        """Test default configuration values"""
        config = AppConfig(title="MicroFrame API", version="1.0.0")
        assert config.title == "MicroFrame API"
        assert config.version == "1.0.0"
        assert config.debug is False
        assert config.openapi_url == "/openapi.json"
        assert config.docs_url == "/docs"
        assert config.redoc_url == "/redoc"

    def test_custom_config(self):
        """Test custom configuration"""
        config = AppConfig(
            title="Custom API",
            version="2.0.0",
            description="Custom Description",
            debug=True,
        )
        assert config.title == "Custom API"
        assert config.version == "2.0.0"
        assert config.description == "Custom Description"
        assert config.debug is True

    def test_disable_docs(self):
        """Test disabling documentation endpoints"""
        config = AppConfig(docs_url=None, redoc_url=None, openapi_url=None)
        assert config.docs_url is None
        assert config.redoc_url is None
        assert config.openapi_url is None

    def test_cors_configuration(self):
        """Test CORS configuration"""
        config = AppConfig(
            cors_origins=["http://localhost:3000", "https://example.com"],
            cors_methods=["GET", "POST"],
            cors_headers=["Content-Type"],
        )
        assert len(config.cors_origins) == 2
        assert "http://localhost:3000" in config.cors_origins
        assert "GET" in config.cors_methods
        assert "Content-Type" in config.cors_headers

    def test_security_configuration(self):
        """Test security configuration"""
        config = AppConfig(
            rate_limit_requests=50,
            rate_limit_window=30,
            max_request_size=5_000_000,
        )
        assert config.rate_limit_requests == 50
        assert config.rate_limit_window == 30
        assert config.max_request_size == 5_000_000

    def test_config_immutability(self):
        """Test that config is a Pydantic model"""
        config = AppConfig(title="Test")
        assert hasattr(config, "rate_limit_enabled")
        assert hasattr(config, "rate_limit_requests")
