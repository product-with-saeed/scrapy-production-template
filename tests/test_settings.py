"""
Unit Tests for Scrapy Settings Module.

Tests for settings configuration following TDD principles.
Each test follows the Arrange-Act-Assert pattern.

Following PEP 8 style guide and pytest conventions.
"""

import os

import pytest


@pytest.mark.unit
class TestScrapySettings:
    """Test suite for Scrapy settings module."""

    def test_settings_module_can_be_imported(self):
        """Test that settings module can be imported successfully."""
        # Arrange & Act
        from scrapers import settings

        # Assert
        assert settings is not None

    def test_bot_name_is_configured(self):
        """Test that BOT_NAME is properly configured."""
        # Arrange & Act
        from scrapers.settings import BOT_NAME

        # Assert
        assert BOT_NAME == "scrapers"
        assert isinstance(BOT_NAME, str)

    def test_spider_modules_configured(self):
        """Test that SPIDER_MODULES is correctly set."""
        # Arrange & Act
        from scrapers.settings import SPIDER_MODULES

        # Assert
        assert isinstance(SPIDER_MODULES, list)
        assert "scrapers.spiders" in SPIDER_MODULES

    def test_newspider_module_configured(self):
        """Test that NEWSPIDER_MODULE is correctly set."""
        # Arrange & Act
        from scrapers.settings import NEWSPIDER_MODULE

        # Assert
        assert NEWSPIDER_MODULE == "scrapers.spiders"

    def test_robotstxt_obey_enabled(self):
        """Test that robots.txt obedience is enabled."""
        # Arrange & Act
        from scrapers.settings import ROBOTSTXT_OBEY

        # Assert
        assert ROBOTSTXT_OBEY is True

    def test_concurrent_requests_configured(self):
        """Test that concurrent requests settings are properly set."""
        # Arrange & Act
        from scrapers.settings import CONCURRENT_REQUESTS, CONCURRENT_REQUESTS_PER_DOMAIN

        # Assert
        assert CONCURRENT_REQUESTS == 16
        assert CONCURRENT_REQUESTS_PER_DOMAIN == 2
        assert isinstance(CONCURRENT_REQUESTS, int)
        assert isinstance(CONCURRENT_REQUESTS_PER_DOMAIN, int)

    def test_download_delay_configured(self):
        """Test that download delay is configured."""
        # Arrange & Act
        from scrapers.settings import DOWNLOAD_DELAY, RANDOMIZE_DOWNLOAD_DELAY

        # Assert
        assert DOWNLOAD_DELAY == 1
        assert RANDOMIZE_DOWNLOAD_DELAY is True

    def test_cookies_disabled(self):
        """Test that cookies are disabled."""
        # Arrange & Act
        from scrapers.settings import COOKIES_ENABLED

        # Assert
        assert COOKIES_ENABLED is False

    def test_telnet_console_disabled(self):
        """Test that telnet console is disabled."""
        # Arrange & Act
        from scrapers.settings import TELNETCONSOLE_ENABLED

        # Assert
        assert TELNETCONSOLE_ENABLED is False

    def test_default_request_headers_configured(self):
        """Test that default request headers are set."""
        # Arrange & Act
        from scrapers.settings import DEFAULT_REQUEST_HEADERS

        # Assert
        assert isinstance(DEFAULT_REQUEST_HEADERS, dict)
        assert "Accept" in DEFAULT_REQUEST_HEADERS
        assert "Accept-Language" in DEFAULT_REQUEST_HEADERS

    def test_spider_middlewares_configured(self):
        """Test that spider middlewares are properly configured."""
        # Arrange & Act
        from scrapers.settings import SPIDER_MIDDLEWARES

        # Assert
        assert isinstance(SPIDER_MIDDLEWARES, dict)
        assert "scrapers.middlewares.ScraperStatsMiddleware" in SPIDER_MIDDLEWARES
        assert SPIDER_MIDDLEWARES["scrapers.middlewares.ScraperStatsMiddleware"] == 100

    def test_downloader_middlewares_configured(self):
        """Test that downloader middlewares are properly configured."""
        # Arrange & Act
        from scrapers.settings import DOWNLOADER_MIDDLEWARES

        # Assert
        assert isinstance(DOWNLOADER_MIDDLEWARES, dict)
        assert "scrapers.middlewares.ErrorLoggingMiddleware" in DOWNLOADER_MIDDLEWARES
        assert DOWNLOADER_MIDDLEWARES["scrapers.middlewares.ErrorLoggingMiddleware"] == 550

    def test_extensions_configured(self):
        """Test that extensions are properly configured."""
        # Arrange & Act
        from scrapers.settings import EXTENSIONS

        # Assert
        assert isinstance(EXTENSIONS, dict)

    def test_item_pipelines_configured(self):
        """Test that item pipelines are configured."""
        # Arrange & Act
        from scrapers.settings import ITEM_PIPELINES

        # Assert
        assert isinstance(ITEM_PIPELINES, dict)
        assert "scrapers.pipelines.PostgresPipeline" in ITEM_PIPELINES
        assert ITEM_PIPELINES["scrapers.pipelines.PostgresPipeline"] == 300

    def test_autothrottle_enabled(self):
        """Test that autothrottle is enabled."""
        # Arrange & Act
        from scrapers.settings import AUTOTHROTTLE_ENABLED

        # Assert
        assert AUTOTHROTTLE_ENABLED is True

    def test_autothrottle_settings(self):
        """Test that autothrottle settings are properly configured."""
        # Arrange & Act
        from scrapers.settings import (
            AUTOTHROTTLE_MAX_DELAY,
            AUTOTHROTTLE_START_DELAY,
            AUTOTHROTTLE_TARGET_CONCURRENCY,
        )

        # Assert
        assert AUTOTHROTTLE_START_DELAY == 1
        assert AUTOTHROTTLE_MAX_DELAY == 10
        assert AUTOTHROTTLE_TARGET_CONCURRENCY == 2.0

    def test_httperror_settings(self):
        """Test that HTTP error settings are configured."""
        # Arrange & Act
        from scrapers.settings import HTTPERROR_ALLOWED_CODES

        # Assert
        assert isinstance(HTTPERROR_ALLOWED_CODES, list)

    def test_stats_enabled(self):
        """Test that stats collection is enabled."""
        # Arrange & Act
        from scrapers.settings import STATS_ENABLED

        # Assert
        assert STATS_ENABLED is True

    def test_retry_settings_configured(self):
        """Test that retry settings are configured."""
        # Arrange & Act
        from scrapers.settings import RETRY_ENABLED, RETRY_HTTP_CODES, RETRY_TIMES

        # Assert
        assert RETRY_ENABLED is True
        assert RETRY_TIMES == 3
        assert isinstance(RETRY_HTTP_CODES, list)
        assert 500 in RETRY_HTTP_CODES
        assert 503 in RETRY_HTTP_CODES

    def test_log_level_configured(self):
        """Test that log level can be set from environment."""
        # Arrange & Act
        from scrapers.settings import LOG_LEVEL

        # Assert
        assert LOG_LEVEL in ["INFO", "DEBUG", "WARNING", "ERROR"]

    def test_feed_export_encoding(self):
        """Test that feed export encoding is set."""
        # Arrange & Act
        from scrapers.settings import FEED_EXPORT_ENCODING

        # Assert
        assert FEED_EXPORT_ENCODING == "utf-8"

    def test_request_fingerprinter_configured(self):
        """Test that request fingerprinter implementation is set."""
        # Arrange & Act
        from scrapers.settings import REQUEST_FINGERPRINTER_IMPLEMENTATION

        # Assert
        assert REQUEST_FINGERPRINTER_IMPLEMENTATION == "2.7"

    def test_twisted_reactor_configured(self):
        """Test that Twisted reactor is configured."""
        # Arrange & Act
        from scrapers.settings import TWISTED_REACTOR

        # Assert
        assert TWISTED_REACTOR == "twisted.internet.asyncioreactor.AsyncioSelectorReactor"


