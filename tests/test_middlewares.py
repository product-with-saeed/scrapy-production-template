"""
Unit Tests for Scrapy Middlewares.

Tests for ScraperStatsMiddleware and ErrorLoggingMiddleware following TDD principles.
Each test follows the Arrange-Act-Assert pattern.

Following PEP 8 style guide and pytest conventions.
"""

from unittest.mock import MagicMock, Mock, call, patch

import pytest
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse, Request
from twisted.python.failure import Failure

from scrapers.middlewares import ErrorLoggingMiddleware, ScraperStatsMiddleware


# ============================================================================
# ScraperStatsMiddleware Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.middleware
class TestScraperStatsMiddleware:
    """Test suite for ScraperStatsMiddleware."""

    def test_middleware_initialization(self):
        """Test that middleware can be initialized with stats."""
        # Arrange
        mock_stats = Mock()

        # Act
        middleware = ScraperStatsMiddleware(mock_stats)

        # Assert
        assert middleware is not None
        assert middleware.stats == mock_stats

    def test_from_crawler_creates_middleware(self):
        """Test that from_crawler creates middleware instance."""
        # Arrange
        mock_crawler = Mock()
        mock_crawler.stats = Mock()
        mock_crawler.settings.getbool.return_value = True

        # Act
        middleware = ScraperStatsMiddleware.from_crawler(mock_crawler)

        # Assert
        assert middleware is not None
        assert isinstance(middleware, ScraperStatsMiddleware)
        mock_crawler.settings.getbool.assert_called_once_with("STATS_ENABLED", True)

    def test_from_crawler_raises_not_configured_when_stats_disabled(self):
        """Test that middleware raises NotConfigured when stats are disabled."""
        # Arrange
        mock_crawler = Mock()
        mock_crawler.settings.getbool.return_value = False

        # Act & Assert
        with pytest.raises(NotConfigured):
            ScraperStatsMiddleware.from_crawler(mock_crawler)

    def test_from_crawler_connects_signals(self):
        """Test that from_crawler connects all required signals."""
        # Arrange
        mock_crawler = Mock()
        mock_crawler.stats = Mock()
        mock_crawler.settings.getbool.return_value = True

        # Act
        middleware = ScraperStatsMiddleware.from_crawler(mock_crawler)

        # Assert
        assert mock_crawler.signals.connect.call_count == 3
        # Verify signals were connected
        calls = mock_crawler.signals.connect.call_args_list
        signal_types = [call[1]["signal"] for call in calls]
        assert signals.spider_opened in signal_types
        assert signals.spider_closed in signal_types
        assert signals.item_scraped in signal_types

    def test_spider_opened_logs_spider_name(self, caplog):
        """Test that spider_opened logs the spider name."""
        # Arrange
        mock_stats = Mock()
        middleware = ScraperStatsMiddleware(mock_stats)
        mock_spider = Mock()
        mock_spider.name = "test_spider"

        # Act
        with caplog.at_level("INFO"):
            middleware.spider_opened(mock_spider)

        # Assert
        assert "Spider opened: test_spider" in caplog.text

    def test_spider_closed_logs_statistics(self, caplog):
        """Test that spider_closed logs comprehensive statistics."""
        # Arrange
        mock_stats = Mock()
        mock_stats.get_stats.return_value = {
            "item_scraped_count": 100,
            "response_received_count": 50,
            "log_count/ERROR": 2,
        }
        middleware = ScraperStatsMiddleware(mock_stats)
        mock_spider = Mock()
        mock_spider.name = "test_spider"

        # Act
        with caplog.at_level("INFO"):
            middleware.spider_closed(mock_spider, "finished")

        # Assert
        log_text = caplog.text
        assert "Spider closed: test_spider" in log_text
        assert "Reason: finished" in log_text
        assert "Items scraped: 100" in log_text
        assert "Pages crawled: 50" in log_text
        assert "Errors: 2" in log_text

    def test_spider_closed_handles_missing_stats(self, caplog):
        """Test that spider_closed handles missing stats gracefully."""
        # Arrange
        mock_stats = Mock()
        mock_stats.get_stats.return_value = {}
        middleware = ScraperStatsMiddleware(mock_stats)
        mock_spider = Mock()
        mock_spider.name = "test_spider"

        # Act
        with caplog.at_level("INFO"):
            middleware.spider_closed(mock_spider, "finished")

        # Assert
        log_text = caplog.text
        assert "Items scraped: 0" in log_text
        assert "Pages crawled: 0" in log_text
        assert "Errors: 0" in log_text

    def test_item_scraped_executes_without_error(self):
        """Test that item_scraped method can be called without error."""
        # Arrange
        mock_stats = Mock()
        middleware = ScraperStatsMiddleware(mock_stats)
        mock_item = {"test": "data"}
        mock_spider = Mock()

        # Act - should not raise any exceptions
        middleware.item_scraped(mock_item, mock_spider)

        # Assert - method executes successfully
        assert True  # No exception raised


