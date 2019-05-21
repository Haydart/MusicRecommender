from urllib.parse import urlparse, urljoin
import scrapy
from scrapy import Request
from ..items import EveryNoiseGenreItem


class ExampleSpider(scrapy.Spider):
    name = 'everynoise'
    allowed_domains = ['everynoise.com']
    start_urls = ['http://everynoise.com/']

    def parse(self, response):
        for container in response.xpath('//div[@class="genre scanme"]'):
            name = container.xpath('./text()').extract()[0]
            link = container.xpath('./a[@class="navlink"]/@href').extract()[0]

            style_string = container.xpath('./@style').extract()[0]
            canvas_x = style_string.split('left: ')[-1].split('px;')[0]
            canvas_y = style_string.split('top: ')[-1].split('px;')[0]

            font_size = canvas_y = style_string.split('font-size: ')[-1].split('%')[0]

            color_string = style_string.split('color: #')[-1].split('px;')[0]
            color_tuple = self.extract_rgb(color_string)

            item = EveryNoiseGenreItem()
            item['name'] = name
            item['link'] = link
            item['r'] = color_tuple[0]
            item['g'] = color_tuple[1]
            item['b'] = color_tuple[2]
            item['canvas_x'] = canvas_x
            item['canvas_y'] = canvas_y
            item['font_size'] = font_size

            print(item)

            # yield Request(url=urljoin(response.url, str(link)),
            #               callback=self.parse_genre_site,
            #               meta={"item": item})

    def parse_genre_site(self, response):
        x = response.meta['item']
        print(x)

    def extract_rgb(self, hex_color):
        stripped = hex_color.lstrip('#')
        return tuple(int(stripped[i:i + 2], 16) for i in (0, 2, 4))
