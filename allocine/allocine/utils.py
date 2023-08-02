import ast, requests
import os
from dotenv import load_dotenv

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


def extraire_id(query:str) -> int:
    """
    Réalise une requête sur l'API TMDB pour extraire l'id du film dans le meilleur résultat de la recherche textuelle
    
    :param query: nom du film à requêter
    :return extracted_id: id du meilleur resultat
    """
    base_url = "https://api.themoviedb.org/3/search/movie"
    endpoint = f"{base_url}?api_key={tmdb_key}&query={query}"
    try:
        response = requests.get(endpoint)
        response.raise_for_status()  # Raise an exception for HTTP errors (if any)
        data = response.json()
        if data["results"]:
            extracted_id = data["results"][0]["id"] 
            return extracted_id
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
        