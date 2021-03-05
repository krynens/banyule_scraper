# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import scrapy
import datetime
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags


def Melbourne_href(value):
    return 'https://www.melbourne.vic.gov.au' + value


class MorphioScraperItem(scrapy.Item):
    council_reference = scrapy.Field(input_processor=MapCompose(
        remove_tags, strip), output_processor=TakeFirst())
    date_lodged = scrapy.Field(input_processor=MapCompose(
        remove_tags, strip), output_processor=TakeFirst())
    address = scrapy.Field(input_processor=MapCompose(
        remove_tags, strip), output_processor=TakeFirst())
    description = scrapy.Field(input_processor=MapCompose(
        remove_tags, strip), output_processor=TakeFirst())
    info_url = scrapy.Field(input_processor=MapCompose(
        remove_tags, strip, Melbourne_href), output_processor=TakeFirst())
