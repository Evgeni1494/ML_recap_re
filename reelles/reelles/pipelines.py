# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv, os


class ReellesPipeline:
    def __init__(self):
        if os.path.exists('real_data.csv'):   # Création et parametrage du csv
            os.remove('real_data.csv')
        self.csvfile = open(f'real_data.csv', mode='a+', newline='')
        self.fieldnames = ['titre', 'date_de_sortie', 'entrees_premiere_semaine']
        self.writer = csv.DictWriter(self.csvfile, fieldnames=self.fieldnames)
        if self.csvfile.tell() == 0:
            self.writer.writeheader()
        
    def process_item(self, item, spider):
        
        self.writer.writerow({
            'titre': item.get('titre'),
            'date_de_sortie': item.get('date_de_sortie'),
            'entrees_premiere_semaine': item.get('entrees_premiere_semaine')
        })
            
            