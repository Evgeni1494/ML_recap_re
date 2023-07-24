# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MongodbCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

import scrapy


class FilmItem(scrapy.Item):
    title = scrapy.Field()
    nbre_entrees = scrapy.Field()
  