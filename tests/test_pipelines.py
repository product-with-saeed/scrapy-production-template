"""
Unit Tests for Scrapy Pipelines.

Tests for PostgresPipeline following TDD principles with proper mocking.
Each test follows the Arrange-Act-Assert pattern.

Following PEP 8 style guide and pytest conventions.
"""

from unittest.mock import MagicMock, Mock, call, patch

import psycopg2
import pytest

from scrapers.pipelines import PostgresPipeline


# ============================================================================
# PostgresPipeline Initialization Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.pipeline
@pytest.mark.database
class TestPostgresPipelineInitialization:
    """Test suite for PostgresPipeline initialization."""

    def test_pipeline_creation_with_config(self, mock_db_config):
        """Test that pipeline can be instantiated with config."""
        # Arrange & Act
        pipeline = PostgresPipeline(mock_db_config)

        # Assert
        assert pipeline is not None
        assert pipeline.db_config == mock_db_config
        assert pipeline.connection is None
        assert pipeline.cursor is None
        assert pipeline.logger is not None

    def test_from_crawler_method(self, mock_crawler):
        """Test that pipeline can be created from crawler."""
        # Arrange & Act
        pipeline = PostgresPipeline.from_crawler(mock_crawler)

        # Assert
        assert pipeline is not None
        assert isinstance(pipeline, PostgresPipeline)
        assert pipeline.db_config["host"] == "localhost"
        assert pipeline.db_config["database"] == "test_db"
        assert pipeline.db_config["user"] == "test_user"
        assert pipeline.db_config["password"] == "test_password"
        assert pipeline.db_config["port"] == 5432

    def test_from_crawler_uses_settings(self, mock_crawler):
        """Test that from_crawler correctly extracts settings."""
        # Arrange
        # Mock crawler returns specific values

        # Act
        pipeline = PostgresPipeline.from_crawler(mock_crawler)

        # Assert
        mock_crawler.settings.get.assert_any_call("POSTGRES_HOST", "postgres")
        mock_crawler.settings.get.assert_any_call("POSTGRES_DB", "scrapy_db")
        mock_crawler.settings.get.assert_any_call("POSTGRES_USER", "scrapy")
        mock_crawler.settings.get.assert_any_call("POSTGRES_PASSWORD", "scrapy")
        mock_crawler.settings.get.assert_any_call("POSTGRES_PORT", 5432)


# ============================================================================
# PostgresPipeline Spider Lifecycle Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.pipeline
@pytest.mark.database
class TestPostgresPipelineLifecycle:
    """Test suite for spider open/close operations."""

    def test_open_spider_establishes_connection(
        self, mock_db_config, mock_db_connection, hackernews_spider
    ):
        """Test that open_spider establishes database connection."""
        # Arrange
        pipeline = PostgresPipeline(mock_db_config)

        # Act
        pipeline.open_spider(hackernews_spider)

        # Assert
        assert pipeline.connection is not None
        assert pipeline.cursor is not None
        pipeline.connection.cursor.assert_called_once()

    def test_open_spider_creates_tables(
        self, mock_db_config, mock_db_connection, mock_db_cursor, hackernews_spider
    ):
        """Test that open_spider creates necessary tables."""
        # Arrange
        pipeline = PostgresPipeline(mock_db_config)

        # Act
        pipeline.open_spider(hackernews_spider)

        # Assert
        # Should execute CREATE TABLE query
        mock_db_cursor.execute.assert_called()
        executed_query = mock_db_cursor.execute.call_args[0][0]
        assert "CREATE TABLE IF NOT EXISTS hackernews" in executed_query

    def test_open_spider_handles_connection_error(
        self, mock_db_config, mocker, hackernews_spider
    ):
        """Test that open_spider handles connection errors properly."""
        # Arrange
        pipeline = PostgresPipeline(mock_db_config)
        mocker.patch("psycopg2.connect", side_effect=psycopg2.OperationalError)

        # Act & Assert
        with pytest.raises(psycopg2.OperationalError):
            pipeline.open_spider(hackernews_spider)

    def test_close_spider_commits_and_closes_connection(
        self, mock_db_config, mock_db_connection, hackernews_spider
    ):
        """Test that close_spider properly closes resources."""
        # Arrange
        pipeline = PostgresPipeline(mock_db_config)
        pipeline.open_spider(hackernews_spider)

        # Act
        pipeline.close_spider(hackernews_spider)

        # Assert
        pipeline.connection.commit.assert_called()
        pipeline.cursor.close.assert_called_once()
        pipeline.connection.close.assert_called_once()

    def test_close_spider_handles_no_connection(
        self, mock_db_config, hackernews_spider
    ):
        """Test that close_spider handles missing connection gracefully."""
        # Arrange
        pipeline = PostgresPipeline(mock_db_config)
        # Don't call open_spider, so connection is None

        # Act - should not raise error
        pipeline.close_spider(hackernews_spider)

        # Assert - no error occurred
        assert pipeline.connection is None


