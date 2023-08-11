# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ReellesItem(scrapy.Item):
    titre = scrapy.Field()
    date_de_sortie = scrapy.Field()
    entrees_premiere_semaine = scrapy.Field()