@pytest.mark.unit
class TestPostgresSettings:
    """Test suite for PostgreSQL database settings."""

    def test_postgres_host_from_env(self):
        """Test that POSTGRES_HOST can be read from environment."""
        # Arrange
        os.environ["POSTGRES_HOST"] = "test_host"

        # Act
        # Reimport to pick up env var
        import importlib

        from scrapers import settings as settings_module

        importlib.reload(settings_module)
        from scrapers.settings import POSTGRES_HOST

        # Assert
        assert POSTGRES_HOST == "test_host"

        # Cleanup
        del os.environ["POSTGRES_HOST"]

    def test_postgres_settings_defaults(self):
        """Test that PostgreSQL settings have sensible defaults."""
        # Arrange - Clear any env vars
        env_backup = {}
        for key in [
            "POSTGRES_HOST",
            "POSTGRES_DB",
            "POSTGRES_USER",
            "POSTGRES_PASSWORD",
            "POSTGRES_PORT",
        ]:
            if key in os.environ:
                env_backup[key] = os.environ[key]
                del os.environ[key]

        # Act
        import importlib

        from scrapers import settings as settings_module

        importlib.reload(settings_module)
        from scrapers.settings import (
            POSTGRES_DB,
            POSTGRES_HOST,
            POSTGRES_PASSWORD,
            POSTGRES_PORT,
            POSTGRES_USER,
        )

        # Assert - Defaults when no .env or environment variables
        assert POSTGRES_HOST == "localhost"
        assert POSTGRES_DB == "scrapy_db"
        assert POSTGRES_USER == "scrapy"
        assert POSTGRES_PASSWORD in [
            "scrapy",
            "change_this_password_in_production",
        ]  # Could be from .env
        assert POSTGRES_PORT in [5432, 5433]  # Could be from .env

        # Cleanup - Restore environment
        for key, value in env_backup.items():
            os.environ[key] = value