# ============================================================================
# PostgresPipeline Table Creation Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.pipeline
@pytest.mark.database
class TestPostgresPipelineTableCreation:
    """Test suite for create_tables functionality."""

    @pytest.mark.parametrize(
        "spider_name,expected_table",
        [
            ("hackernews", "hackernews"),
            ("quotes", "quotes"),
            ("books", "books"),
        ],
    )
    def test_create_tables_for_known_spiders(
        self, mock_db_config, mock_db_connection, mock_db_cursor, spider_name, expected_table
    ):
        """Test that tables are created for known spider names."""
        # Arrange
        pipeline = PostgresPipeline(mock_db_config)
        spider = Mock()
        spider.name = spider_name

        # Act
        pipeline.open_spider(spider)

        # Assert
        executed_query = mock_db_cursor.execute.call_args[0][0]
        assert f"CREATE TABLE IF NOT EXISTS {expected_table}" in executed_query
        pipeline.connection.commit.assert_called()

    def test_hackernews_table_has_unique_item_id(
        self, mock_db_config, mock_db_connection, mock_db_cursor, hackernews_spider
    ):
        """Test that HackerNews table has UNIQUE constraint on item_id."""
        # Arrange
        pipeline = PostgresPipeline(mock_db_config)

        # Act
        pipeline.open_spider(hackernews_spider)

        # Assert
        executed_query = mock_db_cursor.execute.call_args[0][0]
        assert "item_id TEXT UNIQUE" in executed_query

    def test_books_table_has_unique_url(
        self, mock_db_config, mock_db_connection, mock_db_cursor, books_spider
    ):
        """Test that Books table has UNIQUE constraint on url."""
        # Arrange
        pipeline = PostgresPipeline(mock_db_config)

        # Act
        pipeline.open_spider(books_spider)

        # Assert
        executed_query = mock_db_cursor.execute.call_args[0][0]
        assert "url TEXT UNIQUE" in executed_query

    def test_quotes_table_has_text_array(
        self, mock_db_config, mock_db_connection, mock_db_cursor, quotes_spider
    ):
        """Test that Quotes table has TEXT[] array for tags."""
        # Arrange
        pipeline = PostgresPipeline(mock_db_config)

        # Act
        pipeline.open_spider(quotes_spider)

        # Assert
        executed_query = mock_db_cursor.execute.call_args[0][0]
        assert "tags TEXT[]" in executed_query


# ============================================================================
# PostgresPipeline Item Processing Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.pipeline
@pytest.mark.database
class TestPostgresPipelineItemProcessing:
    """Test suite for process_item functionality."""

    def test_process_hackernews_item(
        self,
        mock_db_config,
        mock_db_connection,
        mock_db_cursor,
        hackernews_spider,
        sample_hackernews_item,
    ):
        """Test that HackerNews items are processed correctly."""
        # Arrange
        pipeline = PostgresPipeline(mock_db_config)
        pipeline.open_spider(hackernews_spider)
        mock_db_cursor.reset_mock()  # Clear open_spider calls

        # Act
        returned_item = pipeline.process_item(sample_hackernews_item, hackernews_spider)

        # Assert
        assert returned_item == sample_hackernews_item
        mock_db_cursor.execute.assert_called_once()
        executed_query = mock_db_cursor.execute.call_args[0][0]
        assert "INSERT INTO hackernews" in executed_query
        assert "ON CONFLICT (item_id) DO NOTHING" in executed_query
        pipeline.connection.commit.assert_called()

    def test_process_quotes_item(
        self,
        mock_db_config,
        mock_db_connection,
        mock_db_cursor,
        quotes_spider,
        sample_quote_item,
    ):
        """Test that Quote items are processed correctly."""
        # Arrange
        pipeline = PostgresPipeline(mock_db_config)
        pipeline.open_spider(quotes_spider)
        mock_db_cursor.reset_mock()

        # Act
        returned_item = pipeline.process_item(sample_quote_item, quotes_spider)

        # Assert
        assert returned_item == sample_quote_item
        mock_db_cursor.execute.assert_called_once()
        executed_query = mock_db_cursor.execute.call_args[0][0]
        assert "INSERT INTO quotes" in executed_query
        # Quotes don't have ON CONFLICT
        assert "ON CONFLICT" not in executed_query

    def test_process_books_item(
        self,
        mock_db_config,
        mock_db_connection,
        mock_db_cursor,
        books_spider,
        sample_book_item,
    ):
        """Test that Book items are processed correctly."""
        # Arrange
        pipeline = PostgresPipeline(mock_db_config)
        pipeline.open_spider(books_spider)
        mock_db_cursor.reset_mock()

        # Act
        returned_item = pipeline.process_item(sample_book_item, books_spider)

        # Assert
        assert returned_item == sample_book_item
        mock_db_cursor.execute.assert_called_once()
        executed_query = mock_db_cursor.execute.call_args[0][0]
        assert "INSERT INTO books" in executed_query
        assert "ON CONFLICT (url) DO NOTHING" in executed_query

    def test_process_item_extracts_correct_fields(
        self,
        mock_db_config,
        mock_db_connection,
        mock_db_cursor,
        hackernews_spider,
        sample_hackernews_item,
    ):
        """Test that process_item extracts and inserts correct field values."""
        # Arrange
        pipeline = PostgresPipeline(mock_db_config)
        pipeline.open_spider(hackernews_spider)
        mock_db_cursor.reset_mock()

        # Act
        pipeline.process_item(sample_hackernews_item, hackernews_spider)

        # Assert
        call_args = mock_db_cursor.execute.call_args
        inserted_values = call_args[0][1]
        assert "Test Article" in inserted_values
        assert "https://example.com/article" in inserted_values
        assert "12345" in inserted_values


