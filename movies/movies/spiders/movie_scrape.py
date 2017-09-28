import scrapy

class MovieSpider(scrapy.Spider):
    name = 'imbd_scrape'
    static_movie_url = 'imdb.com'
    static_list_url = 'http://www.imdb.com/search/title'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
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
        # Extract the links to the individual festival pages
        for href in response.xpath('//h3/a/@href').extract():
            yield scrapy.Request(
                url=static_movie_url + href, callback=self.parse_movie,
                meta={'url':href})
        # Follow pagination links and repeat
        next_url = static_list_url + response.xpath(
            '//a[@class="next page-numbers"]/@href'
        ).extract()

        yield scrapy.Request(url=next_url,callback=self.parse)

    def parse_movie(self,response):
        url = response.request.meta['url']