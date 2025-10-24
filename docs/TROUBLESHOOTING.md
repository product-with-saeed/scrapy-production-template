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
