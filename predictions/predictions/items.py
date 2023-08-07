# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PredictionsItem(scrapy.Item):
    titre = scrapy.Field()
    titre_original = scrapy.Field()
    duree = scrapy.Field()
    date_de_sortie = scrapy.Field()
    genres = scrapy.Field()
    directeur = scrapy.Field()
    acteurs = scrapy.Field()
    nationalite = scrapy.Field()
