# Running Spiders Guide

This guide explains how to run spiders and view the scraped data.

## Quick Start

### Run a Spider with Terminal Output

```bash
./scripts/run_spider.sh hackernews
```

This will:
- Show output in your terminal in real-time
- Save logs to `logs/` directory
- Store data in PostgreSQL database

### View Scraped Data

```bash
./scripts/view_data.sh
```

This shows a summary of all scraped data from the database.

## Available Spiders

### 1. HackerNews Spider (`hackernews`)

Scrapes the front page of Hacker News.

**Data collected:**
- Article title
- URL
- Rank on front page
- Points/score
- Author
- Number of comments
- Item ID

**Run:**
```bash
./scripts/run_spider.sh hackernews
```

**Database table:** `hackernews`

### 2. Quotes Spider (`quotes`)

Scrapes quotes from http://quotes.toscrape.com

**Data collected:**
- Quote text
- Author name
- Tags

**Run:**
```bash
./scripts/run_spider.sh quotes
```

**Database table:** `quotes`

### 3. Books Spider (`books`)

Scrapes book information from http://books.toscrape.com

**Data collected:**
- Book title
- Price
- Availability
- Star rating
- Product URL

**Run:**
```bash
./scripts/run_spider.sh books
```

**Database table:** `books`

## Running Options

### Limit Number of Items

Scrape only a specific number of items:

```bash
./scripts/run_spider.sh quotes --limit 10
```

### Debug Mode

Enable debug logging to see detailed information:

```bash
./scripts/run_spider.sh hackernews --debug
```

### Dry Run (No Database)

Run spider without saving to database (testing):

```bash
./scripts/run_spider.sh books --no-db
```

### Combine Options

You can combine multiple options:

```bash
./scripts/run_spider.sh quotes --limit 5 --debug
```

## Direct Scrapy Commands

If you prefer using Scrapy directly:

### Basic Run

```bash
scrapy crawl hackernews
```

**Note:** Output will go to log files only (see `logs/` directory)

### With Terminal Output

```bash
scrapy crawl quotes -s LOG_FILE=
```

The `-s LOG_FILE=` disables file logging and shows output in terminal.

### Limit Items

```bash
scrapy crawl books -s CLOSESPIDER_ITEMCOUNT=10
```

### Debug Mode

```bash
scrapy crawl hackernews -s LOG_LEVEL=DEBUG
```

### Disable Database

```bash
scrapy crawl quotes -s ITEM_PIPELINES={}
```

## Viewing Data

### Quick Summary

```bash
./scripts/view_data.sh
```

Shows latest 5 items from each table.

### Connect to Database

```bash
docker exec -it scrapy_postgres psql -U scrapy -d scrapy_db
```

Then run SQL queries:

```sql
-- View all HackerNews articles
SELECT * FROM hackernews ORDER BY created_at DESC;

-- View quotes by a specific author
SELECT text FROM quotes WHERE author = 'Albert Einstein';

-- Count books by rating
SELECT rating, COUNT(*) FROM books GROUP BY rating;

-- View latest scraped items
SELECT title, scraped_at FROM hackernews ORDER BY scraped_at DESC LIMIT 10;
```

### Query from Command Line

```bash
# Count items
docker exec scrapy_postgres psql -U scrapy -d scrapy_db -c "SELECT COUNT(*) FROM quotes;"

# View specific data
docker exec scrapy_postgres psql -U scrapy -d scrapy_db -c "SELECT title, url FROM hackernews LIMIT 5;"

# Export to CSV
docker exec scrapy_postgres psql -U scrapy -d scrapy_db -c "COPY (SELECT * FROM hackernews) TO STDOUT CSV HEADER" > hackernews.csv
```

## Log Files

All spider runs create log files in the `logs/` directory:

```bash
# View latest log
tail -f logs/$(ls -t logs/ | head -1)

# Search for errors
grep ERROR logs/*.log

# View specific spider's logs
ls -lht logs/
tail -100 logs/scrapy_20251030_043120.log
```

## Understanding Spider Output

When you run a spider, you'll see:

1. **Spider Initialization**
   - Middleware and pipelines being loaded
   - Database connection established

