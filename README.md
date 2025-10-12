# 🕷️ Production-Grade Web Scraper Template

> A scalable, production-ready web scraping framework built with Scrapy and PostgreSQL. Demonstrates robust error handling, data validation, and deployment-ready architecture.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Scrapy](https://img.shields.io/badge/scrapy-2.11-green.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-15-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Spiders](#-spiders)
- [Architecture](#-architecture)
- [Configuration](#-configuration)
- [Documentation](#-documentation)
- [Use Cases](#-use-cases)
- [Tech Stack](#-tech-stack)
- [Legal & Ethics](#-legal--ethics)
- [Author](#-author)

---

## 🎯 Overview

This project showcases a **professional-grade web scraping system** designed for real-world data collection needs. Built with best practices for production environments, it demonstrates:

- Clean, maintainable code architecture
- Robust error handling and retry logic
- Data validation and storage pipelines
- Docker containerization for easy deployment
- Comprehensive logging and monitoring

**Perfect for:**
- Portfolio demonstration
- Learning production Scrapy patterns
- Starting point for custom scraper projects
- Interview/technical assessment reference

---

## ✨ Features

### Core Features
- ✅ **Production-Ready Scrapy Configuration** - Rate limiting, retry logic, robots.txt compliance
- ✅ **PostgreSQL Data Pipeline** - Structured storage with proper schema design and UNIQUE constraints
- ✅ **Rotating User Agents** - Built-in user agent rotation to mimic different browsers
- ✅ **Comprehensive Error Handling** - Graceful failure handling with detailed logging
- ✅ **Data Validation** - Scrapy Items with field validation and processors
- ✅ **Docker Support** - Fully containerized with docker-compose for one-command deployment

### Advanced Features
- ✅ **Auto-throttling** - Intelligent request rate adjustment based on server response
- ✅ **Duplicate Prevention** - Database UNIQUE constraints prevent redundant data
- ✅ **Multiple Export Formats** - JSON, CSV, XML, PostgreSQL support
- ✅ **Structured Logging** - Timestamped logs with custom middleware for statistics
- ✅ **Environment Configuration** - `.env` file support for secure credential management
- ✅ **Health Monitoring** - Built-in statistics tracking and error reporting

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL 15+ (or use Docker)
- Git

### Local Installation

```bash
# 1. Clone the repository
git clone https://github.com/product-with-saeed/scrapy-production-template.git
cd scrapy-production-template

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup PostgreSQL database
sudo service postgresql start
sudo -u postgres psql << 'SQL'
CREATE DATABASE scrapy_db;
CREATE USER scrapy WITH PASSWORD 'scrapy';
GRANT ALL PRIVILEGES ON DATABASE scrapy_db TO scrapy;
\c scrapy_db
GRANT ALL ON SCHEMA public TO scrapy;
SQL

# 5. Run a spider
scrapy crawl hackernews

# 6. View the data
psql -U scrapy -d scrapy_db -h localhost -c "SELECT * FROM hackernews LIMIT 5;"
```

### Docker Installation

```bash
# 1. Clone and configure
git clone https://github.com/product-with-saeed/scrapy-production-template.git
cd scrapy-production-template
cp .env.example .env

# 2. Start containers
docker-compose up -d

# 3. Run spiders
docker-compose exec scraper scrapy crawl hackernews
docker-compose exec scraper scrapy crawl quotes
docker-compose exec scraper scrapy crawl books

# 4. Check results
docker-compose exec postgres psql -U scrapy -d scrapy_db -c "SELECT COUNT(*) FROM hackernews;"
```

---

## 🕸️ Spiders

This project includes three distinct spiders demonstrating different scraping scenarios:

### 1. **HackerNews Spider** 
📰 News aggregation from Hacker News front page

**Extracts:**
- Article titles and URLs
- Scores and rankings
- Authors and comment counts
- Timestamps

**Usage:**
```bash
scrapy crawl hackernews
```

**Expected output:** ~30 articles from the front page

---

### 2. **Quotes Spider**
💬 Content collection with pagination support

**Extracts:**
- Quote text
- Author names
- Tags (array)
- Timestamps

**Usage:**
```bash
scrapy crawl quotes
```

**Expected output:** ~100 quotes across all pages

---

### 3. **Books Spider**
📚 E-commerce product scraping with pricing

**Extracts:**
- Book titles
- Prices and availability
- Star ratings
- Product URLs

**Usage:**
```bash
scrapy crawl books
```

**Expected output:** ~1000 books across 50 pages

---

## 🏗️ Architecture

```
scrapy-production-template/
├── scrapers/                    # Main Scrapy project
│   ├── spiders/                 # Spider implementations
│   │   ├── hackernews_spider.py
│   │   ├── quotes_spider.py
│   │   └── books_spider.py
│   ├── items.py                 # Data models with validation
│   ├── pipelines.py             # PostgreSQL pipeline
│   ├── settings.py              # Production configuration
│   └── middlewares.py           # Custom middleware (stats, errors)
├── docs/                        # Comprehensive documentation
│   ├── USAGE.md                 # Usage guide
│   ├── TROUBLESHOOTING.md       # Common issues and solutions
│   └── DEPLOYMENT.md            # Production deployment guide
├── samples/                     # Sample output data
│   ├── hackernews_sample.json
│   ├── quotes_sample.json
│   └── books_sample.json
├── logs/                        # Application logs
├── Dockerfile                   # Container definition
├── docker-compose.yml           # Local development setup
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
└── README.md                    # This file
```

---

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `.env` and customize:

```env
# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_DB=scrapy_db
POSTGRES_USER=scrapy
POSTGRES_PASSWORD=scrapy
POSTGRES_PORT=5432

# Logging
LOG_LEVEL=INFO
```

### Key Settings

In `scrapers/settings.py`:

```python
CONCURRENT_REQUESTS = 16              # Parallel requests
DOWNLOAD_DELAY = 1                    # Seconds between requests
RETRY_TIMES = 3                       # Retry failed requests
AUTOTHROTTLE_ENABLED = True           # Smart rate limiting
ROBOTSTXT_OBEY = True                 # Respect robots.txt
```

### Custom Spider Settings

Override settings per spider:

```python
custom_settings = {
    'DOWNLOAD_DELAY': 2,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    'CLOSESPIDER_ITEMCOUNT': 100
}
```

---

## 📚 Documentation

Comprehensive guides available in the `docs/` directory:

- **[USAGE.md](docs/USAGE.md)** - Detailed usage instructions, query examples, scheduling
- **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Production deployment strategies (AWS, DigitalOcean, Heroku)

### Quick Links

- [Database Queries](docs/USAGE.md#database-queries)
- [Scheduling Spiders](docs/USAGE.md#scheduling)
- [Export Formats](docs/USAGE.md#output-formats)
- [Cloud Deployment](docs/DEPLOYMENT.md#cloud-deployment-options)

---

## 💼 Use Cases

This scraper template is designed for:

| Use Case | Description |
|----------|-------------|
| **E-commerce Monitoring** | Track competitor pricing, product availability, reviews |
| **Job Aggregation** | Collect job listings from multiple boards |
| **News Collection** | Build content databases for analysis |
| **Market Research** | Gather product information and market trends |
| **Real Estate** | Monitor property listings and price changes |
| **Academic Research** | Collect datasets for data science projects |

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.10+ | Core language |
| **Scrapy** | 2.11+ | Web scraping framework |
| **PostgreSQL** | 15+ | Data storage |
| **psycopg2** | 2.9+ | PostgreSQL adapter |
| **Docker** | Latest | Containerization |
| **scrapy-user-agents** | 0.1.1 | User agent rotation |

---

## 🔒 Legal & Ethics

⚠️ **Important Notice**

This project is for **educational and demonstration purposes**. When using this scraper:

- ✅ **Always check** `robots.txt` before scraping
- ✅ **Respect** rate limits and server resources
- ✅ **Review** Terms of Service for target websites
- ✅ **Consider** using official APIs when available
- ✅ **Obtain permission** for commercial use
- ❌ **Never** scrape personal data without consent
- ❌ **Never** bypass anti-scraping measures maliciously

**All included spiders:**
- Respect `robots.txt` rules
- Implement rate limiting
- Target publicly accessible data only
- Are configured for ethical scraping practices

For production use, always verify legal compliance in your jurisdiction.

---

## 🧪 Testing

Run tests and verify functionality:

```bash
# Test individual spider with limited output
scrapy crawl hackernews -s CLOSESPIDER_ITEMCOUNT=5 -o test.json

# Test with debug logging
scrapy crawl quotes -s LOG_LEVEL=DEBUG

# Verify database integrity
psql -U scrapy -d scrapy_db -h localhost << 'SQL'
SELECT 
    'hackernews' as spider, 
    COUNT(*) as records,
    MAX(scraped_at) as last_scraped
FROM hackernews
UNION ALL
SELECT 'quotes', COUNT(*), MAX(scraped_at) FROM quotes
UNION ALL
SELECT 'books', COUNT(*), MAX(scraped_at) FROM books;
SQL

# Run all spiders
./run_all_spiders.sh
```

---

## 📊 Performance

Benchmark results on standard hardware:

| Metric | Value |
|--------|-------|
| **Throughput** | ~100 requests/minute (configurable) |
| **Memory Usage** | <500MB per spider process |
| **Database Performance** | Handles millions of records efficiently |
| **Scalability** | Horizontal scaling with Scrapy Cluster |

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Areas for enhancement:
- Additional spider examples
- Advanced proxy rotation
- Enhanced data validation
- Export to other databases (MongoDB, Elasticsearch)
- Monitoring dashboard
- CI/CD pipeline

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Saeed Mohammadpour**  
*Python/Django Developer | Web Scraping Specialist | AI Product Owner*

Freelance developer specializing in automation, data engineering, and healthtech AI solutions. 10+ years building production systems for EU/UK clients.

- 💼 **LinkedIn:** [Saeed Mohammadpour](https://www.linkedin.com/in/product-with-saeed/)
- 📧 **Email:** product.with.saeed@gmail.com
- 🐙 **GitHub:** [@product-with-saeed](https://github.com/product-with-saeed)
- 💬 **Upwork:** [Saeed Mohammadpour](https://www.upwork.com/freelancers/~0186cad39ef759aae0)

---

## 💬 Need a Custom Scraper?

I build production-grade scraping solutions for businesses:

- ✅ E-commerce price monitoring systems
- ✅ Job board aggregators
- ✅ Real estate data pipelines
- ✅ Market research automation
- ✅ Content collection systems

**Contact me for consultation:** product.with.saeed@gmail.com

---

## ⭐ Show Your Support

If this project helped you, please give it a ⭐ star on GitHub!

---

**Built with ❤️ for the web scraping community**
