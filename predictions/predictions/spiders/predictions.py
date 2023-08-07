from datetime import datetime, timedelta
from scrapy.spiders import CrawlSpider
from ..items import PredictionsItem
import csv, os, scrapy

##############connection SQL et CREATE TABLE  ##################

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from itemadapter import ItemAdapter
from dotenv import load_dotenv
import os
import pyodbc
import re
load_dotenv()
from datetime import datetime


server='projet-affluence-cinema-mlrecap.database.windows.net'
database='BDD_boxoffice'
username = 'project_affluence_cinema'
password = os.getenv('password')
driver = 'ODBC Driver 18 for SQL Server'
print(password)


conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()




cursor.execute("DROP TABLE IF EXISTS actualisation_scrap")
cursor.execute(""" 
       CREATE TABLE actualisation_scrap(
            id INT PRIMARY KEY IDENTITY(1,1),
            titre TEXT NOT NULL,
            duree TEXT NOT NULL,
            date_de_sortie VARCHAR(20) NOT NULL,
            genres VARCHAR(70) NOT NULL,
            directeur TEXT NOT NULL,
            distributeur TEXT,
            acteurs VARCHAR(70) NOT NULL,
            nationalite TEXT NOT NULL,
            prediction_film FLOAT DEFAULT NULL,
            ecart_eval_predict FLOAT DEFAULT NULL
            )
""")

# Valider la transaction
conn.commit()

# Fermer le curseur et la connexion
cursor.close()
conn.close()


############       fonction conversion liste en STR           ###################
def l_s(a):
    return ",".join(map(str, a))


###################################################################### fction pour ajout valeures à la table créée   ###############

def ajouter_valeures(titre, duree, date_de_sortie, genres, directeur,distributeur, acteurs, nationalite) -> int: 
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(conn_str)
    
# Créer un curseur
    cursor = conn.cursor()
    cursor.execute(""" 
        INSERT INTO actualisation_scrap
        VALUES ( ?, ?, ?, ?,?,?,?,?, NULL, NULL)           
        """, ( titre, duree, date_de_sortie, genres, directeur,distributeur, acteurs, nationalite))       

    conn.commit()
    conn.close()
    
###################################################################################



class PredictionsSpider(CrawlSpider):
    name = "predictions"
    allowed_domains = ["allocine.fr"]
    
    def start_requests(self):
        
        date_actuelle = datetime.now()   
        jour_de_semaine_actuel = date_actuelle.weekday()
        jours_jusqua_mercredi = (2 - jour_de_semaine_actuel) % 7
        mercredi_suivant = date_actuelle + timedelta(days=jours_jusqua_mercredi)
        date_prochain_mercredi = mercredi_suivant.strftime("%d/%m/%Y") # Récupere la date du jour et se place au mercredi suivant
        
        jour = date_prochain_mercredi[0:2]
        mois = date_prochain_mercredi[3:5]
        annee = date_prochain_mercredi[6:10]
        
        url = f"https://www.allocine.fr/film/agenda/mois/mois-{annee}-{mois}/"
        yield scrapy.Request(url, callback=self.parse_start)
        
    def parse_start(self, response):
        for link in response.css('.month-movies-link::attr(href)').getall():
            yield response.follow(link, self.parse_movie_details)
           
    def parse_movie_details(self, response):
        items = PredictionsItem()
        
        titre = response.css('.titlebar-title-lg::text').get()
        if response.css('div.meta-body-item>span.light::text')[-1].get().strip() == 'Titre original':
            titre_original = response.css('div.meta-body-item::text')[-1].get()
        else:
            titre_original = ''
        duree = response.css('div.meta-body-item.meta-body-info::text')[3].get()
        date_de_sortie = response.css('div.meta-body-item.meta-body-info>span.blue-link::text').get()
        genres = l_s(response.css('div.meta-body-item.meta-body-info>span::text')[3:].getall())
        directeur = response.css('div.meta-body-item.meta-body-direction>span.blue-link::text').get()
        distributeur = response.css('div.item:nth-child(3)>:nth-child(2)::text').get()
        acteurs = l_s(response.css('.meta-body-actor.meta-body-item>span::text')[1:].getall())
        nationalite = l_s(response.css('span.that>.nationality::text').getall())
        print(titre, duree, date_de_sortie, genres, directeur, distributeur, acteurs, nationalite)
        ajouter_valeures(titre, duree, date_de_sortie, genres, directeur, distributeur, acteurs, nationalite)
        print('okkkkkkkkkk')
        # items['titre'] = titre.strip()
        # items['titre_original'] = titre_original.strip()
        # items['duree'] = duree.strip()
        # items['date_de_sortie'] = date_de_sortie.strip()
        # items['genres'] = genres
        # items['directeur'] = directeur
        # items['distributeur'] = distributeur.strip()
        # items['acteurs'] = acteurs
        # items['nationalite'] = nationalite

        # yield items





        # items['titre'] = titre.strip()
        # items['titre_original'] = titre_original.strip()
        # items['duree'] = duree.strip()
        # items['date_de_sortie'] = date_de_sortie.strip()
        # items['genres'] = genres
        # items['directeur'] = directeur
        # items['acteurs'] = acteurs
        # items['nationalite'] = nationalite
        # yield items
        
        # genres = ', '.join(genres)
        # acteurs = ', '.join(acteurs)
        # if not os.path.exists('movies.csv'):
        #     with open('movies.csv', 'a', newline='', encoding='utf-8') as csvfile:
        #         writer = csv.writer(csvfile)
        #         writer.writerow(['titre', 'titre_original', 'duree', 'date_de_sortie', 'genres', 'directeur', 'acteurs', 'synopsis', 'note_presse', 'nationalite'])
        # with open('movies.csv', 'a', newline='', encoding='utf-8') as csvfile:
        #     writer = csv.writer(csvfile)

        #     # Check if the file is empty, if yes, write the header
        #     if csvfile.tell() == 0:
        #         writer.writerow(['titre', 'titre_orignal', 'duree', 'date_de_sortie', 'genres', 'directeur', 'acteurs', 'synopsis', 'note_presse', 'nationalite'])

        #     # Write the data
        #     writer.writerow([titre, titre_original, duree[0], date_de_sortie[0], genres[0], directeur[0], acteurs, nationalite[0]])            