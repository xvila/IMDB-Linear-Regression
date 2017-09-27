import scrapy

class MovieSpider(scrapy.Spider):
    name = 'imbd_scrape'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = [
        'http://www.imdb.com/year/2015',
        'http://www.imdb.com/year/2016'
    ]

    def parse(self, response):
        # Extract the links to the individual festival pages


        # Follow pagination links and repeat