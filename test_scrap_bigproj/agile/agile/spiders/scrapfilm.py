import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# from fonctions import convert_to_minutes
from items import Top

class TopfilmsspiderSpider(CrawlSpider):
    custom_settings = {
        'ITEM_PIPELINES': {
            'top_films_series.pipelines.TopFilmsPipeline': 400
        }
    }
    name = 'crawler_films'
    allowed_domains = ['jpbox-office.com']
    #Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
    # user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'
    
    def start_requests(self):
        yield scrapy.Request(url='https://www.jpbox-office.com/v9_demarrage.php?view=2', headers={
            'User-Agent': self.user_agent
        })

    rules = (
    Rule(LinkExtractor(restrict_css='.titleColumn a'), callback='parse_item'),
    )
    
    def parse_item(self, response):
        item = {}
        
        item['titre'] = response.css('h3 a::text').extract()
        # item['realisateur'] = response.css(...)  # Remplacez (...) par le sélecteur pour le réalisateur
        item['nbre_entrees'] = response.css('td.col_poster_contenu_majeur::text').extract()

        # Vérifier si le dernier lien est vide
        liens = response.css('a[href^="/v9_demarrage.php"]').extract()
        if liens:
            dernier_lien = liens[-1]  # Sélectionner le dernier lien

            if not dernier_lien.strip():
                return  # Arrêter le scraping si le dernier lien est vide

            yield response.follow(dernier_lien, callback=self.parse_item)

        yield item
        next_page=response.css
    
    
    # #item['year'] = response.css('.ipc-inline-list__item a[href*="releaseinfo"]::text')[0].extract()
    #     item['note']=response.css('.sc-52d569c6-1 span.sc-bde20123-1::text').extract()
    #     item['genre'] = response.css('div.ipc-chip-list__scroller ::text').extract()
    #     item['duree']=convert_to_minutes(response.css('.sc-afe43def-4 li:nth-of-type(3) ::text').extract())
    #     item['synopsis']=response.css('span.sc-5f699a2-2 ::text').extract()
    #     item['casting']=response.css('.sc-52d569c6-3 .ipc-metadata-list-item--link div ::text').extract()
    #     item['pays']=response.css   ("[data-testid='title-details-origin'] a::text").extract()
    #     item['public']=response.css('.sc-afe43def-4 li:nth-of-type(2) a::text').extract()
    #     item['affiche'] = response.css('div.ipc-media--poster-l img.ipc-image::attr(src)').extract_first()