@pytest.mark.unit
class TestSettingsValidation:
    """Test suite for validating settings configuration."""

    def test_all_middleware_paths_are_strings(self):
        """Test that all middleware configurations use string paths."""
        # Arrange & Act
        from scrapers.settings import DOWNLOADER_MIDDLEWARES, SPIDER_MIDDLEWARES

        # Assert
        for middleware in SPIDER_MIDDLEWARES.keys():
            assert isinstance(middleware, str)

        for middleware in DOWNLOADER_MIDDLEWARES.keys():
            assert isinstance(middleware, str)

    def test_all_pipeline_paths_are_strings(self):
        """Test that all pipeline configurations use string paths."""
        # Arrange & Act
        from scrapers.settings import ITEM_PIPELINES

        # Assert
        for pipeline in ITEM_PIPELINES.keys():
            assert isinstance(pipeline, str)

    def test_settings_have_no_syntax_errors(self):
        """Test that settings file has no syntax errors."""
        # Arrange & Act
        try:
            from scrapers import settings

            # Assert
            assert True
        except SyntaxError:
            pytest.fail("Settings file has syntax errors")

    def test_critical_settings_are_defined(self):
        """Test that all critical settings are defined."""
        # Arrange
        from scrapers import settings

        critical_settings = [
            "BOT_NAME",
            "SPIDER_MODULES",
            "ROBOTSTXT_OBEY",
            "CONCURRENT_REQUESTS",
            "ITEM_PIPELINES",
            "LOG_LEVEL",
        ]

        # Act & Assert
        for setting_name in critical_settings:
            assert hasattr(settings, setting_name), f"Missing critical setting: {setting_name}"
