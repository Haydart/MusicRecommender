from urllib.parse import urlparse, urljoin
import plotly
import scrapy
from scrapy import Request
from ..items import EveryNoiseGenreItem
import plotly.graph_objs as go
import numpy as np


class ExampleSpider(scrapy.Spider):
    name = 'everynoise'
    allowed_domains = ['everynoise.com']
    start_urls = ['http://everynoise.com/']

    def parse(self, response):
        items = []

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

            items.append(item)
        print(items)
        self.plot_3d_color_scatter(items)

            # yield Request(url=urljoin(response.url, str(link)),
            #               callback=self.parse_genre_site,
            #               meta={"item": item})

    def parse_genre_site(self, response):
        x = response.meta['item']
        print(x)

    def extract_rgb(self, hex_color):
        stripped = hex_color.lstrip('#')
        return tuple(int(stripped[i:i + 2], 16) for i in (0, 2, 4))

    def plot_3d_color_scatter(self, items_colors):
        x, y, z = np.random.multivariate_normal(np.array([0, 0, 0]), np.eye(3), 200).transpose()
        trace1 = go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode='markers',
            marker=dict(
                size=12,
                line=dict(
                    color='rgba(217, 217, 217, 0.14)',
                    width=0.5
                ),
                opacity=0.8
            )
        )

        x2, y2, z2 = np.random.multivariate_normal(np.array([0, 0, 0]), np.eye(3), 200).transpose()
        trace2 = go.Scatter3d(
            x=x2,
            y=y2,
            z=z2,
            mode='markers',
            marker=dict(
                color='rgb(127, 127, 127)',
                size=12,
                symbol='circle',
                line=dict(
                    color='rgb(204, 204, 204)',
                    width=1
                ),
                opacity=0.9
            )
        )
        data = [trace1, trace2]
        layout = go.Layout(
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0
            )
        )
        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, auto_open=True)

        # py.plotly.offline.plot(*yourplotname *, filename='3D color scatter.html')
