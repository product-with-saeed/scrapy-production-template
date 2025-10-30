"""
Unit Tests for Scrapy Item Models.

Tests for HackerNewsItem, QuoteItem, and BookItem following TDD principles.
Each test follows the Arrange-Act-Assert pattern.

Following PEP 8 style guide and pytest conventions.
"""

from datetime import datetime

import pytest

from scrapers.items import BookItem, HackerNewsItem, QuoteItem


# ============================================================================
# HackerNewsItem Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.spider
class TestHackerNewsItem:
    """Test suite for HackerNewsItem model."""

    def test_item_creation(self):
        """Test that HackerNewsItem can be instantiated."""
        # Arrange & Act
        item = HackerNewsItem()

        # Assert
        assert item is not None
        assert isinstance(item, HackerNewsItem)

    def test_item_has_required_fields(self):
        """Test that HackerNewsItem has all required fields."""
        # Arrange & Act
        item = HackerNewsItem()

        # Assert
        expected_fields = {
            "title",
            "url",
            "rank",
            "score",
            "author",
            "comments",
            "item_id",
            "scraped_at",
        }
        assert set(item.fields.keys()) == expected_fields

    def test_item_field_assignment(self, sample_hackernews_item):
        """Test that fields can be assigned and retrieved."""
        # Arrange (using fixture)
        item = sample_hackernews_item

        # Act & Assert
        assert item["title"] == "Test Article"
        assert item["url"] == "https://example.com/article"
        assert item["rank"] == "1"
        assert item["score"] == "100"
        assert item["author"] == "testuser"
        assert item["comments"] == "50"
        assert item["item_id"] == "12345"
        assert isinstance(item["scraped_at"], datetime)

    def test_item_partial_data(self):
        """Test that item works with partial data."""
        # Arrange
        item = HackerNewsItem()

        # Act
        item["title"] = "Test Title"
        item["item_id"] = "999"

        # Assert
        assert item["title"] == "Test Title"
        assert item["item_id"] == "999"
        assert "url" not in item  # Should not raise error

    def test_item_get_method_with_default(self):
        """Test that get() method returns default for missing fields."""
        # Arrange
        item = HackerNewsItem()
        item["title"] = "Test"

        # Act
        title = item.get("title")
        missing = item.get("url", "default_url")

        # Assert
        assert title == "Test"
        assert missing == "default_url"

    def test_item_field_types(self, sample_hackernews_item):
        """Test that field types are correct."""
        # Arrange (using fixture)
        item = sample_hackernews_item

        # Act & Assert
        assert isinstance(item["title"], str)
        assert isinstance(item["url"], str)
        assert isinstance(item["rank"], str)
        assert isinstance(item["score"], str)
        assert isinstance(item["author"], str)
        assert isinstance(item["comments"], str)
        assert isinstance(item["item_id"], str)
        assert isinstance(item["scraped_at"], datetime)


# ============================================================================
# QuoteItem Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.spider
class TestQuoteItem:
    """Test suite for QuoteItem model."""

    def test_item_creation(self):
        """Test that QuoteItem can be instantiated."""
        # Arrange & Act
        item = QuoteItem()

        # Assert
        assert item is not None
        assert isinstance(item, QuoteItem)

    def test_item_has_required_fields(self):
        """Test that QuoteItem has all required fields."""
        # Arrange & Act
        item = QuoteItem()

        # Assert
        expected_fields = {"text", "author", "tags", "scraped_at"}
        assert set(item.fields.keys()) == expected_fields

    def test_item_field_assignment(self, sample_quote_item):
        """Test that fields can be assigned and retrieved."""
        # Arrange (using fixture)
        item = sample_quote_item

        # Act & Assert
        assert item["text"] == "Test quote text"
        assert item["author"] == "Test Author"
        assert item["tags"] == ["inspiration", "life"]
        assert isinstance(item["scraped_at"], datetime)

    def test_item_tags_as_list(self, sample_quote_item):
        """Test that tags field accepts and returns a list."""
        # Arrange (using fixture)
        item = sample_quote_item

        # Act
        tags = item["tags"]

        # Assert
        assert isinstance(tags, list)
        assert len(tags) == 2
        assert "inspiration" in tags
        assert "life" in tags

    def test_item_empty_tags(self):
        """Test that item works with empty tags list."""
        # Arrange
        item = QuoteItem()

        # Act
        item["text"] = "Test"
        item["author"] = "Author"
        item["tags"] = []
        item["scraped_at"] = datetime.now()

        # Assert
        assert item["tags"] == []
        assert isinstance(item["tags"], list)

    def test_item_field_types(self, sample_quote_item):
        """Test that field types are correct."""
        # Arrange (using fixture)
        item = sample_quote_item

        # Act & Assert
        assert isinstance(item["text"], str)
        assert isinstance(item["author"], str)
        assert isinstance(item["tags"], list)
        assert isinstance(item["scraped_at"], datetime)


