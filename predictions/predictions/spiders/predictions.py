from datetime import datetime, timedelta
from scrapy.spiders import CrawlSpider
from ..items import PredictionsItem
import csv, os, scrapy

class PredictionsSpider(CrawlSpider):
    name = "predictions"
    allowed_domains = ["allocine.fr"]
    
    def start_requests(self):
        
        date_actuelle = datetime.now()   
        jour_de_semaine_actuel = date_actuelle.weekday()
        jours_jusqua_mercredi = (2 - jour_de_semaine_actuel) % 7
        mercredi_suivant = date_actuelle + timedelta(days=jours_jusqua_mercredi)
        date_prochain_mercredi = mercredi_suivant.strftime("%d/%m/%Y") # Récupere la date du jour et se place au mercredi suivant
        
        jour = date_prochain_mercredi[0:2]
        mois = date_prochain_mercredi[3:5]
        annee = date_prochain_mercredi[6:10]
        
        url = f"https://www.allocine.fr/film/agenda/mois/mois-{annee}-{mois}/"
        yield scrapy.Request(url, callback=self.parse_start)
        
    def parse_start(self, response):
        for link in response.css('.month-movies-link::attr(href)').getall():
            yield response.follow(link, self.parse_movie_details)
           
    def parse_movie_details(self, response):
        items = PredictionsItem()
        
        titre = response.css('.titlebar-title-lg::text').get()
        if response.css('div.meta-body-item>span.light::text')[-1].get().strip() == 'Titre original':
            titre_original = response.css('div.meta-body-item::text')[-1].get()
        else:
            titre_original = ''
        duree = response.css('div.meta-body-item.meta-body-info::text')[3].get()
        date_de_sortie = response.css('div.meta-body-item.meta-body-info span.blue-link::text').get()
        genres = response.css('div.meta-body-item.meta-body-info>span::text')[3:].getall()
        directeur = response.css('div.meta-body-item.meta-body-direction span.blue-link::text').get()
        acteurs = response.css('.meta-body-actor.meta-body-item>span::text')[1:].getall()
        nationalite = response.css('span.that>.nationality::text').getall()

        items['titre'] = titre.strip()
        items['titre_original'] = titre_original.strip()
        items['duree'] = duree.strip()
        items['date_de_sortie'] = date_de_sortie.strip()
        items['genres'] = genres
        items['directeur'] = directeur
        items['acteurs'] = acteurs
        items['nationalite'] = nationalite
        yield items
        
           