"""
Unit Tests for Scrapy Spiders.

Tests for HackerNewsSpider, QuotesSpider, and BooksSpider following TDD principles.
Each test follows the Arrange-Act-Assert pattern.

Following PEP 8 style guide and pytest conventions.
"""

from datetime import datetime
from unittest.mock import patch

import pytest
from scrapy.http import HtmlResponse, Request

from scrapers.spiders.books_spider import BooksSpider
from scrapers.spiders.hackernews_spider import HackerNewsSpider
from scrapers.spiders.quotes_spider import QuotesSpider


# ============================================================================
# HackerNewsSpider Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.spider
class TestHackerNewsSpider:
    """Test suite for HackerNewsSpider."""

    def test_spider_attributes(self):
        """Test that spider has correct basic attributes."""
        # Arrange & Act
        spider = HackerNewsSpider()

        # Assert
        assert spider.name == "hackernews"
        assert "news.ycombinator.com" in spider.allowed_domains
        assert "https://news.ycombinator.com/" in spider.start_urls

    def test_spider_custom_settings(self):
        """Test that spider has correct custom settings."""
        # Arrange & Act
        spider = HackerNewsSpider()

        # Assert
        assert spider.custom_settings["DOWNLOAD_DELAY"] == 1
        assert spider.custom_settings["CONCURRENT_REQUESTS_PER_DOMAIN"] == 2
        assert spider.custom_settings["ROBOTSTXT_OBEY"] is True

    def test_parse_extracts_items(self):
        """Test that parse method extracts items from response."""
        # Arrange
        spider = HackerNewsSpider()
        html_content = """
        <html>
            <body>
                <table class="itemlist">
                    <tr class="athing" id="12345">
                        <td align="right" valign="top" class="title">
                            <span class="rank">1.</span>
                        </td>
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
        response = HtmlResponse(
            url="https://news.ycombinator.com/",
            body=html_content.encode("utf-8"),
            encoding="utf-8",
        )

        # Act
        results = list(spider.parse(response))

        # Assert
        assert len(results) == 1
        item = results[0]
        assert item["title"] == "Test Article"
        assert item["url"] == "https://example.com/article"
        assert item["rank"] == "1."
        assert item["item_id"] == "12345"
        assert item["score"] == "100 points"
        assert item["author"] == "testuser"
        assert "50" in item["comments"]
        assert "scraped_at" in item

    def test_parse_handles_multiple_items(self):
        """Test that parse method handles multiple items."""
        # Arrange
        spider = HackerNewsSpider()
        html_content = """
        <html>
            <body>
                <table class="itemlist">
                    <tr class="athing" id="1">
                        <td class="rank">1.</td>
                        <td><span class="titleline"><a href="url1">Title 1</a></span></td>
                    </tr>
                    <tr><td colspan="2"></td><td class="subtext">
                        <span class="score">10 points</span>
                        <a class="hnuser">user1</a>
                        <a>5 comments</a>
                    </td></tr>
                    <tr class="athing" id="2">
                        <td class="rank">2.</td>
                        <td><span class="titleline"><a href="url2">Title 2</a></span></td>
                    </tr>
                    <tr><td colspan="2"></td><td class="subtext">
                        <span class="score">20 points</span>
                        <a class="hnuser">user2</a>
                        <a>10 comments</a>
                    </td></tr>
                </table>
            </body>
        </html>
        """
        response = HtmlResponse(
            url="https://news.ycombinator.com/",
            body=html_content.encode("utf-8"),
            encoding="utf-8",
        )

        # Act
        results = list(spider.parse(response))

        # Assert
        assert len(results) == 2
        assert results[0]["title"] == "Title 1"
        assert results[1]["title"] == "Title 2"

    def test_parse_handles_missing_fields(self):
        """Test that parse gracefully handles missing fields."""
        # Arrange
        spider = HackerNewsSpider()
        html_content = """
        <html>
            <body>
                <table class="itemlist">
                    <tr class="athing" id="999">
                        <td><span class="titleline"><a>Partial Data</a></span></td>
                    </tr>
                    <tr><td></td></tr>
                </table>
            </body>
        </html>
        """
        response = HtmlResponse(
            url="https://news.ycombinator.com/",
            body=html_content.encode("utf-8"),
            encoding="utf-8",
        )

        # Act
        results = list(spider.parse(response))

        # Assert
        assert len(results) == 1
        item = results[0]
        assert item["title"] == "Partial Data"
        assert item["item_id"] == "999"
        # Missing fields should be None
        assert item["score"] is None
        assert item["author"] is None


# ============================================================================
# QuotesSpider Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.spider
class TestQuotesSpider:
    """Test suite for QuotesSpider."""

    def test_spider_attributes(self):
        """Test that spider has correct basic attributes."""
        # Arrange & Act
        spider = QuotesSpider()

        # Assert
        assert spider.name == "quotes"
        assert "quotes.toscrape.com" in spider.allowed_domains
        assert "http://quotes.toscrape.com/" in spider.start_urls

    def test_spider_custom_settings(self):
        """Test that spider has correct custom settings."""
        # Arrange & Act
        spider = QuotesSpider()

        # Assert
        assert spider.custom_settings["DOWNLOAD_DELAY"] == 0.5
        assert spider.custom_settings["CONCURRENT_REQUESTS_PER_DOMAIN"] == 2
        assert spider.custom_settings["ROBOTSTXT_OBEY"] is True

    def test_parse_extracts_quotes(self):
        """Test that parse method extracts quote items."""
        # Arrange
        spider = QuotesSpider()
        html_content = """
        <html>
            <body>
                <div class="quote">
                    <span class="text">"Test quote text"</span>
                    <small class="author">Test Author</small>
                    <div class="tags">
                        <a class="tag">inspiration</a>
                        <a class="tag">life</a>
                    </div>
                </div>
            </body>
        </html>
        """
        response = HtmlResponse(
            url="http://quotes.toscrape.com/",
            body=html_content.encode("utf-8"),
            encoding="utf-8",
        )

        # Act
        results = list(spider.parse(response))

        # Assert
        assert len(results) == 1
        item = results[0]
        assert item["text"] == '"Test quote text"'
        assert item["author"] == "Test Author"
        assert item["tags"] == ["inspiration", "life"]
        assert "scraped_at" in item

    def test_parse_handles_multiple_quotes(self):
        """Test that parse handles multiple quotes."""
        # Arrange
        spider = QuotesSpider()
        html_content = """
        <html>
            <body>
                <div class="quote">
                    <span class="text">"Quote 1"</span>
                    <small class="author">Author 1</small>
                    <div class="tags"><a class="tag">tag1</a></div>
                </div>
                <div class="quote">
                    <span class="text">"Quote 2"</span>
                    <small class="author">Author 2</small>
                    <div class="tags"><a class="tag">tag2</a></div>
                </div>
            </body>
        </html>
        """
        response = HtmlResponse(
            url="http://quotes.toscrape.com/",
            body=html_content.encode("utf-8"),
            encoding="utf-8",
        )

        # Act
        results = list(spider.parse(response))

        # Assert
        assert len(results) == 2
        assert results[0]["text"] == '"Quote 1"'
        assert results[1]["text"] == '"Quote 2"'

    def test_parse_follows_pagination(self):
        """Test that parse follows pagination links."""
        # Arrange
        spider = QuotesSpider()
        html_content = """
        <html>
            <body>
                <div class="quote">
                    <span class="text">"Test"</span>
                    <small class="author">Author</small>
                    <div class="tags"><a class="tag">tag</a></div>
                </div>
                <ul class="pager">
                    <li class="next">
                        <a href="/page/2/">Next →</a>
                    </li>
                </ul>
            </body>
        </html>
        """
        response = HtmlResponse(
            url="http://quotes.toscrape.com/",
            body=html_content.encode("utf-8"),
            encoding="utf-8",
        )

        # Act
        results = list(spider.parse(response))

        # Assert
        # Should have 1 item + 1 request
        assert len(results) == 2
        # First result is the quote
        assert isinstance(results[0], dict)
        # Second result is the pagination request
        assert isinstance(results[1], Request)
        assert "/page/2/" in results[1].url

    def test_parse_handles_no_pagination(self):
        """Test that parse handles pages without pagination."""
        # Arrange
        spider = QuotesSpider()
        html_content = """
        <html>
            <body>
                <div class="quote">
                    <span class="text">"Last quote"</span>
                    <small class="author">Author</small>
                    <div class="tags"><a class="tag">tag</a></div>
                </div>
            </body>
        </html>
        """
        response = HtmlResponse(
            url="http://quotes.toscrape.com/page/10/",
            body=html_content.encode("utf-8"),
            encoding="utf-8",
        )

        # Act
        results = list(spider.parse(response))

        # Assert
        # Should only have the quote item, no pagination request
        assert len(results) == 1
        assert isinstance(results[0], dict)


# ============================================================================
# BooksSpider Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.spider
class TestBooksSpider:
    """Test suite for BooksSpider."""

    def test_spider_attributes(self):
        """Test that spider has correct basic attributes."""
        # Arrange & Act
        spider = BooksSpider()

        # Assert
        assert spider.name == "books"
        assert "books.toscrape.com" in spider.allowed_domains
        assert "http://books.toscrape.com/" in spider.start_urls

    def test_spider_custom_settings(self):
        """Test that spider has correct custom settings."""
        # Arrange & Act
        spider = BooksSpider()

        # Assert
        assert spider.custom_settings["DOWNLOAD_DELAY"] == 0.5
        assert spider.custom_settings["CONCURRENT_REQUESTS_PER_DOMAIN"] == 2
        assert spider.custom_settings["ROBOTSTXT_OBEY"] is True

    def test_parse_extracts_books(self):
        """Test that parse method extracts book items."""
        # Arrange
        spider = BooksSpider()
        html_content = """
        <html>
            <body>
                <article class="product_pod">
                    <p class="star-rating Four"></p>
                    <h3><a href="book.html" title="Test Book">Test Book</a></h3>
                    <p class="price_color">£51.77</p>
                    <p class="availability">
                        In stock
                    </p>
                </article>
            </body>
        </html>
        """
        response = HtmlResponse(
            url="http://books.toscrape.com/",
            body=html_content.encode("utf-8"),
            encoding="utf-8",
        )

        # Act
        results = list(spider.parse(response))

        # Assert
        assert len(results) == 1
        item = results[0]
        assert item["title"] == "Test Book"
        assert item["price"] == "£51.77"
        assert item["availability"] == "In stock"
        assert item["rating"] == "Four"
        assert "book.html" in item["url"]
        assert "scraped_at" in item

    def test_parse_handles_multiple_books(self):
        """Test that parse handles multiple books."""
        # Arrange
        spider = BooksSpider()
        html_content = """
        <html>
            <body>
                <article class="product_pod">
                    <p class="star-rating Five"></p>
                    <h3><a href="book1.html" title="Book 1">Book 1</a></h3>
                    <p class="price_color">£10.00</p>
                    <p class="availability">In stock</p>
                </article>
                <article class="product_pod">
                    <p class="star-rating Three"></p>
                    <h3><a href="book2.html" title="Book 2">Book 2</a></h3>
                    <p class="price_color">£20.00</p>
                    <p class="availability">Out of stock</p>
                </article>
            </body>
        </html>
        """
        response = HtmlResponse(
            url="http://books.toscrape.com/",
            body=html_content.encode("utf-8"),
            encoding="utf-8",
        )

        # Act
        results = list(spider.parse(response))

        # Assert
        assert len(results) == 2
        assert results[0]["title"] == "Book 1"
        assert results[0]["rating"] == "Five"
        assert results[1]["title"] == "Book 2"
        assert results[1]["rating"] == "Three"

    def test_parse_extracts_rating_correctly(self):
        """Test that parse correctly extracts star ratings."""
        # Arrange
        spider = BooksSpider()

        # Test different ratings
        ratings = ["One", "Two", "Three", "Four", "Five"]
        for rating in ratings:
            html_content = f"""
            <html>
                <body>
                    <article class="product_pod">
                        <p class="star-rating {rating}"></p>
                        <h3><a href="book.html" title="Book">Book</a></h3>
                        <p class="price_color">£10.00</p>
                        <p class="availability">In stock</p>
                    </article>
                </body>
            </html>
            """
            response = HtmlResponse(
                url="http://books.toscrape.com/",
                body=html_content.encode("utf-8"),
                encoding="utf-8",
            )

            # Act
            results = list(spider.parse(response))

            # Assert
            assert results[0]["rating"] == rating

    def test_parse_handles_missing_rating(self):
        """Test that parse handles missing rating."""
        # Arrange
        spider = BooksSpider()
        html_content = """
        <html>
            <body>
                <article class="product_pod">
                    <h3><a href="book.html" title="Book">Book</a></h3>
                    <p class="price_color">£10.00</p>
                    <p class="availability">In stock</p>
                </article>
            </body>
        </html>
        """
        response = HtmlResponse(
            url="http://books.toscrape.com/",
            body=html_content.encode("utf-8"),
            encoding="utf-8",
        )

        # Act
        results = list(spider.parse(response))

        # Assert
        assert results[0]["rating"] is None

    def test_parse_follows_pagination(self):
        """Test that parse follows pagination links."""
        # Arrange
        spider = BooksSpider()
        html_content = """
        <html>
            <body>
                <article class="product_pod">
                    <p class="star-rating Four"></p>
                    <h3><a href="book.html" title="Book">Book</a></h3>
                    <p class="price_color">£10.00</p>
                    <p class="availability">In stock</p>
                </article>
                <ul class="pager">
                    <li class="next">
                        <a href="catalogue/page-2.html">next</a>
                    </li>
                </ul>
            </body>
        </html>
        """
        response = HtmlResponse(
            url="http://books.toscrape.com/",
            body=html_content.encode("utf-8"),
            encoding="utf-8",
        )

        # Act
        results = list(spider.parse(response))

        # Assert
        # Should have 1 item + 1 request
        assert len(results) == 2
        assert isinstance(results[0], dict)
        assert isinstance(results[1], Request)
        assert "page-2.html" in results[1].url

    def test_parse_url_join(self):
        """Test that parse correctly joins relative URLs."""
        # Arrange
        spider = BooksSpider()
        html_content = """
        <html>
            <body>
                <article class="product_pod">
                    <p class="star-rating Four"></p>
                    <h3><a href="catalogue/book.html" title="Book">Book</a></h3>
                    <p class="price_color">£10.00</p>
                    <p class="availability">In stock</p>
                </article>
            </body>
        </html>
        """
        response = HtmlResponse(
            url="http://books.toscrape.com/",
            body=html_content.encode("utf-8"),
            encoding="utf-8",
        )

        # Act
        results = list(spider.parse(response))

        # Assert
        assert results[0]["url"] == "http://books.toscrape.com/catalogue/book.html"


# ============================================================================
# Spider Instantiation Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.spider
class TestSpiderInstantiation:
    """Test that all spiders can be instantiated correctly."""

    @pytest.mark.parametrize(
        "spider_class,expected_name",
        [
            (HackerNewsSpider, "hackernews"),
            (QuotesSpider, "quotes"),
            (BooksSpider, "books"),
        ],
    )
    def test_spider_instantiation(self, spider_class, expected_name):
        """Test that spiders can be instantiated."""
        # Arrange & Act
        spider = spider_class()

        # Assert
        assert spider is not None
        assert spider.name == expected_name
        assert hasattr(spider, "allowed_domains")
        assert hasattr(spider, "start_urls")
        assert hasattr(spider, "custom_settings")
        assert hasattr(spider, "parse")
