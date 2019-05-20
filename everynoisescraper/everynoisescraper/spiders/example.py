import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'everynoise'
    allowed_domains = ['everynoise.com']
    start_urls = ['http://everynoise.com/']

    def parse(self, response):
        print('\n'.join(response.xpath('//div/a').extract()))
