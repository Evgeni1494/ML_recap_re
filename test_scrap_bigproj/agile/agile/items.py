# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy




class Top(scrapy.Item):
    title = scrapy.Field()
    nbre_entrees = scrapy.Field()
    
class AgileItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
