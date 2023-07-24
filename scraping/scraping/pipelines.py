# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from dotenv import load_dotenv
import os
import csv

load_dotenv()
ATLAS_KEY = os.getenv('ATLAS_KEY')

class ScrapingPipeline:
    def __init__(self):
        self.csvfile = open('films.csv', mode='a', newline='')
        self.fieldnames = ['titre', 'date_de_sortie', 'genres', 'directeur', 'acteurs', 'synopsis', 'note_presse', 'note_spectateurs', 'nationalite', 'budget', 'box_office_france', 'prix_et_nominations']
        self.writer = csv.DictWriter(self.csvfile, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def process_item(self, item, spider):
        self.writer.writerow({
            'titre': item.get('titre'),
            'date_de_sortie': item.get('date_de_sortie'),
            'genres': item.get('genres'),
            'directeur': item.get('directeur'),
            'acteurs': item.get('acteurs'),
            'synopsis': item.get('synopsis'),
            'note_presse': item.get('note_presse'),
            'note_spectateurs': item.get('note_spectateurs'),
            'nationalite': item.get('nationalite'),
            'budget': item.get('budget'),
            'box_office_france': item.get('box_office_france'),
            'prix_et_nominations': item.get('prix_et_nominations')
        })
        return item

    def close_spider(self, spider):
        self.csvfile.close()
