import ast, requests, os, json
from dotenv import load_dotenv
from datetime import datetime, timedelta
from datetime import datetime
import locale
load_dotenv()
tmdb_key = os.getenv('TMDB_KEY')
import urllib.request
import json




months_map = {
    'janvier': 'January',
    'février': 'February',
    'mars': 'March',
    'avril': 'April',
    'mai': 'May',
    'juin': 'June',
    'juillet': 'July',
    'août': 'August',
    'septembre': 'September',
    'octobre': 'October',
    'novembre': 'November',
    'décembre': 'December'
}

import dateparser

def convert_to_iso8601(date_string):
    # Utiliser le module dateparser pour analyser la date
    date_object = dateparser.parse(date_string)
    
    if date_object:
        # Formater la date en ISO 8601
        iso8601_date = date_object.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return iso8601_date
    else:
        return None

# Exemple de date au format "8 janvier 2020"

def extract_first_name(names_string):
    # Diviser la chaîne en utilisant la virgule comme séparateur
    names_list = names_string.split(',')

    # Extraire le premier nom et le nettoyer (supprimer les espaces avant et après)
    if names_list:
        first_name = names_list[0].strip()
        return first_name
    else:
        return names_string
    
def extract_2_name(names_string):
    # Diviser la chaîne en utilisant la virgule comme séparateur
    names_list = names_string.split(',')

    # Extraire le premier nom et le nettoyer (supprimer les espaces avant et après)
    if names_list:
        first_name = names_list[1].strip()
        return first_name
    else:
        return None
    
def extract_3_name(names_string):
    # Diviser la chaîne en utilisant la virgule comme séparateur
    names_list = names_string.split(',')

    # Extraire le premier nom et le nettoyer (supprimer les espaces avant et après)
    if names_list:
        first_name = names_list[2].strip()
        return first_name
    else:
        return None


def convert_to_iso86011(date_string):
    # Configurer la locale en français
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

    # Convertir la date en un objet datetime
    date_object = datetime.strptime(date_string, '%d %B %Y')

    # Formater la date en ISO 8601
    iso8601_date = date_object.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    return iso8601_date

def enlever_espace_pays(liste_de_pays:str) -> list:
    """
    Les pays scrappés comportent tous un espace au début de leur chaîne de caractères propre
    Prends un str, le transforme en liste puis enlève le premier caractère de chaque élément
    
    :param liste_de_pays: Le str transformable en list
    :return liste_de_pays_sans_espace: la liste mise en forme
    """
    liste_de_pays = ast.literal_eval(liste_de_pays)
    liste_de_pays_sans_espace = []
    for pays in liste_de_pays:
        pays = pays[1:]
        liste_de_pays_sans_espace.append(pays)
    return liste_de_pays_sans_espace


def extraire_prix_et_nominations(texte:str) -> tuple:
    """
    Trouve les chiffres correspondant aux nombre de prix et de nominations du film dans le texte scrapé
    
    :param texte: texte scrapé
    :return prix_et_nominations: Un tuple composé du nombre de récompenses en valeur 1 et le nombre de nominations en valeur 2
    """
    texte = texte.strip()

    try:
        nombre_de_prix = int(texte.split('prix')[0][:-1]) if 'prix' in texte else 0
    except ValueError:
        nombre_de_prix = 0

    try:
        if 'nomination' in texte:
            tokens = texte.split('nomination')[0].split(' ')
            chiffres = [int(token) for token in tokens if token.isdigit()]
            nombre_de_nominations = chiffres[-1] if chiffres else 0
        else:
            nombre_de_nominations = 0
    except ValueError:
        nombre_de_nominations = 0

    prix_et_nominations = (nombre_de_prix, nombre_de_nominations)
    return prix_et_nominations


def strip_texte(texte:str) -> str:
    """
    Pour nettoyer les données scrapées,
    retourne le texte sans les espaces ou passages à la ligne au debut ou à la fin du string

    :param texte: chaine de caractères scapée
    :return texte: texte nettoyé
    """
    return texte.strip()

def extraire_entrees(texte:str) -> int:
    """
    Extrait le nombres d'entrées de la chaine de caractères afin de retirer de le mot "entrées" et les espaces"
    
    :param texte: donnée à nettoyer
    :return nombre: nombre d'entrée du box office extrait
    """
    texte = texte.split()
    nombre = ''.join(caractere for caractere in texte if caractere.isdigit())
    return int(nombre)


def extraire_id(titre:str, date_de_sortie:str=None, duree:str=None) -> int:
    """
    Réalise une requête sur l'API TMDB pour extraire l'id du film dans le meilleur résultat de la recherche textuelle
    La recherche se fait sur le titre et optionnellement sur la date de sortie et la duree pour plus d'exactitude sur le film requêté
    :param query: nom du film à requêter
    :param date de sortie: date de sortie en salle au format scrapé J(int) mois-en-toutes-lettres AAAA(int)
    :param duree: duree du film au format scrapé Nh NNmin
    :return extracted_id: id du meilleur resultat
    """

    base_url = "https://api.themoviedb.org/3/search/movie"

    # Construction des paramètres pour la recherche
    params = {"api_key": tmdb_key, "query": titre}
    
    if date_de_sortie:
        params["year"] = date_de_sortie[-4:]

    if duree:
        heures = duree.split('h')[0]
        minutes = duree.split('min')[0][-2:]
        duree_en_minutes = int(heures)*60+int(minutes)
        params["runtime"] = duree_en_minutes
        
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()   
        if data['results']:
            id_extrait = data["results"][0]["id"]
            return id_extrait
        else:
            return None
    except requests.exceptions.RequestException as e:
        print("Erreur lors de la récupération des données:", e)
        
        