# ============================================================================
# PostgresPipeline Error Handling Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.pipeline
@pytest.mark.database
class TestPostgresPipelineErrorHandling:
    """Test suite for error handling in pipeline."""

    def test_process_item_handles_database_error(
        self,
        mock_db_config,
        mock_db_connection,
        mock_db_cursor,
        hackernews_spider,
        sample_hackernews_item,
    ):
        """Test that process_item handles database errors and rolls back."""
        # Arrange
        pipeline = PostgresPipeline(mock_db_config)
        pipeline.open_spider(hackernews_spider)
        mock_db_cursor.execute.side_effect = psycopg2.DatabaseError("Test error")

        # Act
        returned_item = pipeline.process_item(sample_hackernews_item, hackernews_spider)

        # Assert
        assert returned_item == sample_hackernews_item  # Item still returned
        pipeline.connection.rollback.assert_called()

    def test_process_item_continues_after_error(
        self,
        mock_db_config,
        mock_db_connection,
        mock_db_cursor,
        hackernews_spider,
        sample_hackernews_item,
    ):
        """Test that pipeline continues processing after error."""
        # Arrange
        pipeline = PostgresPipeline(mock_db_config)
        pipeline.open_spider(hackernews_spider)

        # First call fails, second succeeds
        mock_db_cursor.execute.side_effect = [
            psycopg2.DatabaseError("Error"),
            None,
        ]

        # Act
        item1 = pipeline.process_item(sample_hackernews_item, hackernews_spider)

        # Reset side effect for second call
        mock_db_cursor.execute.side_effect = None
        item2 = pipeline.process_item(sample_hackernews_item, hackernews_spider)

        # Assert
        assert item1 is not None
        assert item2 is not None


# ============================================================================
# PostgresPipeline Integration Tests (Mocked)
# ============================================================================


@pytest.mark.integration
@pytest.mark.pipeline
@pytest.mark.database
class TestPostgresPipelineIntegration:
    """Integration tests for complete pipeline workflow."""

    def test_complete_pipeline_lifecycle(
        self,
        mock_db_config,
        mock_db_connection,
        mock_db_cursor,
        hackernews_spider,
        sample_hackernews_item,
    ):
        """Test complete pipeline lifecycle from open to close."""
        # Arrange
        pipeline = PostgresPipeline(mock_db_config)

        # Act
        pipeline.open_spider(hackernews_spider)
        pipeline.process_item(sample_hackernews_item, hackernews_spider)
        pipeline.close_spider(hackernews_spider)

        # Assert
        # Verify connection was established
        assert pipeline.connection is not None
        # Verify cursor was created
        pipeline.connection.cursor.assert_called()
        # Verify item was inserted
        assert mock_db_cursor.execute.call_count >= 2  # CREATE TABLE + INSERT
        # Verify cleanup
        pipeline.cursor.close.assert_called_once()
        pipeline.connection.close.assert_called_once()

    def test_pipeline_handles_multiple_items(
        self,
        mock_db_config,
        mock_db_connection,
        mock_db_cursor,
        hackernews_spider,
        sample_hackernews_item,
    ):
        """Test that pipeline can handle multiple items in sequence."""
        # Arrange
        pipeline = PostgresPipeline(mock_db_config)
        pipeline.open_spider(hackernews_spider)
        mock_db_cursor.reset_mock()
        # Reset commit count after open_spider (which also commits)
        mock_db_connection.commit.reset_mock()

        # Act
        for i in range(3):
            item = sample_hackernews_item.copy()
            item["item_id"] = f"item_{i}"
            pipeline.process_item(item, hackernews_spider)

        # Assert
        assert mock_db_cursor.execute.call_count == 3
        assert pipeline.connection.commit.call_count == 3
