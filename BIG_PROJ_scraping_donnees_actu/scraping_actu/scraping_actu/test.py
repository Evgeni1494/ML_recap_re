# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from dotenv import load_dotenv
import os
import pyodbc
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# from fonctions import convert_to_minutes
# from mongodb_crawler.items import FilmItem
from fonctions import extract_text_between_substrings
import re
load_dotenv()

class AzureSQLPipeline:
    def __init__(self):
        # Informations de connexion
        server = 'projet-affluence-cinema-mlrecap.database.windows.net'
        database = 'BDD_boxoffice'
        username = 'project_affluence_cinema'
        password = os.getenv('password')
        driver = 'ODBC Driver 18 for SQL Server'

        # Établir la connexion
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        self.conn = pyodbc.connect(conn_str)

        # Créer un curseur
        self.cursor = self.conn.cursor()

        # Créer la table utilisateur si elle n'existe pas
        self.create_table()

    def create_table(self):
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS utilisateur (
                id INTEGER PRIMARY KEY IDENTITY(1,1),
                nom TEXT NOT NULL,
                email TEXT NOT NULL,
                mdp TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        # Insérer les données de l'item dans la table utilisateur
        self.cursor.execute(
            "INSERT INTO utilisateur (nom, email, mdp) VALUES (?, ?, ?)",
            item['nom'], item['email'], item['mdp']
        )
        self.conn.commit()
        return item

    def close_spider(self, spider):
        # Fermer le curseur et la connexion
        self.cursor.close()
        self.conn.close()
