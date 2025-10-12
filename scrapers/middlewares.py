import logging
import random
from scrapy import signals
from scrapy.exceptions import NotConfigured

logger = logging.getLogger(__name__)

class ScraperStatsMiddleware:
    """Middleware to track scraping statistics"""
    
    def __init__(self, stats):
        self.stats = stats
        
    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('STATS_ENABLED', True):
            raise NotConfigured
        
        middleware = cls(crawler.stats)
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(middleware.item_scraped, signal=signals.item_scraped)
        
        return middleware
    
    def spider_opened(self, spider):
        logger.info(f"🕷️  Spider opened: {spider.name}")
        
    def spider_closed(self, spider, reason):
        stats = self.stats.get_stats()
        logger.info(f"✅ Spider closed: {spider.name}")
        logger.info(f"   Reason: {reason}")
        logger.info(f"   Items scraped: {stats.get('item_scraped_count', 0)}")
        logger.info(f"   Pages crawled: {stats.get('response_received_count', 0)}")
        logger.info(f"   Errors: {stats.get('log_count/ERROR', 0)}")
        
    def item_scraped(self, item, spider):
        pass  # Could add per-item logging if needed

class ErrorLoggingMiddleware:
    """Middleware to log detailed error information"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_error, signal=signals.spider_error)
        return middleware
    
    def spider_error(self, failure, response, spider):
        self.logger.error(
            f"❌ Error in {spider.name}: {failure.getErrorMessage()} "
            f"on {response.url}"
        )
