"""
Pytest Configuration and Fixtures for Scrapy Production Template.

This module provides reusable fixtures for testing spiders, pipelines,
and items following TDD and OOP best practices.

Following PEP 8 and pytest conventions.
"""

from datetime import datetime
from unittest.mock import MagicMock, Mock

import pytest
from scrapy.http import HtmlResponse, Request, TextResponse

from scrapers.items import BookItem, HackerNewsItem, QuoteItem


# ============================================================================
# Spider Fixtures
# ============================================================================


@pytest.fixture
def mock_spider():
    """
    Create a mock Scrapy spider instance.

    Returns:
        Mock: A mock spider with name attribute.
    """
    spider = Mock()
    spider.name = "test_spider"
    return spider


@pytest.fixture
def hackernews_spider():
    """
    Create a HackerNews spider mock.

    Returns:
        Mock: A mock spider configured for HackerNews.
    """
    spider = Mock()
    spider.name = "hackernews"
    return spider


@pytest.fixture
def quotes_spider():
    """
    Create a Quotes spider mock.

    Returns:
        Mock: A mock spider configured for Quotes.
    """
    spider = Mock()
    spider.name = "quotes"
    return spider


@pytest.fixture
def books_spider():
    """
    Create a Books spider mock.

    Returns:
        Mock: A mock spider configured for Books.
    """
    spider = Mock()
    spider.name = "books"
    return spider


# ============================================================================
# HTTP Response Fixtures
# ============================================================================


@pytest.fixture
def sample_request():
    """
    Create a sample Scrapy Request object.

    Returns:
        Request: A basic request to example.com.
    """
    return Request(url="http://example.com")


@pytest.fixture
def sample_html_response(sample_request):
    """
    Create a sample HTML response for testing spider parsing.

    Args:
        sample_request: Request fixture.

    Returns:
        HtmlResponse: A basic HTML response.
    """
    html_content = """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Test Heading</h1>
            <p class="content">Test paragraph</p>
        </body>
    </html>
    """
    return HtmlResponse(
        url="http://example.com",
        request=sample_request,
        body=html_content.encode("utf-8"),
        encoding="utf-8",
    )


@pytest.fixture
def hackernews_response(sample_request):
    """
    Create a mock HackerNews HTML response.

    Args:
        sample_request: Request fixture.

    Returns:
        HtmlResponse: A response mimicking HackerNews structure.
    """
    html_content = """
    <html>
        <body>
            <table class="itemlist">
                <tr class="athing" id="12345">
                    <td class="rank">1.</td>
                    <td class="title">
                        <span class="titleline">
                            <a href="https://example.com/article">Test Article</a>
                        </span>
                    </td>
                </tr>
                <tr>
                    <td colspan="2"></td>
                    <td class="subtext">
                        <span class="score" id="score_12345">100 points</span>
                        by <a href="user?id=testuser" class="hnuser">testuser</a>
                        <a href="item?id=12345">50&nbsp;comments</a>
                    </td>
                </tr>
            </table>
        </body>
    </html>
    """
    return HtmlResponse(
        url="https://news.ycombinator.com",
        request=sample_request,
        body=html_content.encode("utf-8"),
        encoding="utf-8",
    )


# ============================================================================
# Item Fixtures
# ============================================================================


@pytest.fixture
def sample_hackernews_item():
    """
    Create a sample HackerNews item for testing.

    Returns:
        HackerNewsItem: A populated HackerNews item.
    """
    item = HackerNewsItem()
    item["title"] = "Test Article"
    item["url"] = "https://example.com/article"
    item["rank"] = "1"
    item["score"] = "100"
    item["author"] = "testuser"
    item["comments"] = "50"
    item["item_id"] = "12345"
    item["scraped_at"] = datetime.now()
    return item


@pytest.fixture
def sample_quote_item():
    """
    Create a sample Quote item for testing.

    Returns:
        QuoteItem: A populated Quote item.
    """
    item = QuoteItem()
    item["text"] = "Test quote text"
    item["author"] = "Test Author"
    item["tags"] = ["inspiration", "life"]
    item["scraped_at"] = datetime.now()
    return item


@pytest.fixture
def sample_book_item():
    """
    Create a sample Book item for testing.

    Returns:
        BookItem: A populated Book item.
    """
    item = BookItem()
    item["title"] = "Test Book"
    item["price"] = "£51.77"
    item["availability"] = "In stock"
    item["rating"] = "Four"
    item["url"] = "https://example.com/book"
    item["scraped_at"] = datetime.now()
    return item


# ============================================================================
# Database Fixtures (Mocked)
# ============================================================================


@pytest.fixture
def mock_db_config():
    """
    Provide mock database configuration.

    Returns:
        dict: Database configuration dictionary.
    """
    return {
        "host": "localhost",
        "database": "test_db",
        "user": "test_user",
        "password": "test_password",
        "port": 5432,
    }


@pytest.fixture
def mock_db_connection(mocker):
    """
    Create a mocked PostgreSQL database connection.

    Args:
        mocker: pytest-mock fixture.

    Returns:
        Mock: Mocked psycopg2 connection.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mocker.patch("psycopg2.connect", return_value=mock_conn)
    return mock_conn


@pytest.fixture
def mock_db_cursor(mock_db_connection):
    """
    Create a mocked database cursor.

    Args:
        mock_db_connection: Mocked connection fixture.

    Returns:
        Mock: Mocked cursor object.
    """
    return mock_db_connection.cursor.return_value


# ============================================================================
# Scrapy Crawler Fixtures
# ============================================================================


@pytest.fixture
def mock_crawler_settings():
    """
    Create mock Scrapy crawler settings.

    Returns:
        Mock: Mocked settings object.
    """
    settings = Mock()
    settings.get = Mock(
        side_effect=lambda key, default=None: {
            "POSTGRES_HOST": "localhost",
            "POSTGRES_DB": "test_db",
            "POSTGRES_USER": "test_user",
            "POSTGRES_PASSWORD": "test_password",
            "POSTGRES_PORT": 5432,
        }.get(key, default)
    )
    return settings


@pytest.fixture
def mock_crawler(mock_crawler_settings):
    """
    Create a mock Scrapy crawler.

    Args:
        mock_crawler_settings: Mocked settings fixture.

    Returns:
        Mock: Mocked crawler object.
    """
    crawler = Mock()
    crawler.settings = mock_crawler_settings
    return crawler


# ============================================================================
# Utility Fixtures
# ============================================================================


@pytest.fixture
def sample_timestamp():
    """
    Provide a consistent timestamp for testing.

    Returns:
        datetime: A fixed datetime object.
    """
    return datetime(2025, 10, 30, 12, 0, 0)


@pytest.fixture
def sample_tags():
    """
    Provide sample tags for testing.

    Returns:
        list: List of sample tags.
    """
    return ["python", "scrapy", "testing"]


# ============================================================================
# Pytest Configuration Hooks
# ============================================================================


def pytest_configure(config):
    """
    Configure pytest with custom markers.

    Args:
        config: pytest configuration object.
    """
    config.addinivalue_line(
        "markers", "unit: Mark test as a unit test (fast, isolated)"
    )
    config.addinivalue_line(
        "markers", "integration: Mark test as an integration test"
    )
    config.addinivalue_line("markers", "slow: Mark test as slow")
    config.addinivalue_line("markers", "spider: Mark test as spider-related")
    config.addinivalue_line("markers", "pipeline: Mark test as pipeline-related")
    config.addinivalue_line("markers", "database: Mark test as database-related")
