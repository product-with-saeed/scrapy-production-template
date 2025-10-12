# Deployment Guide

Production deployment strategies for the scraper system.

## Table of Contents

1. [Local Production Deployment](#local-production-deployment)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment Options](#cloud-deployment-options)
4. [Monitoring & Maintenance](#monitoring--maintenance)
5. [Security Considerations](#security-considerations)

## Local Production Deployment

### Setup Production Environment

```bash
# Clone repository
git clone <your-repo-url>
cd scrapy-production-template

# Create production virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup production database
sudo -u postgres psql << 'SQL'
CREATE DATABASE scrapy_prod;
CREATE USER scrapy_prod WITH ENCRYPTED PASSWORD 'strong_password_here';
GRANT ALL PRIVILEGES ON DATABASE scrapy_prod TO scrapy_prod;
\c scrapy_prod
GRANT ALL ON SCHEMA public TO scrapy_prod;
SQL

# Create production .env file
cat > .env << 'ENV'
POSTGRES_HOST=localhost
POSTGRES_DB=scrapy_prod
POSTGRES_USER=scrapy_prod
POSTGRES_PASSWORD=strong_password_here
POSTGRES_PORT=5432
LOG_LEVEL=INFO
ENV

# Create systemd service for automatic restart
sudo tee /etc/systemd/system/scrapy-hackernews.service << 'SERVICE'
[Unit]
Description=Scrapy HackerNews Spider
After=network.target postgresql.service

[Service]
Type=oneshot
User=your_username
WorkingDirectory=/path/to/scrapy-production-template
Environment="PATH=/path/to/scrapy-production-template/venv/bin"
ExecStart=/path/to/scrapy-production-template/venv/bin/scrapy crawl hackernews
StandardOutput=append:/var/log/scrapy/hackernews.log
StandardError=append:/var/log/scrapy/hackernews-error.log

[Install]
WantedBy=multi-user.target
SERVICE

# Create log directory
sudo mkdir -p /var/log/scrapy
sudo chown your_username:your_username /var/log/scrapy

# Enable and test service
sudo systemctl daemon-reload
sudo systemctl enable scrapy-hackernews.service
sudo systemctl start scrapy-hackernews.service
sudo systemctl status scrapy-hackernews.service
```

### Setup Cron Jobs

```bash
# Edit crontab
crontab -e

# Add scheduled jobs
# HackerNews every 6 hours
0 */6 * * * cd /path/to/scrapy-production-template && source venv/bin/activate && scrapy crawl hackernews >> /var/log/scrapy/hackernews.log 2>&1

# Quotes daily at 2 AM
0 2 * * * cd /path/to/scrapy-production-template && source venv/bin/activate && scrapy crawl quotes >> /var/log/scrapy/quotes.log 2>&1

# Books weekly on Sunday at 3 AM
0 3 * * 0 cd /path/to/scrapy-production-template && source venv/bin/activate && scrapy crawl books >> /var/log/scrapy/books.log 2>&1

# Database backup daily at 4 AM
0 4 * * * pg_dump -U scrapy_prod scrapy_prod > /backups/scrapy_$(date +\%Y\%m\%d).sql
```

## Docker Deployment

### Production Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: scrapy_postgres_prod
    restart: always
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_prod_data:/var/lib/postgresql/data
      - ./backups:/backups
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - scrapy_network

  scraper:
    build: .
    container_name: scrapy_scraper_prod
    restart: always
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      POSTGRES_HOST: postgres
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_PORT: 5432
      LOG_LEVEL: INFO
    volumes:
      - ./scrapers:/app/scrapers
      - ./logs:/app/logs
      - ./data:/app/data
    networks:
      - scrapy_network
    command: tail -f /dev/null

volumes:
  postgres_prod_data:

networks:
  scrapy_network:
    driver: bridge
```

### Deploy with Docker

```bash
# Create production .env
cp .env.example .env
# Edit .env with production credentials

# Build and start
docker-compose -f docker-compose.prod.yml up -d

# Run spiders
docker-compose -f docker-compose.prod.yml exec scraper scrapy crawl hackernews

# View logs
docker-compose -f docker-compose.prod.yml logs -f scraper

# Backup database
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U scrapy scrapy_db > backup.sql

# Stop services
docker-compose -f docker-compose.prod.yml down
```

## Cloud Deployment Options

### Option 1: AWS EC2

**Requirements:**
- EC2 instance (t2.micro or larger)
- PostgreSQL RDS instance
- Security groups configured

**Setup Steps:**

```bash
# SSH into EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv git postgresql-client -y

# Clone and setup
git clone <your-repo>
cd scrapy-production-template
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure .env with RDS endpoint
cat > .env << 'ENV'
POSTGRES_HOST=your-rds-endpoint.region.rds.amazonaws.com
POSTGRES_DB=scrapy_prod
POSTGRES_USER=admin
POSTGRES_PASSWORD=your_rds_password
POSTGRES_PORT=5432
ENV

# Setup cron jobs (as shown above)
```

**Estimated Monthly Cost:** $15-30 (t2.micro EC2 + db.t3.micro RDS)

### Option 2: DigitalOcean Droplet

**Requirements:**
- Droplet ($6/month minimum)
- Managed PostgreSQL database ($15/month)

**Setup Steps:**

```bash
# Similar to EC2 setup
# Use DigitalOcean's managed database connection string
POSTGRES_HOST=your-db-cluster.db.ondigitalocean.com
```

**Estimated Monthly Cost:** $21+

### Option 3: Heroku

**Requirements:**
- Heroku account
- Heroku Postgres addon

**Setup Steps:**

```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create your-scraper-app

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Configure buildpack
echo "python-3.10.12" > runtime.txt

# Create Procfile
echo "worker: scrapy crawl hackernews" > Procfile

# Deploy
git push heroku main

# Run spider
heroku run scrapy crawl hackernews

# Schedule with Heroku Scheduler addon
heroku addons:create scheduler:standard
```

**Estimated Monthly Cost:** $7-25

### Option 4: Docker on VPS

**Any VPS provider (Linode, Vultr, etc.):**

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone and deploy
git clone <your-repo>
cd scrapy-production-template
docker-compose -f docker-compose.prod.yml up -d
```

## Monitoring & Maintenance

### Setup Monitoring

**1. Log Rotation:**

```bash
# Create logrotate config
sudo tee /etc/logrotate.d/scrapy << 'LOGROTATE'
/var/log/scrapy/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 your_username your_username
}
LOGROTATE
```

**2. Database Monitoring:**

```sql
-- Check database size
SELECT pg_size_pretty(pg_database_size('scrapy_prod'));

-- Check table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Active connections
SELECT count(*) FROM pg_stat_activity WHERE datname = 'scrapy_prod';
```

**3. Health Check Script:**

```bash
#!/bin/bash
# health_check.sh

# Check PostgreSQL
if ! pg_isready -U scrapy_prod -h localhost > /dev/null 2>&1; then
    echo "❌ PostgreSQL is down!"
    # Send alert (email, Slack, etc.)
fi

# Check disk space
DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 80 ]; then
    echo "⚠️  Disk usage above 80%: ${DISK_USAGE}%"
fi

# Check recent scraping activity
RECENT_ITEMS=$(psql -U scrapy_prod -d scrapy_prod -t -c "SELECT COUNT(*) FROM hackernews WHERE scraped_at > NOW() - INTERVAL '1 day';")
if [ "$RECENT_ITEMS" -lt 10 ]; then
    echo "⚠️  Low scraping activity: only ${RECENT_ITEMS} items in last 24h"
fi

echo "✅ All checks passed"
```

Run health checks hourly:
```bash
0 * * * * /path/to/health_check.sh >> /var/log/scrapy/health.log 2>&1
```

### Maintenance Tasks

**Weekly:**
- Review error logs
- Check database size
- Verify cron jobs running
- Test spider selectors (sites may change)

**Monthly:**
- Update dependencies: `pip install --upgrade -r requirements.txt`
- Database optimization: `VACUUM ANALYZE;`
- Review and archive old data
- Security updates: `apt update && apt upgrade`

**Quarterly:**
- Review scraping targets (still relevant?)
- Update user agents list
- Performance optimization
- Backup testing (restore from backup)

## Security Considerations

### 1. Database Security

```bash
# Use strong passwords
# Never commit credentials to Git
# Use environment variables

# Enable SSL for PostgreSQL connections
# In postgresql.conf:
ssl = on
ssl_cert_file = '/etc/ssl/certs/server.crt'
ssl_key_file = '/etc/ssl/private/server.key'

# Configure pg_hba.conf for SSL only:
hostssl all all 0.0.0.0/0 md5
```

### 2. Network Security

```bash
# Firewall rules (ufw)
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 5432/tcp  # PostgreSQL (if external access needed)
sudo ufw enable

# Or use iptables
sudo iptables -A INPUT -p tcp --dport 5432 -s trusted_ip -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 5432 -j DROP
```

### 3. Application Security

```python
# In settings.py - Never expose in logs
import os

# Use environment variables
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')  # Never hardcode

# Validate scraped data before storage
# Sanitize inputs
# Use parameterized queries (already done in pipelines.py)
```

### 4. Access Control

```bash
# Limit SSH access
# Use SSH keys, disable password auth
# In /etc/ssh/sshd_config:
PasswordAuthentication no
PermitRootLogin no

# Create limited user for scraper
sudo adduser scraper
sudo usermod -aG sudo scraper  # Only if needed
```

### 5. Secrets Management

**Use environment variables:**
```bash
export POSTGRES_PASSWORD="$(openssl rand -base64 32)"
```

**Or use secrets management tools:**
- AWS Secrets Manager
- HashiCorp Vault
- Docker secrets

## Backup Strategy

### Automated Backups

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="scrapy_prod"

# Create backup
pg_dump -U scrapy_prod $DB_NAME | gzip > $BACKUP_DIR/scrapy_${DATE}.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "scrapy_*.sql.gz" -mtime +30 -delete

# Upload to S3 (optional)
# aws s3 cp $BACKUP_DIR/scrapy_${DATE}.sql.gz s3://your-bucket/backups/

echo "✅ Backup completed: scrapy_${DATE}.sql.gz"
```

Schedule daily:
```bash
0 4 * * * /path/to/backup.sh >> /var/log/scrapy/backup.log 2>&1
```

### Restore from Backup

```bash
# Restore from compressed backup
gunzip -c /backups/scrapy_20241012.sql.gz | psql -U scrapy_prod scrapy_prod

# Or from uncompressed
psql -U scrapy_prod scrapy_prod < /backups/scrapy_20241012.sql
```

## Scaling Considerations

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize PostgreSQL configuration
- Use connection pooling (PgBouncer)

### Horizontal Scaling
- Use Scrapy Cluster for distributed scraping
- Load balance with multiple scraper instances
- Shard PostgreSQL database by spider/date

### Performance Optimization
- Index frequently queried columns
- Partition large tables by date
- Use Redis for caching
- Implement queue system (RabbitMQ, Celery)

## Production Checklist

Before going live:

- [ ] Strong passwords for all services
- [ ] SSL/TLS enabled for database connections
- [ ] Firewall configured
- [ ] Backups scheduled and tested
- [ ] Monitoring and alerting setup
- [ ] Log rotation configured
- [ ] Health checks running
- [ ] Documentation updated
- [ ] Error handling tested
- [ ] Rate limiting appropriate
- [ ] robots.txt compliance verified
- [ ] Terms of Service reviewed for all targets
- [ ] Cost monitoring setup (if cloud)
- [ ] Disaster recovery plan documented

## Support

For deployment issues:
- Check logs in `/var/log/scrapy/`
- Review systemd service status
- Verify database connectivity
- Test network access to target sites
- Review cloud provider documentation
