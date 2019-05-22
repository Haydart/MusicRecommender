from scrapy import Item, Field


class EveryNoiseGenreItem(Item):
    name = Field()
    link = Field()
    r = Field()
    g = Field()
    b = Field()
    canvas_x = Field()
    canvas_y = Field()
    font_size = Field()


class EveryNoiseArtistItem(Item):
    name = Field()
    genre = Field()
