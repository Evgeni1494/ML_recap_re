from django.shortcuts import render
import pyodbc
import pandas as pd

def test_sql(request):
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

        query = "SELECT TOP 10 id, titre, nbre_entrees FROM [dbo].[bdd_model_ML_cat]"

        data_frame = pd.read_sql_query(query, connection)

        # Fermer la connexion
        connection.close()

        return {'data_frame': data_frame, 'is_empty': data_frame.empty}
    except Exception as e:
        return {'error_message': str(e)}





def monitoring(request):
    return {}


def combined_view(request):
    
        # Récupérer les données des deux vues
        monitoring_data = monitoring(request)
        test_sql_data = test_sql(request)

        # Combinez les données
        combined_data = {**monitoring_data, **test_sql_data}

        return render(request, 'monitoring.html', combined_data)