2. **Scraping Progress**
   - Requests being made
   - Items being scraped
   - Pages being crawled

3. **Statistics**
   - Total items scraped
   - Pages crawled
   - Response codes
   - Errors (if any)

4. **Spider Closure**
   - Database connection closed
   - Final statistics dump

Example output:
```
🕷️  Running Spider: quotes
================================
Log level: INFO
Database: PostgreSQL (localhost:5433)
================================

2025-10-30 04:31:21 [scrapy.core.engine] INFO: Spider opened
2025-10-30 04:31:21 [scrapers.pipelines] INFO: Connected to PostgreSQL for spider: quotes
2025-10-30 04:31:23 [scrapy.core.scraper] DEBUG: Scraped from <200 http://quotes.toscrape.com/>
{'text': '"The world as we have created it..."', 'author': 'Albert Einstein', 'tags': [...]}
...
2025-10-30 04:31:23 [scrapers.middlewares] INFO: ✅ Spider closed: quotes
2025-10-30 04:31:23 [scrapers.middlewares] INFO:    Items scraped: 10
2025-10-30 04:31:23 [scrapers.middlewares] INFO:    Pages crawled: 2
```

## Troubleshooting

### No Output in Terminal

**Problem:** Spider runs but nothing appears in terminal.

**Solution:** Use the wrapper script:
```bash
./scripts/run_spider.sh hackernews
```

Or disable LOG_FILE:
```bash
scrapy crawl hackernews -s LOG_FILE=
```

### Database Connection Error

**Problem:** `connection to server at "localhost" ... failed`

**Solution:** Start PostgreSQL:
```bash
./scripts/setup_postgres.sh
```

### No Data in Database

**Problem:** Spider completes but no data in database.

**Check:**
1. Look for errors in logs
2. Verify PostgreSQL is running: `docker ps | grep scrapy_postgres`
3. Check pipeline is enabled in settings.py
4. Verify network connectivity to target website

### Spider Stops Immediately

**Problem:** Spider closes right after opening.

**Possible causes:**
1. Target website is blocking requests
2. No items match the selectors (website structure changed)
3. Item limit reached (if using CLOSESPIDER_ITEMCOUNT)

**Solution:** Run with debug mode:
```bash
./scripts/run_spider.sh hackernews --debug
```

## Advanced Usage

### Schedule Regular Scraping

Use cron to schedule regular scraping:

```bash
# Edit crontab
crontab -e

# Add line to scrape HackerNews every hour
0 * * * * cd /path/to/scrapy-production-template && ./scripts/run_spider.sh hackernews >> logs/cron.log 2>&1
```

### Run Multiple Spiders

```bash
# Sequential
./scripts/run_spider.sh hackernews && \
./scripts/run_spider.sh quotes && \
./scripts/run_spider.sh books

# Parallel (careful with resources)
./scripts/run_spider.sh hackernews &
./scripts/run_spider.sh quotes &
./scripts/run_spider.sh books &
wait
```

### Export Data

```bash
# To JSON
docker exec scrapy_postgres psql -U scrapy -d scrapy_db -t -c \
  "SELECT json_agg(row_to_json(t)) FROM (SELECT * FROM hackernews) t" > data.json

# To CSV
docker exec scrapy_postgres psql -U scrapy -d scrapy_db -c \
  "COPY hackernews TO STDOUT CSV HEADER" > hackernews.csv
```

## Best Practices

1. **Start Small**: Use `--limit` when testing spiders
2. **Check Logs**: Always review logs for errors and warnings
3. **Monitor Resources**: Watch CPU/memory usage during scraping
4. **Respect Robots.txt**: The spiders obey robots.txt by default
5. **Rate Limiting**: AutoThrottle is enabled to prevent overwhelming servers
6. **Data Quality**: Verify scraped data matches expected format
7. **Database Backups**: Regularly backup your PostgreSQL data

## See Also

- [PostgreSQL Setup Guide](POSTGRES_SETUP.md)
- [Activity Plan](ACTIVITY_PLAN.md)
- [Fixed Issues](FIXED_ISSUES.md)
