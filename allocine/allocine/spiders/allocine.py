import scrapy, ast, csv, random
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime
from ..items import AlloCineItem
from ..utils import strip_texte, extraire_prix_et_nominations, enlever_espace_pays, extraire_entrees

class AlloCineSpider(CrawlSpider):
    name = "allocine"
    allowed_domains = ["allocine.fr"]
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    csvfile=None
    def start_requests(self):
        """
        Commence le scraping d'Allocine en se basant sur son dictionnaire
        Pour chacune des trois décénnie, parcoure toutes ses pages par bloc de 500
        Tout en monitorant 2 csv, un par page et un par bloc
        """

        nombres_de_pages_par_decennies = {
            2020: 804,
            2010: 1748,
            2000: 1530
        }
        for decennie, nombre_de_pages in nombres_de_pages_par_decennies.items():
            for i in range(0,nombre_de_pages):
                    url = f"https://www.allocine.fr/films/decennie-{decennie}/?page={i}"
                    yield scrapy.Request(url, callback=self.parse_start, headers={'User-Agent': self.user_agent})

                
                
    def parse_start(self, response):
        for link in response.css("h2.meta-title .meta-title-link::attr(href)").getall():
            yield response.follow(link, self.parse_movie_details, headers={'User-Agent': self.user_agent})

    def parse_movie_details(self, response):
        items = AlloCineItem()
        try:
            titre = response.css('.titlebar-title-lg::text').get()
            if response.css('div.meta-body-item>span.light::text')[-1].get().strip() == 'Titre original':
                titre_original = response.css('div.meta-body-item::text')[-1].get()
            else:
                titre_original = ''
            duree = response.css('div.meta-body-item.meta-body-info::text')[3].get().strip()
            date_de_sortie = response.css('div.meta-body-item.meta-body-info span.blue-link::text').get()
            genres = response.css('div.meta-body-item.meta-body-info>span::text')[3:].getall()
            directeur = response.css('div.meta-body-item.meta-body-direction span.blue-link::text').get()
            acteurs = response.css('.meta-body-actor.meta-body-item>span::text')[1:].getall()
            synopsis = response.css('div.content-txt::text').get() #\n #\n
            note_presse = response.css('div.rating-item:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)::text').get()
            note_spectateurs = response.css('div.rating-item:nth-child(2) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)::text').get()
            nationalite = response.css('span.that>.nationality::text').getall() #' '
            box_office_france = response.css('div.item>span.that:contains("entrées")::text').get()
            prix_et_nominations = response.css('section.section.ovw.ovw-technical>div.item>.that.blue-link::text')[1].get()
            

            ####
            prix_et_nominations_extraits = extraire_prix_et_nominations(prix_et_nominations)
            
            items['titre'] = titre
            items['titre_original'] = titre_original.strip()
            items['duree'] = duree
            items['date_de_sortie'] = strip_texte(date_de_sortie)
            items['genres'] = genres
            items['directeur'] = directeur
            items['acteurs'] = acteurs
            items['synopsis'] = strip_texte(synopsis)
            items['note_presse'] = note_presse
            items['note_spectateurs'] = note_spectateurs
            items['nationalite'] = nationalite
            items['box_office_france'] = extraire_entrees(box_office_france)
            items['prix'] = prix_et_nominations_extraits[0]
            items['nominations'] = prix_et_nominations_extraits[1]
            
            yield items

        except Exception as e:
            self.logger.error(f"Error occurred: {e}")
            
    def closed(self, reason):
        if self.csvfile:
            self.csvfile.close()