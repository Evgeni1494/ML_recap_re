# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapingItem(scrapy.Item):
    titre = scrapy.Field()
    date_de_sortie = scrapy.Field()
    genres = scrapy.Field()
    directeur = scrapy.Field()
    acteurs = scrapy.Field()
    synopsis = scrapy.Field()
    note_presse = scrapy.Field()
    note_spectateurs = scrapy.Field()
    nationalite = scrapy.Field()
    budget = scrapy.Field()
    box_office_france = scrapy.Field()
    prix_et_nominations = scrapy.Field()
    
