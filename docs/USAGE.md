# Usage Guide

Complete guide for running and customizing the scrapers.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Advanced Configuration](#advanced-configuration)
3. [Output Formats](#output-formats)
4. [Database Queries](#database-queries)
5. [Scheduling](#scheduling)
6. [Troubleshooting](#troubleshooting)

## Basic Usage

### Running Individual Spiders

```bash
# Activate virtual environment
source venv/bin/activate

# Run specific spider
scrapy crawl hackernews
scrapy crawl quotes
scrapy crawl books

# Run with custom log level
scrapy crawl hackernews -s LOG_LEVEL=DEBUG

# Limit number of items
scrapy crawl quotes -s CLOSESPIDER_ITEMCOUNT=50
```

### Running All Spiders

```bash
# Use the helper script
./run_all_spiders.sh

# Or run sequentially
scrapy crawl hackernews && scrapy crawl quotes && scrapy crawl books
```

## Advanced Configuration

### Custom Settings Override

```bash
# Change download delay
scrapy crawl books -s DOWNLOAD_DELAY=2

# Increase concurrency
scrapy crawl quotes -s CONCURRENT_REQUESTS=32

# Disable AutoThrottle
scrapy crawl hackernews -s AUTOTHROTTLE_ENABLED=False
```

### Environment Variables

Create a `.env` file:

```env
POSTGRES_HOST=localhost
POSTGRES_DB=scrapy_db
POSTGRES_USER=scrapy
POSTGRES_PASSWORD=scrapy
POSTGRES_PORT=5432
LOG_LEVEL=INFO
```

Load before running:

```bash
export $(cat .env | xargs)
scrapy crawl hackernews
```

## Output Formats

### Export to JSON

```bash
# Single file
scrapy crawl hackernews -o output.json

# JSON Lines (one object per line)
scrapy crawl quotes -o output.jsonl

# Pretty printed
scrapy crawl books -o output.json -s FEED_EXPORT_INDENT=2
```

### Export to CSV

```bash
scrapy crawl hackernews -o output.csv

# Custom CSV format
scrapy crawl quotes -o output.csv -s FEED_EXPORT_FIELDS="author,text,tags"
```

### Export to XML

```bash
scrapy crawl books -o output.xml
```

### Multiple Outputs

```bash
# Save to both database and file
scrapy crawl hackernews -o backup.json

# The PostgreSQL pipeline still runs
```

## Database Queries

### Connect to Database

```bash
psql -U scrapy -d scrapy_db -h localhost
```

### Common Queries

```sql
-- Count records per spider
SELECT 'hackernews' as spider, COUNT(*) FROM hackernews
UNION ALL
SELECT 'quotes', COUNT(*) FROM quotes
UNION ALL
SELECT 'books', COUNT(*) FROM books;

-- Recent HackerNews articles
SELECT title, score, author 
FROM hackernews 
ORDER BY scraped_at DESC 
LIMIT 10;

-- Top scored HackerNews articles
SELECT title, score, url 
FROM hackernews 
WHERE score IS NOT NULL
ORDER BY CAST(REPLACE(score, ' points', '') AS INTEGER) DESC 
LIMIT 10;

-- Quotes by specific author
SELECT text, tags 
FROM quotes 
WHERE author = 'Albert Einstein';

-- Books by price range
SELECT title, price, rating 
FROM books 
WHERE price LIKE '£1%' OR price LIKE '£2%'
ORDER BY price;

-- Books with 5-star rating
SELECT title, price 
FROM books 
WHERE rating = 'Five'
ORDER BY title;

-- Most common tags in quotes
SELECT UNNEST(tags) as tag, COUNT(*) as count
FROM quotes
GROUP BY tag
ORDER BY count DESC
LIMIT 10;

-- Daily scraping stats
SELECT DATE(scraped_at) as date, COUNT(*) as items
FROM hackernews
GROUP BY DATE(scraped_at)
ORDER BY date DESC;
```

### Export from Database

```bash
# Export to CSV
psql -U scrapy -d scrapy_db -h localhost -c "COPY hackernews TO '/tmp/hackernews.csv' CSV HEADER;"

# Export specific query
psql -U scrapy -d scrapy_db -h localhost -c "COPY (SELECT title, score FROM hackernews WHERE score IS NOT NULL) TO '/tmp/top_stories.csv' CSV HEADER;"
```

## Scheduling

### Using Cron (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add entries (run every 6 hours)
0 */6 * * * cd /path/to/scrapy-production-template && source venv/bin/activate && scrapy crawl hackernews >> logs/cron.log 2>&1

# Run daily at 2 AM
0 2 * * * cd /path/to/scrapy-production-template && ./run_all_spiders.sh >> logs/daily.log 2>&1
```

### Using Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., daily at 2 AM)
4. Action: Start a program
5. Program: `C:\Path\To\Python\python.exe`
6. Arguments: `-m scrapy crawl hackernews`
7. Start in: `C:\Path\To\scrapy-production-template`

### Using Docker Cron

Add to `docker-compose.yml`:

```yaml
  scheduler:
    build: .
    depends_on:
      - postgres
    environment:
      POSTGRES_HOST: postgres
    volumes:
      - ./scrapers:/app/scrapers
    command: >
      sh -c "apt-get update && apt-get install -y cron &&
             echo '0 */6 * * * cd /app && scrapy crawl hackernews' | crontab - &&
             cron -f"
```

## Troubleshooting

### Spider Not Finding Data

**Problem:** Spider completes but extracts 0 items

**Solutions:**
1. Check if selectors are correct:
```bash
scrapy shell "http://quotes.toscrape.com"
>>> response.css('div.quote').getall()
```

2. Check robots.txt compliance:
```bash
scrapy crawl quotes -s ROBOTSTXT_OBEY=False
```

3. Verify website hasn't changed structure

### Database Connection Errors

**Problem:** `psycopg2.OperationalError`

**Solutions:**
1. Check PostgreSQL is running:
```bash
sudo service postgresql status
```

2. Verify credentials in `.env` file

3. Test connection manually:
```bash
psql -U scrapy -d scrapy_db -h localhost
```

4. Check permissions:
```sql
GRANT ALL ON SCHEMA public TO scrapy;
```

### Rate Limiting / Getting Blocked

**Problem:** Spider getting HTTP 429 or 403 errors

**Solutions:**
1. Increase download delay:
```bash
scrapy crawl books -s DOWNLOAD_DELAY=3
```

2. Enable AutoThrottle:
```python
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
```

3. Rotate user agents (already enabled)

4. Consider using proxies (see Advanced section)

### Memory Issues

**Problem:** Spider consuming too much memory

**Solutions:**
1. Limit concurrent requests:
```bash
scrapy crawl books -s CONCURRENT_REQUESTS=8
```

2. Limit items per spider:
```bash
scrapy crawl books -s CLOSESPIDER_ITEMCOUNT=500
```

3. Use pagination more carefully

### Slow Performance

**Problem:** Scraping takes too long

**Solutions:**
1. Increase concurrency:
```bash
scrapy crawl books -s CONCURRENT_REQUESTS=32 -s CONCURRENT_REQUESTS_PER_DOMAIN=8
```

2. Disable AutoThrottle:
```bash
scrapy crawl quotes -s AUTOTHROTTLE_ENABLED=False
```

3. Reduce download delay:
```bash
scrapy crawl hackernews -s DOWNLOAD_DELAY=0.5
```

**Note:** Balance speed with being respectful to target servers.

## Best Practices

1. **Always respect robots.txt** - Keep `ROBOTSTXT_OBEY = True`
2. **Use appropriate delays** - Don't hammer servers
3. **Handle errors gracefully** - Log and continue
4. **Validate data** - Use Scrapy Items
5. **Monitor logs** - Check for errors regularly
6. **Backup database** - Regular PostgreSQL dumps
7. **Test selectors** - Use `scrapy shell` before deploying
8. **Version control** - Commit working spiders

## Performance Tuning

### Optimize for Speed

```python
# settings.py
CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_DOMAIN = 8
DOWNLOAD_DELAY = 0
AUTOTHROTTLE_ENABLED = False
```

### Optimize for Reliability

```python
# settings.py
CONCURRENT_REQUESTS = 8
CONCURRENT_REQUESTS_PER_DOMAIN = 2
DOWNLOAD_DELAY = 2
AUTOTHROTTLE_ENABLED = True
RETRY_TIMES = 5
```

## Getting Help

- Check logs in `logs/` directory
- Use `scrapy shell` to test selectors
- Run with `LOG_LEVEL=DEBUG` for detailed output
- Review Scrapy documentation: https://docs.scrapy.org
EOF

# Create troubleshooting guide
cat > docs/TROUBLESHOOTING.md << 'EOF'
# Troubleshooting Guide

Common issues and their solutions.

## Installation Issues

### psycopg2 Build Error

**Error:** `Error: pg_config executable not found`

**Solution:**
```bash
sudo apt-get install libpq-dev python3-dev
pip install psycopg2-binary
```

### Twisted Reactor Error

**Error:** `reactor already installed`

**Solution:**
Update `settings.py`:
```python
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
```

## Runtime Issues

### Empty Results

Check if selectors match:
```bash
scrapy shell "http://books.toscrape.com"
>>> response.css('article.product_pod').getall()
```

### Database Locked

PostgreSQL connection limit reached:
```sql
SELECT * FROM pg_stat_activity WHERE datname = 'scrapy_db';
-- Kill idle connections
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'scrapy_db' AND state = 'idle';
```

### Memory Leak

Reduce batch size or restart spider periodically:
```bash
scrapy crawl books -s CLOSESPIDER_ITEMCOUNT=1000
```

## Docker Issues

### Container Won't Start

Check logs:
```bash
docker-compose logs postgres
docker-compose logs scraper
```

### Database Not Ready

Increase health check timeout in `docker-compose.yml`:
```yaml
healthcheck:
  interval: 10s
  timeout: 10s
  retries: 10
```

## Contact

For issues not covered here, check:
- Scrapy documentation
- PostgreSQL documentation
- Project GitHub issues
