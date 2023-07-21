from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, LoginForm
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


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




@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')




# 97523818-83d3-441c-8683-403f98ffcdb0
