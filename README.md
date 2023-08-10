# Projet Nostradamus Cinéma

Ce projet est conçu pour prédire le nombre d'entrées d'un film au cinéma qui est capable de capter 1/3000 de personnes en france qui vont au cinéma, la connexion à une base de données Azure SQL pour récupérer des informations liées au cinéma, et afficher ces informations sur un tableau de bord.
Fonctionnalités principales

    Authentification et Gestion des Utilisateurs :
        Inscription d'un nouvel utilisateur.
        Connexion d'un utilisateur existant.
        Réinitialisation du mot de passe via un lien de réinitialisation envoyé par e-mail.
        Prédiction du nombre d'entrée d'un film.
        Comparaison de la prédiction avec les données réels.

    Connexion à la Base de Données Azure SQL :
        Récupération des données d'évaluation des films.
        Récupération des films qui sortent cette semaine de la table dans Azur SQL.
        Récupération des entrées de la table Azur SQL entre le prochain mercredi et le mardi suivant.

    Affichage des Données :
        Les données récupérées sont affichées dans différents tableaux de bord, notamment evaluation, monitoring et dashboard.

# Comment l'utiliser

    Allez sur le site de l'application : http://20.123.74.176:8000/
    Inscrivez vous.
    Connectez vous.
    Recuperez les informations sur les sorties et les prédictions. (ça peut prendre un peu de temps)



# Le modele.

    Le modele de machine learning utilisé pour ce projet a était entrainé sur AzurML.
    La performance du modele s'éléve a 0.73 de R2.
    Le modele utilisé pour la prédiction est un Voting Ensemble de LightGBM,XGBoost et RandomForest Extreme Regressor.
    L'entrainement du modele a était fait sur un dataset obtenu par scraping de sites Allociné et JPbox.
    Le dataset d'entrainement était composé d'environ 2600 lignes.
    L'API endpoint du modele est celui de AzurML.

# Déployment
    L'application a était crée avec Django.
    Le déployement a était fait avec Docker et AzurVM.
    L'application Django est dans une image Docker qui est executé sur une VM Azur.
    




# Contributions

Les contributions sont les bienvenues ! Si vous souhaitez contribuer, veuillez créer une issue ou soumettre une pull request.
Licence

Ce projet est sous licence MIT. Pour plus de détails, voir le fichier LICENSE.

