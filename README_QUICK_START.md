# Quick Start Guide

## 1. View Current Data

```bash
./scripts/view_data.sh
```

This shows you what's already been scraped and stored in the database.

## 2. Run a Spider (with terminal output)

```bash
# Run HackerNews spider
./scripts/run_spider.sh hackernews

# Run Quotes spider with limit
./scripts/run_spider.sh quotes --limit 10

# Run Books spider in debug mode
./scripts/run_spider.sh books --debug
```

## 3. Check the Results

```bash
./scripts/view_data.sh
```

## Where is the Data?

All scraped data is stored in **PostgreSQL database**:
- **HackerNews articles** → `hackernews` table
- **Quotes** → `quotes` table  
- **Books** → `books` table

## Why Don't I See Output in Terminal?

By default, Scrapy logs go to files in the `logs/` directory. Use the helper scripts above to see real-time output:

```bash
# ✅ This shows output in terminal
./scripts/run_spider.sh quotes

# ❌ This only logs to file
scrapy crawl quotes
```

## Database Access

Connect directly to the database:

```bash
docker exec -it scrapy_postgres psql -U scrapy -d scrapy_db
```

Then run SQL:
```sql
SELECT * FROM quotes LIMIT 10;
SELECT title, author FROM hackernews ORDER BY score DESC LIMIT 5;
```

## More Information

- [Running Spiders Guide](docs/RUNNING_SPIDERS.md) - Complete spider documentation
- [PostgreSQL Setup](docs/POSTGRES_SETUP.md) - Database configuration
- [Activity Plan](docs/ACTIVITY_PLAN.md) - Project roadmap
