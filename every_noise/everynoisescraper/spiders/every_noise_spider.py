from urllib.parse import urlparse, urljoin

import scrapy
from scrapy import Request

from ..items import EveryNoiseGenreLink


class ExampleSpider(scrapy.Spider):
    name = 'everynoise'
    allowed_domains = ['everynoise.com']
    start_urls = ['http://everynoise.com/']

    def parse(self, response):
        targets = response.xpath('//div[@class="genre scanme"]').extract()
        links = response.xpath('//div[@class="genre scanme"]/a/@href').extract()

        for target, link in zip(targets, links):
            print(target)
            item = EveryNoiseGenreLink()
            item["genre_name"] = target
            item["genre_link"] = link

            yield Request(url=urljoin(response.url, str(link)),
                          callback=self.parse_genre_site,
                          meta={"item": item})

    def parse_genre_site(self, response):
        x = response.meta["item"]
        print(x)
