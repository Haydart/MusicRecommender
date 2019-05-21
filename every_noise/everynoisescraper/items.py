import scrapy


class EveryNoiseGenreItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    r = scrapy.Field()
    g = scrapy.Field()
    b = scrapy.Field()
    canvas_x = scrapy.Field()
    canvas_y = scrapy.Field()
    font_size = scrapy.Field()
