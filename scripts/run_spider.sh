#!/bin/bash
# Run a Scrapy spider with real-time terminal output
#
# Usage:
#   ./scripts/run_spider.sh <spider_name> [options]
#
# Examples:
#   ./scripts/run_spider.sh hackernews
#   ./scripts/run_spider.sh quotes --limit 10
#   ./scripts/run_spider.sh books --debug

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if spider name provided
if [ $# -lt 1 ]; then
    echo -e "${RED}❌ Error: Spider name required${NC}"
    echo ""
    echo "Usage: $0 <spider_name> [options]"
    echo ""
    echo "Available spiders:"
    echo "  - hackernews"
    echo "  - quotes"
    echo "  - books"
    echo ""
    echo "Options:"
    echo "  --limit N    : Scrape only N items"
    echo "  --debug      : Enable debug logging"
    echo "  --no-db      : Disable database pipeline (dry run)"
    echo ""
    echo "Examples:"
    echo "  $0 hackernews"
    echo "  $0 quotes --limit 10"
    echo "  $0 books --debug"
    exit 1
fi

SPIDER_NAME=$1
shift

# Parse options
ITEM_LIMIT=""
LOG_LEVEL="INFO"
DISABLE_PIPELINE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --limit)
            ITEM_LIMIT="-s CLOSESPIDER_ITEMCOUNT=$2"
            shift 2
            ;;
        --debug)
            LOG_LEVEL="DEBUG"
            shift
            ;;
        --no-db)
            DISABLE_PIPELINE="-s ITEM_PIPELINES={}"
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Check if PostgreSQL is running (unless --no-db specified)
if [ -z "$DISABLE_PIPELINE" ]; then
    if ! docker exec scrapy_postgres pg_isready -U scrapy > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  PostgreSQL is not running.${NC}"
        echo -e "${YELLOW}Starting PostgreSQL...${NC}"
        ./scripts/setup_postgres.sh
    fi
fi

# Display spider info
echo -e "${BLUE}🕷️  Running Spider: ${SPIDER_NAME}${NC}"
echo "================================"
echo "Log level: $LOG_LEVEL"
if [ -n "$ITEM_LIMIT" ]; then
    echo "Item limit: $(echo $ITEM_LIMIT | grep -oP '\d+')"
fi
if [ -n "$DISABLE_PIPELINE" ]; then
    echo -e "${YELLOW}Database: DISABLED (dry run)${NC}"
else
    echo "Database: PostgreSQL (localhost:5433)"
fi
echo "================================"
echo ""

# Create timestamp for log file
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="logs/scrapy_${TIMESTAMP}.log"

# Run spider with output to both terminal and file
# We disable LOG_FILE setting and use tee instead
scrapy crawl "$SPIDER_NAME" \
    -s LOG_FILE= \
    -s LOG_LEVEL="$LOG_LEVEL" \
    $ITEM_LIMIT \
    $DISABLE_PIPELINE \
    2>&1 | tee "$LOG_FILE"

# Show summary
echo ""
echo -e "${GREEN}✅ Spider completed!${NC}"
echo ""
echo -e "${BLUE}📋 Summary:${NC}"
echo "  Log file: $LOG_FILE"

if [ -z "$DISABLE_PIPELINE" ]; then
    echo ""
    echo -e "${BLUE}💾 View scraped data:${NC}"
    echo "  ./scripts/view_data.sh"
fi
echo ""
