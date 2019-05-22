from urllib.parse import urlparse, urljoin
import plotly
import scrapy
from scrapy import Request
from ..items import EveryNoiseGenreItem, EveryNoiseArtistItem
import plotly.graph_objs as go
import numpy as np


class ExampleSpider(scrapy.Spider):
    name = 'everynoise'
    allowed_domains = ['everynoise.com']
    start_urls = ['http://everynoise.com/']
    genre_index = 0

    def parse(self, response):
        for index, container in enumerate(response.xpath('//div[@class="genre scanme"]'), 1):
            name = container.xpath('./text()').extract()[0]
            link = container.xpath('./a[@class="navlink"]/@href').extract()[0]

            style_string = container.xpath('./@style').extract()[0]
            canvas_x = style_string.split('left: ')[-1].split('px;')[0]
            canvas_y = style_string.split('top: ')[-1].split('px;')[0]

            font_size = style_string.split('font-size: ')[-1].split('%')[0]

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

            yield Request(url=urljoin(response.url, str(link)),
                          callback=self.parse_genre_site,
                          meta={"item": item, "index": index})

            yield item
        # self.plot_3d_color_scatter(items)

    def parse_genre_site(self, response):
        genre_name = response.meta["item"]["name"]
        self.genre_index += 1
        print(f'Processing genre {self.genre_index} - {genre_name}')

        for index, container in enumerate(response.xpath('//div[@class="genre scanme"]'), 1):
            name = container.xpath('./text()').extract()[0]

            item = EveryNoiseArtistItem()
            item['name'] = name
            item['genre'] = genre_name

            yield item

    def extract_rgb(self, hex_color):
        stripped = hex_color.lstrip('#')
        return tuple(int(stripped[i:i + 2], 16) for i in (0, 2, 4))

    def plot_3d_color_scatter(self, items):
        names = [item['name'] for item in items]
        x = [item['r'] for item in items]
        y = [item['g'] for item in items]
        z = [item['b'] for item in items]

        trace2 = go.Scatter3d(
            x=x,
            y=y,
            z=z,
            text=names,
            mode='markers',
            marker=dict(
                color=[f'rgb({item["r"]}, {item["g"]}, {item["b"]})' for item in items],
                size=5,
                symbol='circle',
                line=dict(
                    color='rgb(200, 200, 200)',
                    width=1
                ),
                opacity=0.9
            )
        )
        data = [trace2]
        layout = go.Layout(
            title='Planets!',
            scene=dict(xaxis=dict(title='Red',
                                  titlefont=dict(color='Black')),
                       yaxis=dict(title='Green',
                                  titlefont=dict(color='Black')),
                       zaxis=dict(title='Blue',
                                  titlefont=dict(color='Black')),
                       bgcolor='rgb(255, 255, 255)'
                       ),
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0
            )
        )
        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, auto_open=True)
