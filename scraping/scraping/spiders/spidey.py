import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import csv
from ..items import ScrapingItem
import random

class SpideySpider(CrawlSpider):
    name = "spidey"
    allowed_domains = ["allocine.fr"]
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    
    def start_requests(self):
        for i in range(0, 3):
            url = f"https://www.allocine.fr/films/?page={i}"
            yield scrapy.Request(url, callback=self.parse_start, headers={'User-Agent': self.user_agent})
    
    def parse_start(self, response):
        for link in response.css("h2.meta-title .meta-title-link::attr(href)").getall():
            yield response.follow(link, self.parse_movie_details, headers={'User-Agent': self.user_agent})

    def parse_movie_details(self, response):
        items = ScrapingItem()
        try:
            titre = response.css('.titlebar-title-lg::text').get()
            date_de_sortie = response.css('div.meta-body-item.meta-body-info span.blue-link::text').get() #\n \n
            genres = response.css('div.meta-body-item.meta-body-info>span::text')[3:].getall()
            directeur = response.css('div.meta-body-item.meta-body-direction span.blue-link::text').get()
            acteurs = response.css('.meta-body-actor.meta-body-item>span::text')[1:].getall()
            synopsis = response.css('div.content-txt::text').get() #\n #\n
            note_presse = response.css('div.rating-item:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)::text').get()
            note_spectateurs = response.css('div.rating-item:nth-child(2) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)::text').get()
            nationalite = response.css('span.that>.nationality::text').getall() #' '
            budget = response.css('div.item>span.that:contains("$")::text').get()
            box_office_france = response.css('div.item>span.that:contains("entrées")::text').get()
            prix_et_nominations = response.css('section.section.ovw.ovw-technical>div.item>.that.blue-link::text')[1].get()#['\n6 prix et 22 nominations\n']
            
            items['titre'] = titre
            items['date_de_sortie'] = date_de_sortie
            items['genres'] = genres
            items['directeur'] = directeur
            items['acteurs'] = acteurs
            items['synopsis'] = synopsis
            items['note_presse'] = note_presse
            items['note_spectateurs'] = note_spectateurs
            items['nationalite'] = nationalite
            items['budget'] = budget
            items['box_office_france'] = box_office_france
            items['prix_et_nominations'] = prix_et_nominations
            
            yield items

        except Exception as e:
            self.logger.error(f"Error occurred: {e}")
            
# class SpideySpider(scrapy.Spider):
#     name = "spidey"
#     allowed_domains = ["allocine.fr"]
#     start_urls = ["http://allocine.fr/films/"]

#     def __init__(self):
#         self.page_count = 0

#     def start_requests(self, response):
#         # Récupérer les liens des films sur la page actuelle
#         film_links = response.css('.meta-title-link::attr(href)').getall()
#         for film_link in film_links:
#             # Suivre chaque lien vers la page du film et appeler la méthode de rappel `parse_film`
#             yield scrapy.Request(response.urljoin(film_link), callback=self.parse_film)

#         # Si vous souhaitez passer à la page suivante, vous pouvez trouver le lien "suivant" et envoyer une requête dessus.
#         next_page = response.css('a.xXx.button.button-md.button-primary-full.button-right::attr(href)').get()
#         # if next_page: ##### TOUT SCRAPPER
#         #     yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
#         if next_page and self.page_count < 3:
#             self.page_count += 1 ################# SCRAPPER 3 PAGES
#             delay = random.uniform(1, 3)  # Délai aléatoire entre 1 et 3 secondes
#             yield scrapy.Request(response.urljoin(next_page), callback=self.parse_film, dont_filter=True, meta={'dont_redirect': True}, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3", 'Connection': 'close'}, dont_cache=True, errback=self.errback_httpbin)


#     def parse_film(self, response):
#         try:
#             titre = response.css('.titlebar-title-lg::text').get()
#             date_de_sortie = response.css('div.meta-body-item.meta-body-info span.blue-link::text').getall() #\n \n
#             genres = response.css('div.meta-body-item.meta-body-info>span::text')[3:].getall()
#             directeur = response.css('div.meta-body-item.meta-body-direction span.blue-link::text').get()
#             acteurs = response.css('.meta-body-actor.meta-body-item>span::text')[1:].getall()
#             synopsis = response.css('div.content-txt::text').get() #\n #\n
#             note_presse = response.css('div.rating-item:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)::text').get()
#             note_spectateurs = response.css('div.rating-item:nth-child(2) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)::text').get()
#             nationalite = response.css('span.that>.nationality::text').getall().strip() #' '
#             budget = response.css('div.item>span.that:contains("$")::text').get()
#             box_office_france = response.css('div.item>span.that:contains("entrées")::text').get()
#             prix_et_nominations = response.css('section.section.ovw.ovw-technical>div.item>.that.blue-link::text')[1].getall()#['\n6 prix et 22 nominations\n']
#             yield {
#                 'titre': titre,
#                 'date_de_sortie': date_de_sortie,
#                 'genres': genres,
#                 'directeur': directeur,
#                 'acteurs': acteurs,
#                 'synopsis': synopsis,
#                 'note_presse': note_presse,
#                 'note_spectateurs': note_spectateurs,
#                 'nationalite': nationalite,
#                 'budget': budget,
#                 'box_office_france': box_office_france,
#                 'prix': prix_et_nominations.split('prix')[0],
#                 'nominations' : prix_et_nominations.split('prix')[1]
#             }
#         except Exception as e:
#             self.logger.error(f"Error occurred: {e}")
            

#     def errback_httpbin(self, failure):
#         # En cas d'erreur, vous pouvez gérer le retour en arrière et l'affichage des messages d'erreur.
#         self.logger.error(repr(failure))