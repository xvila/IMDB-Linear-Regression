import scrapy

class MovieSpider(scrapy.Spider):
    name = 'imbd'

    custom_settings = {
        #"DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    } 
    start_urls = []
    
    for i in range(1970,2016):
        #base = 'http://www.imdb.com/search/title?release_date={}'
        base = 'http://www.imdb.com/search/title?year={},{}&title_type=feature&sort=moviemeter,asc'
        url = base.format(i,i)
        start_urls.append(url)

    def parse(self, response):
        # Extract the links to the individual movie
        static_movie_url = 'http://www.imdb.com'
        static_list_url = 'http://www.imdb.com/search/title'

        for href in response.xpath('//h3/a/@href').extract():
            href = static_movie_url + href
            yield scrapy.Request(
                url=href, callback=self.parse_movie,
                meta={'url':href})
        
        # Follow pagination links and repeat
        next_url = response.xpath(
            '//div[@class="desc"]/a/@href'
        )[1].extract()
        next_url = static_list_url + next_url
        yield scrapy.Request(url=next_url,callback=self.parse)

    def parse_movie(self,response): 
        url = response.request.meta['url']
        name1 = response.xpath('//div[@class="title_wrapper"]/h1/text()').extract()
        budget = response.xpath('//div[@class="txt-block"]/h4/text()[contains(.,"Budget")]/../../text()').extract()
        box_office = response.xpath('//div[@class="txt-block"]/h4/text()[contains(.,"Gross")]/../../text()').extract()
        user_rating1 = response.xpath('//div[@class="ratingValue"]//span/text()').extract()
        genre = response.xpath('//div[@itemprop="genre"]/a/text()').extract()
        year1 = response.xpath('//span[@id="titleYear"]/a/text()').extract()
        # remove the index array for the xpath extracts and add if conditions.
        # bl1 = response.xpath('//*[@id="bling"]/li/a/text()')
        # if bl1:
        #     bling1 = bl1.extract()[0]
        # else:
        #     bling1 = 'None'

        if year1:
            year = year1[0] 
        else:
            year = None
        if user_rating1:
            user_rating = user_rating1[0]
        else:
            user_rating = None
        if name1:
            name = name1[0]
        else:
            name = None


        yield{
        'url': url,
        'name': name,
        'budget': budget,
        'box_office': box_office,
        'user_rating': user_rating,
        'genre': genre,
        'year': year
        }
