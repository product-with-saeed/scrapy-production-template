# Sample Output Data

This directory contains sample outputs from each spider to demonstrate the data structure and quality.

## Files

- `hackernews_sample.json` - 5 articles from Hacker News front page
- `quotes_sample.json` - 10 quotes with authors and tags
- `books_sample.json` - 10 books with pricing and ratings
- `hackernews_sample.csv` - Same data in CSV format
- `quotes_sample.csv` - Same data in CSV format

## Data Quality Features

✅ Clean, structured data
✅ Consistent field naming
✅ ISO timestamp for all records
✅ No missing critical fields
✅ Proper data types

## Full Data Collection

When running without limits:
- **HackerNews**: ~30 articles (front page)
- **Quotes**: ~100 quotes (all pages)
- **Books**: ~1000 books (50 pages)

## Export Formats Supported

- JSON
- CSV
- XML
- PostgreSQL (primary storage)
- JSON Lines
- Pickle

Run spiders with custom output:
```bash
scrapy crawl hackernews -o output.json
scrapy crawl quotes -o output.csv
scrapy crawl books -o output.xml
```

## 📊 Sample data structure (first item from hackernews):
{
  "title": "Macro Gaussian Splats",
  "url": "https://danybittel.ch/macro.html",
  "rank": "1.",
  "item_id": "45556952",
  "score": "244 points",
  "author": "danybittel",
  "comments": "38\u00a0comments",
  "scraped_at": "2025-10-12T17:25:54.759949"
}