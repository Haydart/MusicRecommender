from scrapy.exporters import CsvItemExporter
from .items import EveryNoiseGenreItem, EveryNoiseArtistItem


class EveryNoisePipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, EveryNoiseGenreItem):
            return self.handle_genre_item(item, spider)
        if isinstance(item, EveryNoiseArtistItem):
            return self.handle_artist_item(item, spider)

    def handle_genre_item(self, item, spider):
        print("HANDLING GENRE ITEM")
        return item

    def handle_artist_item(self, item, spider):
        print("ARTIST")
        return item