def extraire_budget(id_du_film:int) -> int:
    """
    Réalise une requête sur l'API TMDB depuis l'id d'un film pour en extraire le budget
    
    :param id_du_film: integer de l'id. (extracted_id depuis extraire_id)
    :return budget: budget du film extrait de l'API
    """
    base_url = "https://api.themoviedb.org/3/movie"
    endpoint = f"{base_url}/{id_du_film}?api_key={tmdb_key}"
    try:
        response = requests.get(endpoint)
        response.raise_for_status() # Raise an exception for HTTP errors (if any)
        data = response.json()
        budget = data['budget']
        if budget:
            return budget
        else:
            return 0
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        

def mercredi_suivant():
    """
    Consulte la date du jour, et retourne la date du prochain mercredi au format DD/MM/AAAA
    """
    date_actuelle = datetime.now()
    jour_de_semaine_actuel = date_actuelle.weekday()
    jours_jusqua_mercredi = (2 - jour_de_semaine_actuel) % 7
    mercredi_suivant = date_actuelle + timedelta(days=jours_jusqua_mercredi)
    date_prochain_mercredi = mercredi_suivant.strftime("%d/%m/%Y")
    return date_prochain_mercredi

def obtenir_details_films(id_film:int) -> dict :
    """
    Retourne un json avec toutes les données d'un films stockés sur TMDB depuis son id
    
    :param id_film: l'ID du film
    :return formatted_json: les données du film
    """
    base_url = "https://api.themoviedb.org/3/movie"
    
    # Endpoint for movie details and videos
    endpoint = f"{base_url}/{id_film}?api_key={tmdb_key}"
    
    try:
        response = requests.get(endpoint)
        response.raise_for_status() # Raise an exception for HTTP errors (if any)
        data = response.json()
        formatted_json = json.dumps(data, indent=2)
        return formatted_json
        
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        
def extraire_poster(id_du_film:int) -> int:
    """
    Réalise une requête sur l'API TMDB depuis l'id d'un film pour en extraire le chemin du poster
    La base d'url pour l'afficher sera https://image.tmdb.org/t/p + poster
    
    :param id_du_film: integer de l'id. (extracted_id depuis extraire_id)
    :return poster: extensien de chemin du poster
    """
    base_url = "https://api.themoviedb.org/3/movie"
    endpoint = f"{base_url}/{id_du_film}?api_key={tmdb_key}"
    try:
        response = requests.get(endpoint)
        response.raise_for_status() # Raise an exception for HTTP errors (if any)
        data = response.json()
        poster = data['poster_path']
        if poster:
            return poster
        else:
            return ''
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        
        
        
        
def l_s(a):
    for i in a:
        return i

def extract_duration_in_minutes(duration_str):
    # Supprimer les caractères "\n" au début et à la fin de la chaîne
    cleaned_duration_str = duration_str.strip()

    # Utiliser une expression régulière pour extraire les heures et les minutes
    pattern = r'(\d+)h (\d+)min'
    match = re.match(pattern, cleaned_duration_str)
    
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2))
        total_minutes = hours * 60 + minutes
        return total_minutes
    else:
        return None
    
    
import pandas as pd
import ast
import numpy as np

# Function to transform date to the required format
def transform_date(date):
    date_string = date
    sortie_string = date
    
    # Define a dictionary to map French month names to numbers
    month_dict = {
        'janvier': '01', 'février': '02', 'mars': '03', 'avril': '04', 
        'mai': '05', 'juin': '06', 'juillet': '07', 'août': '08', 
        'septembre': '09', 'octobre': '10', 'novembre': '11', 'décembre': '12'
    }
    
    # Check if the date is "00/00/0000"
    if date_string == "00/00/0000":
        # Replace French month names with numbers in sortie_string
        for month_name, month_number in month_dict.items():
            sortie_string = sortie_string.replace(month_name, month_number)

        # Convert the sortie date to the required format
        date = pd.to_datetime(sortie_string, format="%d %m %Y", errors='coerce')
    else:
        # Convert to datetime format
        date = pd.to_datetime(date_string, format="%d/%m/%Y", errors='coerce')
        
    # If the date conversion was successful
    if pd.notna(date):
        # Convert to ISO format and add the time
        date_iso = date.isoformat() + "Z"
    else:
        date_iso = None

    return date_iso


import pandas as pd

df= pd.read_csv('csv_ev.csv')
sub_df = df[['directeur', 'acteur1', 'acteur2', 'director_success', 'acteur1_success', 'acteur2_success','cast_success']]


