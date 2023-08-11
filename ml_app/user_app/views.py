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
import subprocess


def send_email_function():
    """
    Envoie un e-mail avec un sujet et un contenu définis à une liste de destinataires.
    """
    subject = 'Sujet de l\'e-mail'
    message = 'Contenu du message de l\'e-mail'
    from_email = 'django.nostradamus@gmail.com'  # Utilisez l'adresse Gmail que vous avez configurée dans votre fichier settings.py
    recipient_list = ['destinataire@example.com']  # Remplacez par l'adresse e-mail du destinataire

    send_mail(subject, message, from_email, recipient_list)


def logout_view(request):
    """
    Déconnecte l'utilisateur et le redirige vers la page de connexion.
    """
    django_logout(request)
    return redirect('user_app:login')


def signup_view(request):
    """
    Gère l'inscription d'un nouvel utilisateur. Si la requête est POST et le formulaire est valide, 
    enregistre le nouvel utilisateur. Sinon, affiche le formulaire d'inscription.
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            
    else:
        form = SignupForm()
    
    return render(request, 'signup.html', {'form': form})
    

def login_view(request):
    """
    Gère la connexion d'un utilisateur. Si la requête est POST et le formulaire est valide,
    authentifie l'utilisateur et le redirige vers le tableau de bord. Sinon, affiche le formulaire de connexion.
    """
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue {username} !")
                return redirect('user_app:combined_view')  # Assurez-vous d'avoir une URL nommée 'dashboard' dans votre application 'user_app'
            else:
                messages.error(request, "Identifiants invalides")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})



def reset_password(request):
    """
    Gère la demande de réinitialisation du mot de passe. Si un utilisateur avec l'adresse e-mail fournie existe, 
    génère un lien unique de réinitialisation du mot de passe et l'envoie à l'utilisateur.
    """
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
    """
    Gère la confirmation de la réinitialisation du mot de passe à l'aide d'un jeton unique.
    Si le jeton est valide, permet à l'utilisateur de définir un nouveau mot de passe.
    """
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




@login_required
def dashboard_view(request):

    # Récupérer les 10 films classés selon la prédiction du plus grand au plus petit
    # films = FilmData.objects.all().order_by('-prediction')[:10]
    # context = {'films': films}
    # return render(request, 'dashboard.html', context)
    return {}


def conn_sql(request):
    """
    Se connecte à une base de données Azure SQL et récupère les entrées de la table [dbo].[actualisation_scrap] 
    entre le prochain mercredi et le mardi suivant.
    """
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
        query = """
            SELECT *
            FROM [dbo].[actu_scrap_poster1]
            WHERE [date] BETWEEN ? AND ?
            ORDER BY evaluation_ML DESC
        """

        data_frame = pd.read_sql_query(query, connection, params=[next_wednesday_str, next_tuesday_str])

        
        connection.close()
        
        return {'data_frame': data_frame, 'is_empty': data_frame.empty}
    except Exception as e:
        return {'error_message': str(e)}

@login_required
def combined_view(request):
    if request.method == 'POST':
        subprocess.run(['scrapy', 'crawl', 'predictions11'])

    
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