from django.shortcuts import render
import pyodbc
import pandas as pd


def eval_data(request):
    try:
        # Se connecter à la base de données Azure SQL
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=projet-affluence-cinema-mlrecap.database.windows.net;'
            'DATABASE=BDD_boxoffice;'
            'UID=project_affluence_cinema;'
            'PWD=*Boxoffice1;'
        )

        # Exécuter la requête SQL
        query = """
                    SELECT 
                    CASE WHEN evaluation_ML = 0 THEN 0 ELSE ISNULL(evaluation_ML, 0) END AS evaluation_ML,
                    ISNULL(prediction_film, 0) AS prediction_film,
                    CASE WHEN evaluation_ML = 0 THEN 0 ELSE ISNULL(ecart_eval_predict, 0) END AS ecart_eval_predict,
                    UPPER(LEFT(CONVERT(VARCHAR, title), 1)) + LOWER(SUBSTRING(CONVERT(VARCHAR, title), 2, LEN(CONVERT(VARCHAR, title)))) AS title, 
                    date 
                    FROM [dbo].[actualisation_scrap1]
                    ORDER BY date DESC, prediction_film DESC
                    OFFSET 0 ROWS
                    FETCH NEXT 10 ROWS ONLY

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
    

