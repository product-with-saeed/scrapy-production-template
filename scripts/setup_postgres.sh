#!/bin/bash
# Setup PostgreSQL database for Scrapy project
# This script starts the Docker PostgreSQL container and creates necessary tables

set -e

echo "🐘 Setting up PostgreSQL for Scrapy..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Stop any existing container
echo "📦 Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Start PostgreSQL container
echo "🚀 Starting PostgreSQL container..."
docker-compose up -d postgres

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
for i in {1..30}; do
    if docker-compose exec -T postgres pg_isready -U scrapy > /dev/null 2>&1; then
        echo "✅ PostgreSQL is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Error: PostgreSQL failed to start"
        exit 1
    fi
    sleep 1
done

# Test connection
echo "🔍 Testing database connection..."
docker-compose exec -T postgres psql -U scrapy -d scrapy_db -c "SELECT version();" > /dev/null

echo ""
echo "✅ PostgreSQL setup complete!"
echo ""
echo "Database connection details:"
echo "  Host: localhost"
echo "  Port: 5433 (mapped from container's 5432)"
echo "  Database: scrapy_db"
echo "  User: scrapy"
echo "  Password: (from .env file)"
echo ""
echo "To run spiders:"
echo "  scrapy crawl hackernews"
echo "  scrapy crawl quotes"
echo "  scrapy crawl books"
echo ""
