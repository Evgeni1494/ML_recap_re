from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, LoginForm
from .models import User, FilmData
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
import uuid, pyodbc, pandas as pd
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from datetime import datetime, timedelta



def send_email_function():
    subject = 'Sujet de l\'e-mail'
    message = 'Contenu du message de l\'e-mail'
    from_email = 'django.nostradamus@gmail.com'  # Utilisez l'adresse Gmail que vous avez configurée dans votre fichier settings.py
    recipient_list = ['destinataire@example.com']  # Remplacez par l'adresse e-mail du destinataire

    send_mail(subject, message, from_email, recipient_list)


def logout_view(request):
    django_logout(request)
    return redirect('user_app:login')


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            
    else:
        form = SignupForm()
    
    return render(request, 'signup.html', {'form': form})
    

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue {username} !")
                return redirect('user_app:dashboard')  # Assurez-vous d'avoir une URL nommée 'dashboard' dans votre application 'user_app'
            else:
                messages.error(request, "Identifiants invalides")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})



def reset_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)

            # Générer un UUID unique pour le lien de réinitialisation
            reset_token = str(uuid.uuid4())

            # Enregistrez l'UUID dans la base de données avec l'utilisateur concerné
            user.reset_password_token = reset_token
            user.save()

            # Construisez l'URL de réinitialisation du mot de passe avec le jeton unique
            reset_url = request.build_absolute_uri(reverse('user_app:reset_password_confirm', args=[reset_token]))

            # Envoyer l'e-mail de réinitialisation avec l'URL de réinitialisation
            subject = 'Réinitialisation du mot de passe'
            message = f'Pour réinitialiser votre mot de passe, cliquez sur le lien ci-dessous : {reset_url}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)

            messages.success(request, 'Un lien de réinitialisation du mot de passe a été envoyé à votre adresse e-mail.')
        except User.DoesNotExist:
            messages.error(request, 'Aucun utilisateur trouvé avec cette adresse e-mail.')
    return render(request, 'reset_password.html')


def reset_password_confirm(request, reset_token):
    if request.method == 'POST':
        # Récupérez l'utilisateur associé au jeton unique
        try:
            user = User.objects.get(reset_password_token=reset_token)

            # Récupérez le nouveau mot de passe depuis le formulaire
            new_password = request.POST['new_password']

            # Réinitialisez le mot de passe de l'utilisateur et supprimez le jeton unique
            user.set_password(new_password)
            user.reset_password_token = None
            user.save()

            messages.success(request, 'Votre mot de passe a été réinitialisé avec succès.')
            return redirect('user_app:login')  # Redirigez l'utilisateur vers la page de login après la réinitialisation du mot de passe
        except User.DoesNotExist:
            messages.error(request, 'Jeton de réinitialisation de mot de passe invalide.')
            return redirect('user_app:reset_password')  # Redirigez l'utilisateur vers la page de réinitialisation du mot de passe s'il y a une erreur

    return render(request, 'reset_password_confirm.html')


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
    api_key = 'ga2YYNrFEWqxdIMGcSvO9xwJoFW0lZxJ'  # API KEY

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
        
        # Adding title to the prediction dictionary
        prediction['title'] = title
        
        # Assuming the prediction result is in the 'Results' key
        if 'Results' in prediction:
            prediction['Results'] = [value / 3000 for value in prediction['Results']]
        
        return prediction
    except urllib.error.HTTPError as error:
        return {"error": str(error.code), "message": error.read().decode("utf8", 'ignore')}



def get_predictions_for_all_rows(request):
    try:
        # Connect to the Azure SQL database
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=projet-affluence-cinema-mlrecap.database.windows.net;'
            'DATABASE=BDD_boxoffice;'
            'UID=project_affluence_cinema;'
            'PWD=*Boxoffice1;'
        )

        # Execute the SQL query
        query = "SELECT * FROM [dbo].[actualisation_scrap]"
        data_frame = pd.read_sql_query(query, connection)

        # Close the connection
        connection.close()

        predictions = []

        # Iterate over each row in the data frame and get predictions
        for _, row in data_frame.iterrows():
            prediction = get_prediction(
                title=row["title"],
                country=row["country"],
                genre=row["genre"],
                date=row["date"],
                durée=row["durée"],
                acteurs=row["acteurs"],
                acteur1_success=row["acteur1_success"],
                acteur2_success=row["acteur2_success"],
                director_success=row["director_success"],
                cast_success=row["cast_success"]
            )
            predictions.append(prediction)

        return {'predictions': predictions, 'is_empty': data_frame.empty}
    except Exception as e:
        return {'error_message': str(e)}






@login_required
def dashboard_view(request):

    # Récupérer les 10 films classés selon la prédiction du plus grand au plus petit
    # films = FilmData.objects.all().order_by('-prediction')[:10]
    # context = {'films': films}
    # return render(request, 'dashboard.html', context)
    return {}


def conn_sql(request):
    try:
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=projet-affluence-cinema-mlrecap.database.windows.net;'
            'DATABASE=BDD_boxoffice;'
            'UID=project_affluence_cinema;'
            'PWD=*Boxoffice1;' 
        )
        # Calculer les dates du prochain mercredi et du mardi suivant
        today = datetime.today()
        next_wednesday = today + timedelta(days=(2 - today.weekday()) % 7)
        next_tuesday = next_wednesday + timedelta(days=6)
        
        # Convertir les dates en format de chaîne pour la requête SQL
        next_wednesday_str = next_wednesday.strftime('%Y-%m-%dT%H:%M:%S.%f')
        next_tuesday_str = next_tuesday.strftime('%Y-%m-%dT%H:%M:%S.%f')
        query = f"SELECT * FROM [dbo].[actu_scrap_poster1] WHERE [date] BETWEEN '{next_wednesday_str}' AND '{next_tuesday_str}'"
        # query = "SELECT TOP (10) * FROM [dbo].[actualisation_scrap1]"
        data_frame = pd.read_sql_query(query, connection)
        
        connection.close()
        
        return {'data_frame': data_frame, 'is_empty': data_frame.empty}
    except Exception as e:
        return {'error_message': str(e)}


def combined_view(request):
    
        # Récupérer les données des deux vues
        dashboard_view_data = dashboard_view(request)
        conn_sql_data = conn_sql(request)


        # Combinez les données
        combined_data = {
            'data_frame': conn_sql_data['data_frame'],
            'is_empty': conn_sql_data['is_empty'],
            'dashboard_view_data': dashboard_view_data  # Ajoutez d'autres clés du dictionnaire de votre fonction 'evaluation' si nécessaire
        }


        return render(request, 'dashboard.html', combined_data)