import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# from fonctions import convert_to_minutes
from mongodb_crawler.items import FilmItem
import re
class TopfilmsspiderSpider(CrawlSpider):
    custom_settings = {
        'ITEM_PIPELINES': {
            'mongodb_crawler.pipelines.TopFilmsPipeline': 400
        }
    }
    name = 'crawlerfilms'
    allowed_domains = ['jpbox-office.com']
    #Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
    # user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'
    
    # def start_requests(self):
    #     yield scrapy.Request(url='https://www.jpbox-office.com/v9_demarrage.php?view=2', headers={
    #         'User-Agent': self.user_agent
    #     })

    # rules = (
    #     Rule(LinkExtractor(), callback='parse_item'),
    # )
    def start_requests(self):
        for i in range(0, 6000, 30):  
            yield scrapy.Request(url='https://www.jpbox-office.com/v9_demarrage.php?view=1&filtre=classg&limite={}&infla=0&variable=0&tri=champ0&order=DESC&limit5=0'.format(i),
                                headers={'User-Agent': self.user_agent},
                                callback=self.parse_item)

    # def parse_item(self, response):
    #     film_items = response.css('td.col_poster_titre h3 a')
    #     nbre_entrees = response.css('td.col_poster_contenu_majeur::text').getall()

    #     for i, item in enumerate(film_items):
    #         film_item = {}
    #         film_item['title'] = item.css('::text').get()
    #         film_item['nbre_entrees'] = nbre_entrees[i] if i < len(nbre_entrees) else None
    #         yiel44.2d film_item
    # dico = {1971: 1.65, 1974: 1.89, 1975: 2.03, 1976: 2.13, 1977: 2.23, 1978: 2.34, 1979: 2.47, 1980: 2.69, 1981: 2.78, 1982: 2.94, 1983: 3.15, 1984: 3.36, 1985: 3.55, 1986: 3.71, 1987: 3.91, 1988: 4.11, 1989: 3.99, 1990: 4.22, 1991: 4.21, 1992: 4.15, 1993: 4.14, 1994: 4.08, 1995: 4.35, 1996: 4.42, 1997: 4.59, 1998: 4.69, 1999: 5.06, 2000: 5.39, 2001: 5.65, 2002: 5.80, 2003: 6.03, 2004: 6.21, 2005: 6.41, 2006: 6.55, 2007: 6.88, 2008: 7.18, 2009: 7.50, 2010: 7.89, 2011: 7.93, 2012: 7.96, 2013: 8.13, 2014: 8.17, 2015: 8.43, 2016: 8.65, 2017: 8.97, 2018: 9.16, 2019: 9.16, 2020: 9.18, 2021: 10.17, 2022: 10.53, 2023: 10.7}
    
    # def parse_item(self, response):
    #     titles = response.css('h3 a::text').getall()
    #     # entries = response.css('td.col_poster_contenu_majeur::text').getall()
    #     year=response.css('td.col_poster_contenu a::text').getall()
    #     for i in range(30):
    #         film_item = {}
    #         film_item['title'] = titles[i]
    #         film_item['nbre_entrees'] = entries[i*4] if i*4 < len(entries) else None
    #         yield film_item
            
    def parse_item(self, response):
        titles = response.css('td.col_poster_titre h3 a::text').getall()
        entries = response.css('td.col_poster_contenu_majeur::text').getall()
        years = response.css('td.col_poster_contenu a::text').getall()[5:]
       
        years1 = []

        for year in years:
            if any(char.isdigit() for char in year):
                years1.append(year)
          # Example dictionary, modify as needed
        nbre_entree=[]
        dico = {1971: 1.65, 1974: 1.89, 1975: 2.03, 1976: 2.13, 1977: 2.23, 1978: 2.34, 1979: 2.47, 1980: 2.69, 1981: 2.78, 1982: 2.94, 1983: 3.15, 1984: 3.36, 1985: 3.55, 1986: 3.71, 1987: 3.91, 1988: 4.11, 1989: 3.99, 1990: 4.22, 1991: 4.21, 1992: 4.15, 1993: 4.14, 1994: 4.08, 1995: 4.35, 1996: 4.42, 1997: 4.59, 1998: 4.69, 1999: 5.06, 2000: 5.39, 2001: 5.65, 2002: 5.80, 2003: 6.03, 2004: 6.21, 2005: 6.41, 2006: 6.55, 2007: 6.88, 2008: 7.18, 2009: 7.50, 2010: 7.89, 2011: 7.93, 2012: 7.96, 2013: 8.13, 2014: 8.17, 2015: 8.43, 2016: 8.65, 2017: 8.97, 2018: 9.16, 2019: 9.16, 2020: 9.18, 2021: 10.17, 2022: 10.53, 2023: 10.7}
        # print(entries)
        # print(years1)
        print(len(entries)/4)
        entre=[entries[i] for i in range (0,120,4)]
        print(entre)
        reel_nbre_entree=[]
        for entry, year in zip(entre, years1):
            entry_number = int(re.sub(r'\D', '', entry))  # Remove non-digit characters
            year_number = int(re.sub(r'\D', '', year))  # Remove non-digit characters
            print(entry_number)
            print(year_number)
            divisor = dico.get(year_number)
            reel_nbre=round(entry_number/divisor)
            reel_nbre_entree.append(reel_nbre)
        print(reel_nbre_entree)
            
        for i in range(30):
            film_item = {}
            film_item['title'] = titles[i]
            film_item['nbre_entrees']=reel_nbre_entree[i]
                    # film_item['nbre_entrees'] = nbre_entree[i]
            yield film_item       
        
    #     for i in range (0,6000,30):
    #         'https://www.jpbox-office.com/v9_demarrage.php?view=1&filtre=classg&limite={i}&infla=0&variable=0&tri=champ0&order=DESC&limit5=0'
            
    # #        /
    #     liens = response.css('a[href="/v9_top_semaines.php?limite=50&tri=weekend&order=DESC&variable=1&view=2"]::text').extract()
    #     if liens:
    #         dernier_lien = liens[-1]  # Sélectionner le dernier lien

    #         if not dernier_lien.strip():
    #             return  # Arrêter le scraping si le dernier lien est vide

    #         yield response.follow(dernier_lien, callback=self.parse_item)
        # entry_number_actu=[]
        # entry_number_actu=entry_number_actu.append(entry_number[0])   # je rajoute la 1ére donnée de la liste "entry_number"
        #mtnt je veux à partir du 5éme item puis 9 puis 13
        # entry_number.pop[0]
        # for i in range (len(entry_number)/4):
        #     entry_number_actu.append(entry_number[i*4])
        # print(entry_number_actu)
        # entry_number_actu.pop[0]
        # entry_number[i*4] if i*4 < len(nbre_entree) else None
        # if divisor is not None:
        #     nbre_entree.append( entry_number / divisor)
        # print (nbre_entree)
        # print(titles)
        # for i in range(30):
        #     film_item = {}
        #     film_item['title'] = titles[i]
        #     film_item['nbre_entrees']=nbre_entree[i*4] if i*4 < len(nbre_entree) else None
        #     # film_item['nbre_entrees'] = nbre_entree[i]
        #     yield film_item       
        
                # film_item = {
                #     'year': year_number,
                #     'nbre_entrees': int(divided_entry)
                # }
                # yield film_item