# ============================================================================
# ErrorLoggingMiddleware Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.middleware
class TestErrorLoggingMiddleware:
    """Test suite for ErrorLoggingMiddleware."""

    def test_middleware_initialization(self):
        """Test that middleware can be initialized."""
        # Arrange & Act
        middleware = ErrorLoggingMiddleware()

        # Assert
        assert middleware is not None
        assert hasattr(middleware, "logger")

    def test_from_crawler_creates_middleware(self):
        """Test that from_crawler creates middleware instance."""
        # Arrange
        mock_crawler = Mock()

        # Act
        middleware = ErrorLoggingMiddleware.from_crawler(mock_crawler)

        # Assert
        assert middleware is not None
        assert isinstance(middleware, ErrorLoggingMiddleware)

    def test_from_crawler_connects_spider_error_signal(self):
        """Test that from_crawler connects spider_error signal."""
        # Arrange
        mock_crawler = Mock()

        # Act
        middleware = ErrorLoggingMiddleware.from_crawler(mock_crawler)

        # Assert
        mock_crawler.signals.connect.assert_called_once()
        call_args = mock_crawler.signals.connect.call_args
        assert call_args[1]["signal"] == signals.spider_error

    def test_spider_error_logs_error_details(self, caplog):
        """Test that spider_error logs comprehensive error information."""
        # Arrange
        middleware = ErrorLoggingMiddleware()
        mock_spider = Mock()
        mock_spider.name = "test_spider"

        # Create a mock failure
        mock_failure = Mock()
        mock_failure.getErrorMessage.return_value = "Test error message"

        # Create a mock response
        mock_response = Mock()
        mock_response.url = "http://example.com/test"

        # Act
        with caplog.at_level("ERROR"):
            middleware.spider_error(mock_failure, mock_response, mock_spider)

        # Assert
        log_text = caplog.text
        assert "Error in test_spider" in log_text
        assert "Test error message" in log_text
        assert "http://example.com/test" in log_text

    def test_spider_error_handles_different_error_types(self, caplog):
        """Test that spider_error handles various error messages."""
        # Arrange
        middleware = ErrorLoggingMiddleware()
        mock_spider = Mock()
        mock_spider.name = "test_spider"
        mock_response = Mock()
        mock_response.url = "http://example.com"

        error_messages = [
            "Connection timeout",
            "404 Not Found",
            "500 Internal Server Error",
            "DNS lookup failed",
        ]

        for error_msg in error_messages:
            # Arrange
            mock_failure = Mock()
            mock_failure.getErrorMessage.return_value = error_msg

            # Act
            with caplog.at_level("ERROR"):
                middleware.spider_error(mock_failure, mock_response, mock_spider)

            # Assert
            assert error_msg in caplog.text


# ============================================================================
# Middleware Integration Tests
# ============================================================================


