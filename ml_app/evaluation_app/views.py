from django.shortcuts import render
import pyodbc
import pandas as pd
from datetime import datetime, timedelta

def eval_data(request):
    """
    Se connecte à une base de données Azure SQL, exécute une requête SQL pour récupérer 
    les données d'évaluation de films, et renvoie les résultats.
    """
    try:
        # Se connecter à la base de données Azure SQL
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=projet-affluence-cinema-mlrecap.database.windows.net;'
            'DATABASE=BDD_boxoffice;'
            'UID=project_affluence_cinema;'
            'PWD=*Boxoffice1;'
        )

        # Calculer les dates pour deux semaines avant aujourd'hui
        date_actuelle = datetime.now()
        jour_de_semaine_actuel = date_actuelle.weekday()
        jours_jusqua_mercredi = (jour_de_semaine_actuel - 2) % 7
        dernier_mercredi = date_actuelle - timedelta(days=jours_jusqua_mercredi + 7)
        mardi_suivant = dernier_mercredi + timedelta(days=6)
        dernier_mercredi_str = dernier_mercredi.strftime('%Y-%m-%dT%H:%M:%S.%f')
        mardi_suivant_str = mardi_suivant.strftime('%Y-%m-%dT%H:%M:%S.%f')

        query = f"""
                    SELECT * FROM [dbo].[actu_scrap_poster1] 
                    WHERE [date] BETWEEN '{dernier_mercredi_str}' AND '{mardi_suivant_str}'
                    ORDER BY evaluation_ML DESC
                """

        data_eval = pd.read_sql_query(query, connection)

        # Fermer la connexion
        connection.close()

        return {'data_eval': data_eval, 'is_empty': data_eval.empty}
    except Exception as e:
        return {'error_message': str(e)}



    
def evaluation(request):
    return render(request, 'evaluation.html')

def combined_eval(request):
        """
    Récupère les données d'évaluation des films depuis deux sources différentes (à savoir les fonctions `eval_data` et `evaluation`),
    les combine et renvoie les données combinées pour être affichées dans le template 'evaluation.html'.
        """
    
        # Récupérer les données des deux vues
        eval_data_data = eval_data(request)
        
        # Votre fonction "evaluation" doit également renvoyer un dictionnaire pour être cohérente avec eval_data
        evaluation_data = evaluation(request)

        # Combinez les données
        combined_data = {
            'data_eval': eval_data_data['data_eval'],
            'is_empty': eval_data_data['is_empty'],
            'evaluation_data': evaluation_data  # Ajoutez d'autres clés du dictionnaire de votre fonction 'evaluation' si nécessaire
        }

    
        return render(request, 'evaluation.html', combined_data)
    

