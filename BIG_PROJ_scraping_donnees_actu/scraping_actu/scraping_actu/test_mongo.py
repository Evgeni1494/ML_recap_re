
from fonctions import extract_text_between_substrings
import scrapy
from scrapy.spiders import CrawlSpider, Rule

class TopfilmsspiderSpider(CrawlSpider):
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraping_actu.pipelines.TopFilmsPipeline': 400
        }
    }
    
    name = 'crawlerfilm'
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
        for i in range(2, 23114 ):
            print(i)
            print(i)
            print(i)
            yield scrapy.Request(url='https://www.jpbox-office.com/fichfilm.php?id={}&view=2'.format(i),
                                headers={'User-Agent': self.user_agent},
                                callback=self.parse_item)

    # def parse_item(self, response):
    #     film_items = response.css('td.col_poster_titre h3 a')
    #     nbre_entrees = response.css('td.col_poster_contenu_majeur::text').getall()

    #     for i, item in enumerate(film_items):
    #         film_item = {}boxoff_FRANCAIS_1st
    #         film_item['title'] = item.css('::text').get()
    #         film_item['nbre_entrees'] = nbre_entrees[i] if i < len(nbre_entrees) else None
    #         yield film_item
    def parse_item(self, response):
        film_id = int(re.search(r'id=(\d+)', response.url).group(1))
        distri_list = response.css('div.bloc_infos_center.tablesmall1').getall()
        print(distri_list)
        titles = response.css('td.texte_2022titre h1::text').get()
        genre = response.css('h3 a::text').getall()
        vrai_genre=genre[-2]
        print(vrai_genre)
        country = response.css('td.texte_2022titre a[href^="fichepays.php"]::text').get()
        title = response.css('td.texte_2022titre h1::text').get()
        date = response.css('div.bloc_infos_center.tablesmall1b p a[href^="v9_avenir.php"]::text').get()
        # chiffres_vrac=response.css('td.col_poster_contenu_majeur ::text').getall()
        # print(chiffres_vrac)
        # first_day_boxoffice=chiffres_vrac[4]
        # first_we_boxoffice=chiffres_vrac[5]
        # first_week_boxoffice=chiffres_vrac[6]
        # public=response.css('div.bloc_infos_center.tablesmall1::text').getall()
        # vrai_public=public[-1]
        # otr_distri=public[1]
        if title:
            cleaned_title = title.strip()    #cleaned title
        # if genre:
        #     cleaned_genre = genre.strip()
        if country:
            cleaned_country = country.strip()
        if date:
            cleaned_date = date.strip()
        print(cleaned_country)
        titles_ori=response.css('td.texte_2022titre h2::text').get()
        print("la distri:",distri_list)
        #for distri in distri_list[0]:
        #    print(1)
        distributor = extract_text_between_substrings(distri_list[0])
        #    print(distributor)
        #    print('8')
        film_item = {}
        film_item['id']=film_id
        film_item['title'] =cleaned_title
        film_item['title_original']=cleaned_title
        film_item['distributeur'] = distributor
        film_item['country']=cleaned_country
        film_item['genre']=vrai_genre
        film_item['date']=cleaned_date
        # 
        
        print(title)
        print(cleaned_title)
        print(distributor)
        yield film_item