@pytest.mark.integration
@pytest.mark.middleware
class TestMiddlewareIntegration:
    """Integration tests for middleware interaction."""

    def test_stats_middleware_full_lifecycle(self, caplog):
        """Test complete lifecycle of stats middleware."""
        # Arrange
        mock_stats = Mock()
        mock_stats.get_stats.return_value = {
            "item_scraped_count": 10,
            "response_received_count": 5,
            "log_count/ERROR": 0,
        }
        middleware = ScraperStatsMiddleware(mock_stats)
        mock_spider = Mock()
        mock_spider.name = "integration_spider"
        mock_item = {"data": "test"}

        # Act
        with caplog.at_level("INFO"):
            middleware.spider_opened(mock_spider)
            middleware.item_scraped(mock_item, mock_spider)
            middleware.spider_closed(mock_spider, "finished")

        # Assert
        log_text = caplog.text
        assert "Spider opened: integration_spider" in log_text
        assert "Spider closed: integration_spider" in log_text
        assert "Items scraped: 10" in log_text

    def test_error_middleware_with_crawler_signals(self):
        """Test error middleware with crawler signal connection."""
        # Arrange
        mock_crawler = Mock()
        middleware = ErrorLoggingMiddleware.from_crawler(mock_crawler)

        # Act
        signal_handler = mock_crawler.signals.connect.call_args[0][0]

        # Assert
        assert signal_handler == middleware.spider_error
        assert callable(signal_handler)

    def test_both_middlewares_can_coexist(self):
        """Test that both middlewares can be instantiated together."""
        # Arrange
        mock_crawler = Mock()
        mock_crawler.stats = Mock()
        mock_crawler.settings.getbool.return_value = True

        # Act
        stats_middleware = ScraperStatsMiddleware.from_crawler(mock_crawler)
        error_middleware = ErrorLoggingMiddleware.from_crawler(mock_crawler)

        # Assert
        assert stats_middleware is not None
        assert error_middleware is not None
        assert isinstance(stats_middleware, ScraperStatsMiddleware)
        assert isinstance(error_middleware, ErrorLoggingMiddleware)


# ============================================================================
# Edge Case Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.middleware
class TestMiddlewareEdgeCases:
    """Test edge cases and error conditions."""

    def test_stats_middleware_with_none_stats(self):
        """Test stats middleware behavior with None stats values."""
        # Arrange
        mock_stats = Mock()
        mock_stats.get_stats.return_value = {
            "item_scraped_count": None,
            "response_received_count": None,
        }
        middleware = ScraperStatsMiddleware(mock_stats)
        mock_spider = Mock()
        mock_spider.name = "test"

        # Act & Assert - should not raise error
        middleware.spider_closed(mock_spider, "finished")

    def test_error_middleware_with_empty_error_message(self, caplog):
        """Test error middleware with empty error message."""
        # Arrange
        middleware = ErrorLoggingMiddleware()
        mock_spider = Mock()
        mock_spider.name = "test"
        mock_failure = Mock()
        mock_failure.getErrorMessage.return_value = ""
        mock_response = Mock()
        mock_response.url = "http://example.com"

        # Act
        with caplog.at_level("ERROR"):
            middleware.spider_error(mock_failure, mock_response, mock_spider)

        # Assert
        # Should still log even with empty message
        assert "Error in test" in caplog.text

    def test_stats_middleware_with_multiple_spider_instances(self, caplog):
        """Test that middleware can handle multiple spider instances."""
        # Arrange
        mock_stats = Mock()
        mock_stats.get_stats.return_value = {"item_scraped_count": 5}
        middleware = ScraperStatsMiddleware(mock_stats)

        # Create spiders with proper name attributes
        spiders = []
        for i in range(3):
            spider = Mock()
            spider.name = f"spider_{i}"
            spiders.append(spider)

        # Act
        with caplog.at_level("INFO"):
            for spider in spiders:
                middleware.spider_opened(spider)
                middleware.spider_closed(spider, "finished")

        # Assert
        for i in range(3):
            assert f"Spider opened: spider_{i}" in caplog.text
            assert f"Spider closed: spider_{i}" in caplog.text

    def test_from_crawler_with_custom_settings(self):
        """Test from_crawler with custom STATS_ENABLED setting."""
        # Arrange
        mock_crawler = Mock()
        mock_crawler.stats = Mock()

        # Test with stats enabled
        mock_crawler.settings.getbool.return_value = True
        middleware = ScraperStatsMiddleware.from_crawler(mock_crawler)
        assert middleware is not None

        # Test with stats disabled
        mock_crawler.settings.getbool.return_value = False
        with pytest.raises(NotConfigured):
            ScraperStatsMiddleware.from_crawler(mock_crawler)
