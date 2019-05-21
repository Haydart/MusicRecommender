import scrapy


class EveryNoiseGenreLink(scrapy.Item):
    genre_name = scrapy.Field()
    genre_link = scrapy.Field()