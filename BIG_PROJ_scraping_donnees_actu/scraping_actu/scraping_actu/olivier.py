# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# from fonctions import extract_text_between_substrings
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
print(server)
print(database)
print(driver)
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()



cursor.execute("DROP TABLE IF EXISTS scrapings")
cursor.execute(""" 
       CREATE TABLE scrapings(
            id INT PRIMARY KEY IDENTITY(1,1),
            title TEXT NOT NULL,
            distributeur TEXT NOT NULL,
            genre TEXT NOT NULL,
            dati TEXT NOT NULL)
            """)

# Valider la transaction
conn.commit()

# Fermer le curseur et la connexion
cursor.close()
conn.close()



def ajouter_valeures(id, title, distributeur, genre,dati) -> int: 
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(conn_str)
    


# Créer un curseur
    cursor = conn.cursor()
    cursor.execute(""" 
        INSERT INTO scrapings
        VALUES ( ?, ?, ?, ?)           
        """, ( title, distributeur, genre,dati))       
  
    conn.commit()
    conn.close()
    
print(16)

film_id='2'
titles='grande marée'
genre='comédie'
country='france'
date='ICI'

ajouter_valeures(film_id,titles,genre,country,date)

class TopfilmsspiderSpider(CrawlSpider):
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'scraping_actu.pipelines.PipelineSQL': 400
    #     }
    # }
    
    name = 'crawlerfilm'
    allowed_domains = ['jpbox-office.com']
   
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'
    
    
    def start_requests(self):
        for i in range(2, 23114 ):
            print(i)
            print(i)
            print(i)
            yield scrapy.Request(url='https://www.jpbox-office.com/fichfilm.php?id={}&view=2'.format(i),
                                headers={'User-Agent': self.user_agent},
                                callback=self.parse_item)

  
    def parse_item(self, response):
        item={}
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
        if title:
            cleaned_title = title.strip()    #cleaned title
        if country:
            cleaned_country = country.strip()
        if date:
            cleaned_date = date.strip()
        print(cleaned_country)
        titles_ori=response.css('td.texte_2022titre h2::text').get()
        ajouter_valeures(film_id,titles,genre,country,date)
        item['title']=titles
        item['distributeur']=genre
        item['genre']=country
        item['dati']=title