#!/bin/bash

# Run all spiders sequentially
echo "🕷️  Starting all spiders..."
echo ""

echo "📰 Running HackerNews spider..."
scrapy crawl hackernews
echo ""

echo "💬 Running Quotes spider..."
scrapy crawl quotes
echo ""

echo "📚 Running Books spider..."
scrapy crawl books
echo ""

echo "✅ All spiders completed!"
echo ""

echo "📊 Database Statistics:"
psql -U scrapy -d scrapy_db -h localhost << 'SQL'
SELECT 'hackernews' as spider, COUNT(*) as records FROM hackernews
UNION ALL
SELECT 'quotes', COUNT(*) FROM quotes
UNION ALL
SELECT 'books', COUNT(*) FROM books;
SQL