# ============================================================================
# BookItem Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.spider
class TestBookItem:
    """Test suite for BookItem model."""

    def test_item_creation(self):
        """Test that BookItem can be instantiated."""
        # Arrange & Act
        item = BookItem()

        # Assert
        assert item is not None
        assert isinstance(item, BookItem)

    def test_item_has_required_fields(self):
        """Test that BookItem has all required fields."""
        # Arrange & Act
        item = BookItem()

        # Assert
        expected_fields = {
            "title",
            "price",
            "availability",
            "rating",
            "url",
            "scraped_at",
        }
        assert set(item.fields.keys()) == expected_fields

    def test_item_field_assignment(self, sample_book_item):
        """Test that fields can be assigned and retrieved."""
        # Arrange (using fixture)
        item = sample_book_item

        # Act & Assert
        assert item["title"] == "Test Book"
        assert item["price"] == "£51.77"
        assert item["availability"] == "In stock"
        assert item["rating"] == "Four"
        assert item["url"] == "https://example.com/book"
        assert isinstance(item["scraped_at"], datetime)

    def test_item_price_format(self):
        """Test that price field accepts currency formats."""
        # Arrange
        item = BookItem()

        # Act
        item["price"] = "£51.77"

        # Assert
        assert item["price"] == "£51.77"
        assert "£" in item["price"]

    def test_item_rating_values(self):
        """Test that rating field accepts word ratings."""
        # Arrange
        item = BookItem()

        # Act & Assert - Testing various rating formats
        ratings = ["One", "Two", "Three", "Four", "Five"]
        for rating in ratings:
            item["rating"] = rating
            assert item["rating"] == rating

    def test_item_availability_states(self):
        """Test that availability field handles different states."""
        # Arrange
        item = BookItem()

        # Act & Assert
        availability_states = ["In stock", "Out of stock", "Available"]
        for state in availability_states:
            item["availability"] = state
            assert item["availability"] == state

    def test_item_field_types(self, sample_book_item):
        """Test that field types are correct."""
        # Arrange (using fixture)
        item = sample_book_item

        # Act & Assert
        assert isinstance(item["title"], str)
        assert isinstance(item["price"], str)
        assert isinstance(item["availability"], str)
        assert isinstance(item["rating"], str)
        assert isinstance(item["url"], str)
        assert isinstance(item["scraped_at"], datetime)


# ============================================================================
# Item Utility Function Tests
# ============================================================================


@pytest.mark.unit
class TestItemUtilityFunctions:
    """Test suite for utility functions in items module."""

    def test_clean_text_function(self):
        """Test the clean_text utility function."""
        # Import the function
        from scrapers.items import clean_text

        # Arrange & Act & Assert
        assert clean_text("  test  ") == "test"
        assert clean_text("test") == "test"
        assert clean_text("") is None
        assert clean_text(None) is None
        assert clean_text("  ") == ""

    def test_clean_text_with_newlines(self):
        """Test clean_text handles newlines and tabs."""
        # Import the function
        from scrapers.items import clean_text

        # Arrange
        text_with_whitespace = "\n\ttest\n\t"

        # Act
        result = clean_text(text_with_whitespace)

        # Assert
        assert result == "test"


# ============================================================================
# Cross-Item Tests
# ============================================================================


@pytest.mark.unit
class TestItemCommonBehavior:
    """Test common behavior across all item types."""

    @pytest.mark.parametrize(
        "item_class",
        [HackerNewsItem, QuoteItem, BookItem],
    )
    def test_all_items_have_scraped_at_field(self, item_class):
        """Test that all items have a scraped_at timestamp field."""
        # Arrange
        item = item_class()

        # Act & Assert
        assert "scraped_at" in item.fields
        # Can set datetime
        now = datetime.now()
        item["scraped_at"] = now
        assert item["scraped_at"] == now

    @pytest.mark.parametrize(
        "item_class,expected_fields",
        [
            (HackerNewsItem, 8),  # 7 data fields + scraped_at
            (QuoteItem, 4),  # 3 data fields + scraped_at
            (BookItem, 6),  # 5 data fields + scraped_at
        ],
    )
    def test_item_field_count(self, item_class, expected_fields):
        """Test that each item has the expected number of fields."""
        # Arrange
        item = item_class()

        # Act
        field_count = len(item.fields)

        # Assert
        assert field_count == expected_fields
