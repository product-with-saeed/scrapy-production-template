#!/bin/bash
# View scraped data from PostgreSQL database

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📊 Scraped Data Summary${NC}"
echo "================================"
echo ""

# Check if PostgreSQL is running
if ! docker exec scrapy_postgres pg_isready -U scrapy > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  PostgreSQL is not running. Start it with:${NC}"
    echo "  ./scripts/setup_postgres.sh"
    exit 1
fi

# Function to display table
display_table() {
    local table=$1
    local title=$2

    echo -e "${GREEN}${title}${NC}"
    echo "--------------------------------"

    # Get count
    count=$(docker exec scrapy_postgres psql -U scrapy -d scrapy_db -t -c "SELECT COUNT(*) FROM ${table};" 2>/dev/null | xargs)

    if [ "$count" -eq 0 ]; then
        echo "No data yet. Run: scrapy crawl ${table}"
        echo ""
        return
    fi

    echo "Total items: $count"
    echo ""

    # Show latest items
    case $table in
        hackernews)
            docker exec scrapy_postgres psql -U scrapy -d scrapy_db -c \
                "SELECT title, author, score FROM ${table} ORDER BY created_at DESC LIMIT 5;"
            ;;
        quotes)
            docker exec scrapy_postgres psql -U scrapy -d scrapy_db -c \
                "SELECT text, author FROM ${table} ORDER BY created_at DESC LIMIT 5;"
            ;;
        books)
            docker exec scrapy_postgres psql -U scrapy -d scrapy_db -c \
                "SELECT title, price, rating FROM ${table} ORDER BY created_at DESC LIMIT 5;"
            ;;
    esac

    echo ""
}

# Display data for each spider
display_table "hackernews" "🗞️  HackerNews Articles"
display_table "quotes" "💬 Quotes"
display_table "books" "📚 Books"

echo "================================"
echo -e "${BLUE}💡 Tip: To view all data, connect to the database:${NC}"
echo "  docker exec -it scrapy_postgres psql -U scrapy -d scrapy_db"
echo ""
echo -e "${BLUE}Or query specific data:${NC}"
echo "  docker exec scrapy_postgres psql -U scrapy -d scrapy_db -c \"SELECT * FROM hackernews LIMIT 10;\""
echo ""
