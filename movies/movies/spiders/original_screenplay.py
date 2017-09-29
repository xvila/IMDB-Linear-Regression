import scrapy

class OriginalSpider(scrapy.Spider):
    name = 'scrape_orginal_screenplay'

    custom_settings = {
        # "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    } 
    start_urls = ['http://www.imdb.com/list/ls000048075/']

    def parse(self, response):
        # Extract the links to the individual movie
        static_movie_url = 'http://www.imdb.com'

        for href in response.xpath('//div[@class="info"]/b/a/@href').extract():
            href = static_movie_url + href
            yield scrapy.Request(
                url=href, callback=self.parse_movie,
                meta={'url':href})

    def parse_movie(self,response): 
        url = response.request.meta['url']
        try:
            name = response.xpath('//div[@class="title_wrapper"]/h1/text()').extract()[0].strip()
        except:
            name = None
        try:
            budget = response.xpath('//div[@class="txt-block"]/h4/text()[contains(.,"Budget")]/../../text()').extract()[1].strip()
        except:
            budget = None
        try:
            box_office = response.xpath('//div[@class="txt-block"]/h4/text()[contains(.,"Gross")]/../../text()').extract()[1].strip()
        except:
            box_office = None
        try:
            user_rating = response.xpath('//div[@class="ratingValue"]//span/text()').extract()[0]
        except:
            user_rating = None
        try:
            genre = response.xpath('//div[@itemprop="genre"]/a/text()').extract()

        except:
            genre = None
        try:
            year = response.xpath('//span[@id="titleYear"]/a/text()').extract()[0]
        except:
            year = None
        try:
            rating = response.xpath('//meta[@itemprop="contentRating"]/../text()').extract()[1].strip()
        except:
            rating = None
        try:
            runtime = response.xpath('//div[@class="txt-block"]/time/text()').extract()[0]
        except:
            runtime = None
        try:
            director = response.xpath('//span[@itemprop="director"]/a/span/text()').extract()[0]

        except:
            director = None
     
        yield{
        'url': url,
        'name': name,
        'budget': budget,
        'box_office': box_office,
        'user_rating': user_rating,
        'genre': genre,
        'year': year,
        'rating': rating,
        'runtime': runtime,
        'director': director
        }
