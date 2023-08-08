import pyodbc
import re
from dotenv import load_dotenv
import os
from datetime import datetime

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Informations de connexion à la base de données
server = 'projet-affluence-cinema-mlrecap.database.windows.net'
database = 'BDD_boxoffice'
username = 'project_affluence_cinema'
password = os.getenv('password')
driver = 'ODBC Driver 18 for SQL Server'

# Afficher le mot de passe pour débogage (retirer ceci dans un environnement de production)
print(password)

# Chaîne de connexion
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    # Connexion à la base de données
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Création de la table actualisation_scrap1
    cursor.execute("""
        DROP TABLE IF EXISTS actualisation_scrap1;
        CREATE TABLE actualisation_scrap1(
            titre TEXT PRIMARY KEY NOT NULL,
            duree TEXT NOT NULL,
            date_de_sortie VARCHAR(20) NOT NULL,
            genres VARCHAR(70) NOT NULL,
            directeur TEXT NOT NULL,
            distributeur TEXT,
            acteurs VARCHAR(70) NOT NULL,
            nationalite TEXT NOT NULL,
            prediction_film FLOAT DEFAULT NULL,
            ecart_eval_predict FLOAT DEFAULT NULL
        );
    """)
    conn.commit()

    # Création de la table assoc_film_pred
    cursor.execute("""
        DROP TABLE IF EXISTS assoc_film_pred;
        CREATE TABLE assoc_film_pred(
            table_pred INT DEFAULT NULL,
            entrees_reel INT DEFAULT NULL,
            FOREIGN KEY (table_pred) REFERENCES actualisation_scrap1(titre),
            FOREIGN KEY (entrees_reel) REFERENCES prediction_eval(titre)
        );
    """)
    conn.commit()

    # Création de la table prediction_eval
    cursor.execute("""
        DROP TABLE IF EXISTS prediction_eval;
        CREATE TABLE prediction_eval(
            titre TEXT PRIMARY KEY NOT NULL,
            prediction_ML FLOAT NULL,
            nbre_entre_reel INT NULL,
            diff_pred_eval FLOAT NULL
        );
    """)
    conn.commit()

except pyodbc.Error as ex:
    print("Erreur de connexion à la base de données :", ex)

finally:
    # Fermer le curseur et la connexion
    cursor.close()
    conn.close()
