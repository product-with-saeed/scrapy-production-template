import scrapy
from datetime import datetime

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'ROBOTSTXT_OBEY': True,
    }
    
    def parse(self, response):
        for book in response.css('article.product_pod'):
            # Extract rating
            rating_class = book.css('p.star-rating::attr(class)').get()
            rating = rating_class.split()[-1] if rating_class else None
            
            # Extract availability
            availability_text = book.css('p.availability::text').getall()
            availability = ''.join(availability_text).strip() if availability_text else None
            
            yield {
                'title': book.css('h3 a::attr(title)').get(),
                'price': book.css('p.price_color::text').get(),
                'availability': availability,
                'rating': rating,
                'url': response.urljoin(book.css('h3 a::attr(href)').get()),
                'scraped_at': datetime.now().isoformat()
            }
        
        # Follow pagination
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)