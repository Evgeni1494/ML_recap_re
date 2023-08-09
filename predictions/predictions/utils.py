import ast, requests, os, json
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
tmdb_key = os.getenv('TMDB_KEY')


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