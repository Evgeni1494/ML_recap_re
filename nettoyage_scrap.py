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

