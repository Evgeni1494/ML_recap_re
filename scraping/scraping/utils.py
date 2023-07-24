import ast

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
    nombre_de_prix = 0
    nombre_de_nominations = 0
    if 'prix' in texte:
        nombre_de_prix = texte.split('prix')[0][:-1]
    if 'nomination' in texte:
        tokens = texte.split('nomination')[0].split(' ')
        chiffres = []
        for token in tokens:
            if token.isdigit():
                chiffres.append(token)
        nombre_de_nominations = chiffres[-1]
    prix_et_nominations = (nombre_de_prix, nombre_de_nominations)    
    return prix_et_nominations