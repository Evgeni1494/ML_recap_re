# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from predictions.utils import get_prediction
import urllib.request
import json
import os
import ssl
from .utils import extraire_id, extraire_budget, extraire_poster
# useful for handling different item types with a single interface
import pyodbc
from dotenv import load_dotenv
import pyodbc
import requests
load_dotenv()
server='projet-affluence-cinema-mlrecap.database.windows.net'
database='BDD_boxoffice'
username = 'project_affluence_cinema'
password = os.getenv('password')
driver = 'ODBC Driver 18 for SQL Server'


    
class PredictionsPipeline:
    def open_spider(self, spider):
        """
        Méthode appelée lorsque la toile (spider) est ouverte.

        Cette méthode initialise la connexion à la base de données SQL Server
        en utilisant les informations de connexion stockées dans les variables d'environnement.

        Args:
            spider (scrapy.Spider): L'instance du spider en cours d'exécution.
        """
        server='projet-affluence-cinema-mlrecap.database.windows.net'
        database='BDD_boxoffice'
        username = 'project_affluence_cinema'
        password = os.getenv('password')
        driver = 'ODBC Driver 18 for SQL Server'

        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

        self.conn = pyodbc.connect(conn_str)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        """
        Méthode appelée lorsque la toile (spider) est fermée.

        Cette méthode ferme la connexion à la base de données SQL Server.

        Args:
            spider (scrapy.Spider): L'instance du spider en cours d'exécution.
        """
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        self.cursor.execute(
        'INSERT INTO actualisation_scrap2 (title, country, genre, date, durée, acteurs, acteur1_success, acteur2_success, director_success, cast_success) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (
            item["title"], item["country"], item["genre"], item["date"],
            item["durée"], item["acteurs"], item["acteur1_success"],
            item["acteur2_success"], item['director_success'], item['cast_success']
        )
    )
        self.conn.commit()
        prediction=get_prediction(item["title"],item["country"],item["genre"],item["date"],item["durée"],item["acteurs"],item["acteur1_success"],item["acteur2_success"],item['director_success'],item['cast_success'])
        
        # api_data =  {
        #     "Inputs": {
        #         "data": [
        #         {
        #             "title": item["title"],
        #             "country": item["country"],
        #             "genre": item["genre"],
        #             "date": item["date"],
        #             "durée": item["durée"],
        #             "acteurs": item["acteurs"],
        #             "acteur1_success": item["acteur1_success"],
        #             "acteur2_success": item["acteur2_success"],
        #             "director_success": item['director_success'],
        #             "cast_success": item['cast_success']
        #         }
        #         ]
        #     },
        #     "GlobalParameters": 0.0
        #         }
        # api_response = requests.post('URL_DE_VOTRE_API', json=api_data)
        # api_result = api_response.json()
        print("icicicicicicicicicici",prediction)
    # Mettre à jour la colonne 'pred' dans la même ligne
        update_query = (
            'UPDATE actualisation_scrap2 '
            'SET pred = ? '
            'WHERE title = ?'  # Remplacez par la condition appropriée pour identifier la ligne
        )
        self.cursor.execute(update_query, (prediction, item["title"]))
        print(item['title'])
        self.conn.commit()

        return item
        