from django.shortcuts import render
import pyodbc
import pandas as pd

def test_sql(request):
    """Se connecte à une base de données Azure SQL, exécute une requête SQL pour récupérer 
    les 10 premières entrées de la table [dbo].[bdd_model_ML_cat], et renvoie les résultats."""
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
        """
        Récupère les données des fonctions `monitoring` et `test_sql`, les combine, 
        puis renvoie les données combinées pour être affichées dans le template 'monitoring.html'.
        """
    
        # Récupérer les données des deux vues
        monitoring_data = monitoring(request)
        test_sql_data = test_sql(request)

        # Combinez les données
        combined_data = {**monitoring_data, **test_sql_data}

        return render(request, 'monitoring.html', combined_data)


