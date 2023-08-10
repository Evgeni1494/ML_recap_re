from datetime import datetime, timedelta
from scrapy.spiders import CrawlSpider
import csv, os, scrapy
from ..items import ReellesItem

class ReellesSpider(CrawlSpider):
    name = "reelles"
    allowed_domains = ["jpbox-office.com"]
    
    def start_requests(self):
        id_semaine_reference = 2767
        date_semaine_reference = datetime(2023, 1, 4)
        date_actuelle = datetime.now()
        jour_de_semaine_actuel = date_actuelle.weekday()
        jours_jusqua_mercredi = (jour_de_semaine_actuel -2) % 7
        dernier_mercredi = date_actuelle - timedelta(days=jours_jusqua_mercredi)
        ecart_semaines = (dernier_mercredi - date_semaine_reference).days // 7
        id_semaine_precedente = id_semaine_reference + ecart_semaines -1

        url = f"https://www.jpbox-office.com/v9_tophebdo.php?idsem={id_semaine_precedente}&view=2"
        yield scrapy.Request(url, callback=self.parse_start)
        
        
    def parse_start(self, response):
        for link in response.css('h3>::attr(href)').getall():
            yield response.follow(link, self.parse_movie_details)
    
    
    def parse_movie_details(self, response):
        items = ReellesItem()
        ### sur la page du film
        titre = response.css('h1::text').get()
        date_de_sortie = response.css('p>::text').get().strip()
        entrees_premiere_semaine = response.xpath('//table[@class="tablesmall tablesmall2"]//tr//td[@class="col_poster_contenu_majeur"]/text()').getall()[-1]
        
        items['titre'] = titre.strip()
        items['date_de_sortie'] = date_de_sortie.strip()
        items['entrees_premiere_semaine'] = entrees_premiere_semaine
        
        yield items