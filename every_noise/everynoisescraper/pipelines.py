from scrapy.exporters import CsvItemExporter
from .items import EveryNoiseGenreItem, EveryNoiseArtistItem


class EveryNoisePipeline(object):

    def __init__(self):
        self.genre_exporter = None
        self.artist_exporter = None

    def open_spider(self, spider):
        self.genre_exporter = CsvItemExporter(file=open('genres_output.csv', 'wb'))
        self.artist_exporter = CsvItemExporter(file=open('artists_output.csv', 'wb'))

    def close_spider(self, spider):
        self.genre_exporter.finish_exporting()
        self.artist_exporter.finish_exporting()
        self.genre_exporter.file.close()
        self.artist_exporter.file.close()

    def process_item(self, item, spider):
        if isinstance(item, EveryNoiseGenreItem):
            return self.export_genre_item(item, spider)
        if isinstance(item, EveryNoiseArtistItem):
            return self.export_artist_item(item, spider)

    def export_genre_item(self, item, spider):
        self.genre_exporter.export_item(item)
        return item

    def export_artist_item(self, item, spider):
        self.artist_exporter.export_item(item)
        return item
