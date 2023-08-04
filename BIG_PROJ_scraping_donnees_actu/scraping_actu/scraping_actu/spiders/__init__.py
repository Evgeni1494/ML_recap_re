import os
import pyodbc
from dotenv import load_dotenv
from scrapy.exceptions import DropItem

class AzureSQLPipeline:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.server = os.getenv('DB_SERVER')
        self.database = os.getenv('DB_name')
        self.DB_Driver = os.getenv('DB_Driver')
        self.spider_name = None

    def open_spider(self, spider):
        self.spider_name = spider.name
        
        if spider.name == 'top_acteurs_spider':
            # Établir la connexion
            connection_string = f'Driver={self.DB_Driver};Server=tcp:{self.server},1433;Database={self.database};Uid={self.username};Pwd={self.password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
            self.conn = pyodbc.connect(connection_string)
            self.cursor = self.conn.cursor()

            self.delete_table('top_acteurs')

            # Créer la table "top_acteur"
            create_top_acteur_table_query = '''
            CREATE TABLE top_acteur (
                id INT IDENTITY(1,1) PRIMARY KEY,
                acteur VARCHAR(500)
            );
            '''
            self.cursor.execute(create_top_acteur_table_query)
            self.conn.commit()

        
        if self.spider_name == 'films_spider':
            # Établir la connexion
            connection_string = f'Driver={self.DB_Driver};Server=tcp:{self.server},1433;Database={self.database};Uid={self.username};Pwd={self.password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
            self.conn = pyodbc.connect(connection_string)
            self.cursor = self.conn.cursor()

            # Delete les tables s'il existent
            self.delete_table('acteurs_films')
            self.delete_table('films')


            # Créer la table "films"
            create_table_query = '''
            CREATE TABLE films (
                id INT IDENTITY(1,1) PRIMARY KEY,
                titre VARCHAR(500),
                date VARCHAR(500),
                duree VARCHAR(500),
                realisateur VARCHAR(500),
                distributeur VARCHAR(500),
                nationalites VARCHAR(500),
                langue_d_origine VARCHAR(500),
                type_film VARCHAR(500),
                annee_production VARCHAR(500),
                nombre_article VARCHAR(500),
                description VARCHAR(2000),
                genre VARCHAR (1000),
                film_id_allocine VARCHAR(10),
                image VARCHAR(1000)
            );
            '''
            self.cursor.execute(create_table_query)
            self.conn.commit()
            
            
            # Créer la table "acteurs_films"
            create_acteurs_films_table_query = '''
            CREATE TABLE acteurs_films (
                id_acteurs_films INT IDENTITY(1,1) PRIMARY KEY,
                film_id INT,
                acteurs VARCHAR(500),
                FOREIGN KEY (film_id) REFERENCES films(id)
                    );
                '''
            self.cursor.execute(create_acteurs_films_table_query)
            self.conn.commit()



    def delete_table(self, table_name):
        drop_table_query = f'DROP TABLE IF EXISTS {table_name};'
        self.cursor.execute(drop_table_query)
        self.conn.commit()

    def close_spider(self, spider):
        if self.spider_name == 'films_spider':
            self.conn.close()

    def process_item(self, item, spider):
        if self.spider_name == 'films_spider':
            try:
                query = '''
                INSERT INTO films (titre, date, duree, genre, realisateur, distributeur, nationalites, langue_d_origine, type_film, annee_production, nombre_article, description, film_id_allocine, image)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                '''
                self.cursor.execute(query, (
                    item['titre'], item['date'], item['duree'], item['genre'], item['realisateur'], item['distributeur'],
                    item['nationalites'], item['langue_d_origine'], item['type_film'],
                    item['annee_production'], 
                    item['nombre_article'], item['description'], item['film_id_allocine'], item['image']
                ))
                self.conn.commit()
                film_id = self.cursor.execute("SELECT @@IDENTITY").fetchone()[0]
            except Exception as e:
                # En cas d'erreur lors de l'insertion, vous pouvez choisir de supprimer l'item ou de le logger
                raise DropItem(f'Erreur lors de l\'insertion des données dans la base de données films : {e}')

            try:
                # Insérer les acteurs dans la table "acteurs_films" en les associant avec l'ID du film
                for acteur in item['acteurs']:
                    acteur_query = '''
                    INSERT INTO acteurs_films (film_id, acteurs)
                    VALUES (?, ?);
                    '''
                    self.cursor.execute(acteur_query, (film_id, acteur))
                    self.conn.commit()
            except Exception as e:
                # En cas d'erreur lors de l'insertion, vous pouvez choisir de supprimer l'item ou de le logger
                raise DropItem(f'Erreur lors de l\'insertion des données dans la base de données acteurs : {e}')
        
            if spider.name == 'top_acteurs_spider':
                try:
                    # Insérer les acteurs dans la table "top_acteur"
                    for acteur in item['acteur']:
                        acteur_query = '''
                        INSERT INTO top_acteur (acteur)
                        VALUES (?);
                        '''
                        self.cursor.execute(acteur_query, (acteur,))
                        self.conn.commit()

                except Exception as e:
                # En cas d'erreur lors de l'insertion, vous pouvez choisir de supprimer l'item ou de le logger
                    raise DropItem(f'Erreur lors de l\'insertion des données dans la base de données acteurs : {e}')

        return item 
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
