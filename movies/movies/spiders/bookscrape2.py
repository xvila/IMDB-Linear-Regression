import scrapy

class BookSpider(scrapy.Spider):
    name = 'wiki_movies_books'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
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

        for href in response.xpath('//table[@class="wikitable"]/tr/td[1]/i/a/@href').extract():
            href = static_movie_url + href
            
            yield scrapy.Request(
                url=href, callback=self.parse_movie,
                meta={'url':href})
# pulls movie title
#response.xpath('//table[@class="wikitable"]/tr/td[2]/i/a/text()').extract()
    def parse_movie(self,response): 
        url = response.request.meta['url']
        try:
            author = response.xpath('//th[text()="Author"]/../td/a/text()').extract()[0]
        except:
            author = None
        try:
            book_name = response.xpath('//h1[@class="firstHeading"]/i/text()').extract()[0]
        except:
            book_name = None
        try:
            publication_date = response.xpath('//div[text()="Publication date"]/../../td/text()').extract()[0]
        except:
            publication_date = None
        try:
            isbn = response.xpath('//a[text()="ISBN"]/../../td/text()').extract()[0].strip()
        except:
            isbn = None
        try:
            genre = response.xpath('//th[text()="Genre"]/../td/a/text()').extract()
        except:
            genre = None
        
        yield{
        'url': url,
        'author': author,
        'book_name': book_name,
        'publication_date': publication_date,
        'isbn': isbn,
        'genre': genre
        }
