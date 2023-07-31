# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from dotenv import load_dotenv
import pymongo, os, csv, time, requests
from .utils import extraire_id, extraire_budget
from .spiders.allocine import AlloCineSpider

load_dotenv()
ATLAS_KEY = os.getenv('ATLAS_KEY')
TMDB_KEY = os.getenv('TMDB_KEY')

class AlloCinePipeline:
    def __init__(self):
        self.client = pymongo.MongoClient(ATLAS_KEY)
        self.db = self.client["ML_re"]
        self.collection = self.db[f"films_allocine"]  ### switch to 2020 / 2010 / 2000
        # if os.path.exists('films.csv'):
        #     os.remove('films.csv')
        # self.csvfile = open(f'films.csv', mode='a+', newline='')
        # self.fieldnames = ['titre', 'titre_original', 'duree', 'date_de_sortie', 'genres', 'directeur', 'acteurs', 'synopsis', 'note_presse', 'note_spectateurs', 'nationalite', 'box_office_france', 'prix', 'nominations', 'budget']
        # self.writer = csv.DictWriter(self.csvfile, fieldnames=self.fieldnames)
        # self.writer.writeheader()


    def process_item(self, item, spider):
        if item.get('titre_original') != '':
            id_tmdb = extraire_id(item.get('titre_original'))
        else:
            id_tmdb = extraire_id(item.get('titre'))
        budget = extraire_budget(id_tmdb)
        try:
            # self.writer.writerow({      ### Enregistrement sur CSV
            #     'titre': item.get('titre'),
            #     'titre_original': item.get('titre_original'),
            #     'duree': item.get('duree'),
            #     'date_de_sortie': item.get('date_de_sortie'),
            #     'genres': item.get('genres'),
            #     'directeur': item.get('directeur'),
            #     'acteurs': item.get('acteurs'),
            #     'synopsis': item.get('synopsis'),
            #     'note_presse': item.get('note_presse'),
            #     'note_spectateurs': item.get('note_spectateurs'),
            #     'nationalite': item.get('nationalite'),
            #     'box_office_france': item.get('box_office_france'),
            #     'prix': item.get('prix'),
            #     'nominations' : item.get('nominations'),
            #     'budget' : budget
            # })
            

            self.collection.insert_one({        ### Enregistrement sur MongoDB
                'titre': item.get('titre'),
                'titre_original': item.get('titre_original'),
                'duree': item.get('duree'),
                'date_de_sortie': item.get('date_de_sortie'),
                'genres': item.get('genres'),
                'directeur': item.get('directeur'),
                'acteurs': item.get('acteurs'),
                'synopsis': item.get('synopsis'),
                'note_presse': item.get('note_presse'),
                'note_spectateurs': item.get('note_spectateurs'),
                'nationalite': item.get('nationalite'),
                'box_office_france': item.get('box_office_france'),
                'prix': item.get('prix'),
                'nominations': item.get('nominations'),
                'budget' : budget
            })
            time.sleep(1)
        except Exception as e:
            self.logger.error(f"Error processing item: {e}")
            
        
        return item
    
    def close_spider(self, spider):
        self.csvfile.close()
