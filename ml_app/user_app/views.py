from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout


def logout_view(request):
    django_logout(request)
    return redirect('user_app:login')


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            # Effectuer des actions supplémentaires (par exemple, envoyer un e-mail de confirmation, rediriger vers la page de connexion, etc.)
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


@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')



