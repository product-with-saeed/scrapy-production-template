# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import psycopg2
from datetime import datetime
import logging

class PostgresPipeline:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None
        self.cursor = None
        self.logger = logging.getLogger(__name__)
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_config={
                'host': crawler.settings.get('POSTGRES_HOST', 'postgres'),
                'database': crawler.settings.get('POSTGRES_DB', 'scrapy_db'),
                'user': crawler.settings.get('POSTGRES_USER', 'scrapy'),
                'password': crawler.settings.get('POSTGRES_PASSWORD', 'scrapy'),
                'port': crawler.settings.get('POSTGRES_PORT', 5432)
            }
        )
    
    def open_spider(self, spider):
        try:
            self.connection = psycopg2.connect(**self.db_config)
            self.cursor = self.connection.cursor()
            self.create_tables(spider.name)
            self.logger.info(f"Connected to PostgreSQL for spider: {spider.name}")
        except Exception as e:
            self.logger.error(f"Failed to connect to PostgreSQL: {e}")
            raise
    
    def close_spider(self, spider):
        if self.connection:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            self.logger.info(f"PostgreSQL connection closed for spider: {spider.name}")
    
    def create_tables(self, spider_name):
        tables = {
            'hackernews': '''
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
            ''',
            'quotes': '''
                CREATE TABLE IF NOT EXISTS quotes (
                    id SERIAL PRIMARY KEY,
                    text TEXT,
                    author TEXT,
                    tags TEXT[],
                    scraped_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'books': '''
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
            '''
        }
        
        if spider_name in tables:
            self.cursor.execute(tables[spider_name])
            self.connection.commit()
            self.logger.info(f"Table '{spider_name}' created/verified")
    
    def process_item(self, item, spider):
        try:
            if spider.name == 'hackernews':
                self.cursor.execute('''
                    INSERT INTO hackernews (title, url, rank, score, author, comments, item_id, scraped_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (item_id) DO NOTHING
                ''', (
                    item.get('title'), item.get('url'), item.get('rank'),
                    item.get('score'), item.get('author'), item.get('comments'),
                    item.get('item_id'), item.get('scraped_at')
                ))
            
            elif spider.name == 'quotes':
                self.cursor.execute('''
                    INSERT INTO quotes (text, author, tags, scraped_at)
                    VALUES (%s, %s, %s, %s)
                ''', (
                    item.get('text'), item.get('author'),
                    item.get('tags'), item.get('scraped_at')
                ))
            
            elif spider.name == 'books':
                self.cursor.execute('''
                    INSERT INTO books (title, price, availability, rating, url, scraped_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (url) DO NOTHING
                ''', (
                    item.get('title'), item.get('price'), item.get('availability'),
                    item.get('rating'), item.get('url'), item.get('scraped_at')
                ))
            
            self.connection.commit()
            
        except Exception as e:
            self.logger.error(f"Error processing item: {e}")
            self.connection.rollback()
        
        return item