director_dict = {}
actor_dict = {}

for index, row in sub_df.iterrows():
    director_dict[row['directeur']] = row['director_success']
    actor_dict[row['acteur1']] = row['acteur1_success']
    actor_dict[row['acteur2']] = row['acteur2_success']
    # actor_dict[row['acteur3_success']] = row['acteur3_success']
    # cast_dict[row['cast_success']]= row ['cast_success']

print(actor_dict)
director_dict_lower = {director.lower(): value for director, value in director_dict.items()}
actor_dict_lower = {actor.lower(): value for actor, value in actor_dict.items()}


# def avoir_acteur1  (acteurs):
#     b=acteurs.split(',')
#     return b[0]

# def avoir_acteur2  (acteurs):
#     b=acteurs.split(',')
#     return b[1]

def avoir_acteur1(acteurs):
    try:
        b = acteurs.split(',')
        return f"['{b[0].strip()}']"
    except:
        return f"['{acteurs.strip()}']"

def avoir_acteur2(acteurs):
    try:
        b = acteurs.split(',')
        if len(b) >= 2:
            return f"['{b[1].strip()}']"
        elif len(b) == 1:
            return f"['{b[0].strip()}']"
        else:
            return "[]"
    except:
        return f"['{acteurs.strip()}']"
    
def avoir_acteur3(acteurs):
    try:
        b = acteurs.split(',')
        if len(b) >= 2:
            return f"['{b[2].strip()}']"
        elif len(b) == 1:
            return f"['{b[0].strip()}']"
        else:
            return "[]"
    except:
        return f"['{acteurs.strip()}']"

def map_acteur1(acteur1):
    acteur1_lower = acteur1.lower()
    if acteur1_lower in actor_dict_lower:
        return actor_dict_lower[acteur1_lower]
    else:
        return 0
  
  
def map_acteur2(acteur2):
    acteur2_lower = acteur2.lower()
    if acteur2_lower in actor_dict_lower:
        return actor_dict_lower[acteur2_lower]
    else:
        return 0   
        
# def map_acteur3(acteur3):
    
#     acteur1_lower = acteur3.lower()
#     if acteur1_lower in actor_dict_lower:
#         acteur1_success = actor_dict_lower[acteur1_lower]
#     else:
#         acteur1_success = 0  
def map_director(directeur):
    
    acteur1_lower = directeur.lower()
    if acteur1_lower in director_dict_lower:
        acteur1_success = director_dict_lower[acteur1_lower]
        return acteur1_success
    else:
        return 0    

dico_genre={'Comédie musicale': 'Comédie', 'Animation': 'Animation', 'Comédie': 'Comédie', 'Thriller': 'Thriller', 'Romance': 'Romance', 'Guerre': 'Guerre', 'Famille': 'Film familial', 'Drame': 'Drame', 'Comédie dramatique': 'Comédie dramatique', 'Musical': 'Musical', 'Arts Martiaux': 'Arts martiaux', 'Fantastique': 'Fantasy', 'Science fiction': 'Science Fiction', 'Western': 'Western', 'Action': 'Animation', 'Péplum': 'Péplum', 'Aventure': 'Aventure - Action'}
def map_genre(genre):
    if genre in dico_genre:
        return( dico_genre[genre])
    else:
        return ('Comédie')      


def convert_to_minutes(time_string):
    # Diviser la chaîne en heures et minutes
    hours, minutes = time_string.split('h')
    minutes = minutes.split('min')[0]  # Supprimer "min" pour obtenir les minutes

    # Convertir les heures et minutes en minutes
    total_minutes = int(hours) * 60 + int(minutes)
    
    return total_minutes




def get_prediction(title, country, genre, date, durée, acteurs, 
                   acteur1_success, acteur2_success, director_success, cast_success):
    
    # Define the request data
    data = {
        "Inputs": {
            "data": [
                {
                    "title": title,
                    "country": country,
                    "genre": genre,
                    "date": date,
                    "durée": durée,
                    "acteurs": acteurs,
                    "acteur1_success": acteur1_success,
                    "acteur2_success": acteur2_success,
                    "director_success": director_success,
                    "cast_success": cast_success
                }
            ]
        },
        "GlobalParameters": 0.0
    }

    # Convert the data to a string and encode it
    body = str.encode(json.dumps(data))

    # Define the API URL and key
    url = 'https://movie-predictor.germanywestcentral.inference.ml.azure.com/score'
    api_key = os.getenv('cle_api')  # API KEY

    # Define the headers for the request
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': 'Bearer ' + api_key, 
        'azureml-model-deployment': 'movie-predictor'
    }

    # Make the request to the API
    req = urllib.request.Request(url, body, headers)
    
    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        prediction = json.loads(result)
        
        # Assuming the prediction result is in the 'result' key
        if 'Results' in prediction:
            prediction['Results'] = [value * (1/3000) for value in prediction['Results']]
        
        return prediction
    except urllib.error.HTTPError as error:
        return {"error": str(error.code), "message": error.read().decode("utf8", 'ignore')}








