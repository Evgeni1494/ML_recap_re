# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pyodbc
from dotenv import load_dotenv
import os
import pyodbc

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
        'INSERT INTO scrapings (title, distributeur, genre, dati ) '
        'VALUES (?, ?, ?, ?)',
        (item["title"], item["distributeur"], item["genre"], item["dati"]))
        self.conn.commit()

        return item