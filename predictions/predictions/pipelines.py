# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv, os
from .utils import extraire_id, extraire_budget, extraire_poster

class PredictionsPipeline:
    def __init__(self):
        self.csvfile = open(f'predi_films.csv', mode='a+', newline='')
        self.fieldnames = ['titre', 'titre_original', 'duree', 'date_de_sortie', 'genres', 'directeur', 
                           'distributeur',
                           'acteurs', 'nationalite', 'budget', 'poster']
        self.writer = csv.DictWriter(self.csvfile, fieldnames=self.fieldnames)
        if self.csvfile.tell() == 0:
            self.writer.writeheader()
    
    def process_item(self, item, spider):
        if item.get('titre_original') != '':
            id_tmdb = extraire_id(titre=item.get('titre_original'),date_de_sortie=item.get('date_de_sortie'),duree=item.get('duree'))
        else:
            id_tmdb = extraire_id(titre=item.get('titre'),date_de_sortie=item.get('date_de_sortie'),duree=item.get('duree'))
        budget = extraire_budget(id_du_film=id_tmdb)
        poster = extraire_poster(id_du_film=id_tmdb)

        self.writer.writerow({      ### Enregistrement sur CSV
            'titre': item.get('titre'),
            'titre_original': item.get('titre_original'),
            'duree': item.get('duree'),
            'date_de_sortie': item.get('date_de_sortie'),
            'genres': item.get('genres'),
            'directeur': item.get('directeur'),
            'distributeur': item.get('distributeur'),
            'acteurs': item.get('acteurs'),
            'nationalite': item.get('nationalite'),
            'budget': budget,
            'poster': poster
        })
