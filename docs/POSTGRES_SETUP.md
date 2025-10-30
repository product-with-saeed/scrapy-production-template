# PostgreSQL Setup Guide

This guide explains how to set up and use PostgreSQL with the Scrapy project.

## Quick Start

The easiest way to set up PostgreSQL is using the provided setup script:

```bash
./scripts/setup_postgres.sh
```

This script will:

1. Start the PostgreSQL Docker container
2. Wait for the database to be ready
3. Test the connection

## Manual Setup

If you prefer to set up manually:

### Option 1: Using Docker (Recommended)

1. **Start PostgreSQL container:**

   ```bash
   docker-compose up -d postgres
   ```

2. **Verify it's running:**

   ```bash
   docker-compose ps
   ```

3. **Check logs if needed:**

   ```bash
   docker-compose logs postgres
   ```

### Option 2: Using Local PostgreSQL

If you want to use a local PostgreSQL installation instead of Docker:

1. **Create the database user:**

   ```bash
   sudo -u postgres createuser -P scrapy
   # Enter password: change_this_password_in_production
   ```

2. **Create the database:**

   ```bash
   sudo -u postgres createdb -O scrapy scrapy_db
   ```

3. **Update .env file** to match your local setup if needed.

## Configuration

The project uses environment variables for database configuration. These are loaded from the `.env` file:

```bash
POSTGRES_HOST=localhost        # Use 'postgres' when running in Docker
POSTGRES_DB=scrapy_db
POSTGRES_USER=scrapy
POSTGRES_PASSWORD=change_this_password_in_production
POSTGRES_PORT=5432
```

### Settings Hierarchy

The [settings.py](../scrapers/settings.py) file loads configuration in this order:

1. **Environment variables** (from `.env` file via `python-dotenv`)
2. **Default values** (fallback if env vars not set)

Example from settings.py:

```python
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'scrapy_db')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'scrapy')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'scrapy')
POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5432))
```

## Database Schema

The PostgresPipeline automatically creates tables when spiders run:

### HackerNews Table

```sql
CREATE TABLE IF NOT EXISTS hackernews (
    id SERIAL PRIMARY KEY,
    title TEXT,
    url TEXT,
    rank TEXT,
    score TEXT,
    author TEXT,
    comments TEXT,
    item_id TEXT UNIQUE,
    scraped_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Quotes Table

```sql
CREATE TABLE IF NOT EXISTS quotes (
    id SERIAL PRIMARY KEY,
    text TEXT,
    author TEXT,
    tags TEXT[],
    scraped_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Books Table

```sql
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title TEXT,
    price TEXT,
    availability TEXT,
    rating TEXT,
    url TEXT UNIQUE,
    scraped_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Troubleshooting

### Error: "password authentication failed for user 'scrapy'"

This usually means one of:

1. **PostgreSQL is not running:**

   ```bash
   docker-compose up -d postgres
   ```

2. **Wrong password in .env:**
   - Check that `.env` file has the correct password
   - Default is `change_this_password_in_production`
   - Match it with what's in `docker-compose.yml`

3. **Local PostgreSQL conflict:**
   - If you have PostgreSQL installed locally on port 5432
   - Either stop local PostgreSQL or change Docker port
   - Edit `docker-compose.yml` ports to `"5433:5432"`
   - Update `.env` with `POSTGRES_PORT=5433`

### Error: "could not connect to server"

1. **Check if PostgreSQL is running:**

   ```bash
   docker-compose ps
   ```

2. **Check if port is accessible:**

   ```bash
   pg_isready -h localhost -p 5432 -U scrapy
   ```

3. **Check Docker logs:**

   ```bash
   docker-compose logs postgres
   ```

### Verify Database Connection

Using Docker exec:

```bash
docker-compose exec postgres psql -U scrapy -d scrapy_db
```

Using psql from host (requires `postgresql-client`):

```bash
PGPASSWORD=change_this_password_in_production psql -h localhost -p 5432 -U scrapy -d scrapy_db
```

### View Scraped Data

```bash
# Connect to database
docker-compose exec postgres psql -U scrapy -d scrapy_db

# View HackerNews data
SELECT * FROM hackernews ORDER BY created_at DESC LIMIT 10;

# View Quotes data
SELECT * FROM quotes ORDER BY created_at DESC LIMIT 10;

# View Books data
SELECT * FROM books ORDER BY created_at DESC LIMIT 10;

# Count records
SELECT COUNT(*) FROM hackernews;
```

## Running Spiders

Once PostgreSQL is set up, you can run spiders:

```bash
# Run individual spiders
scrapy crawl hackernews
scrapy crawl quotes
scrapy crawl books

# Run with Docker
docker-compose run scraper scrapy crawl hackernews
```

## Testing

The test suite uses mocked database connections, so you don't need PostgreSQL running to run tests:

```bash
pytest tests/
```

## Production Considerations

1. **Change the default password** in `.env` and `docker-compose.yml`
2. **Use environment-specific .env files** (`.env.production`, `.env.staging`)
3. **Set up database backups**
4. **Consider connection pooling** for high-volume scraping
5. **Add indexes** on frequently queried columns
6. **Monitor database size** and implement data retention policies
