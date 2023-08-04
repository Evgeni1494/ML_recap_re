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

# class ScrapingActuPipeline:
#     def process_item(self, item, spider):
#         return item



# class PipelineSQL:
#     def __init__(self, server, database, username, password):
#         self.server = server
#         self.database = database
#         self.username = username
#         self.password = password
#         print(self.server)
#         print(database)
#         print(username)
#         print(password)
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             server=crawler.settings.get('server'),
#             database=crawler.settings.get('database'),
#             username=crawler.settings.get('username'),
#             password=crawler.settings.get('password')
#         )

#     def open_spider(self, spider):
#         self.connection = pyodbc.connect(
#             f'DRIVER={{ODBC Driver 18 for SQL Server}};'
#             f'SERVER={self.server};'
#             f'DATABASE={self.database};'
#             f'UID={self.username};'
#             f'PWD={self.password};'
#         )
#         self.cursor = self.connection.cursor()

#     def close_spider(self, spider):
#         self.connection.close()

#     def process_item(self, item, spider):
#         self.connection.insert_one(item)# Écrire ici la logique pour insérer les données dans la base de données Azure SQL
#         pass

    
class PipelineSQL:
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
             

    # def process_item(self, item, spider):
    #     """
    #     Méthode appelée pour traiter chaque élément (item) extrait.

    #     Cette méthode insère les données extraites dans la table "films_prediction" de la base de données.

    #     Args:
    #         item (dict): Dictionnaire contenant les données extraites de la page Web.
    #         spider (scrapy.Spider): L'instance du spider en cours d'exécution.

    #     Returns:
    #         dict: L'objet item d'origine qui sera transmis aux autres pipelines (s'il en existe).
    #     """
    #     self.cursor.execute(
    #         'INSERT INTO scrapings ( title, distributeur, genre,dati ) '
    #         'VALUES (?, ?, ?, ?)',
    #         (item["title"], item["distributeur"], item["genre"], item["dati"]))
    #     self.conn.commit()