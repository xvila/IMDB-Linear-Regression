import scrapy

class NovelSpider(scrapy.Spider):
    name = 'scrape_books'

    custom_settings = {
        # "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    } 
    start_urls = ['https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(0%E2%80%939_and_A%E2%80%93C)',
       'https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(D%E2%80%93J)',
       'https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(K%E2%80%93R)',
       'https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(S%E2%80%93Z)']

    def parse(self, response):
        # Extract the links to the individual movie
        static_movie_url = 'https://en.wikipedia.org'

        for href in response.xpath('//table[@class="wikitable"]/tr/td/i/a/@href').extract():
            href = static_movie_url + href
            yield {
            'url':href
            }

    