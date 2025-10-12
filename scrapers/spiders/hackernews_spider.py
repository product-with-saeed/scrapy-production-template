import scrapy
from datetime import datetime

class HackerNewsSpider(scrapy.Spider):
    name = 'hackernews'
    allowed_domains = ['news.ycombinator.com']
    start_urls = ['https://news.ycombinator.com/']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'ROBOTSTXT_OBEY': True,
    }
    
    def parse(self, response):
        for row in response.css('tr.athing'):
            item = {
                'title': row.css('span.titleline > a::text').get(),
                'url': row.css('span.titleline > a::attr(href)').get(),
                'rank': row.css('span.rank::text').get(),
                'item_id': row.attrib.get('id'),
            }
            
            # Get metadata from next row
            next_row = row.xpath('./following-sibling::tr[1]')
            item['score'] = next_row.css('span.score::text').get()
            item['author'] = next_row.css('a.hnuser::text').get()
            item['comments'] = next_row.css('a:contains("comment")::text').get()
            item['scraped_at'] = datetime.now().isoformat()
            
            yield item
