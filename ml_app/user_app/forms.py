from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User  # Remplacez "User" par votre modèle d'utilisateur personnalisé si vous en avez un.
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    class Meta:
        model = User  # Remplacez "User" par votre modèle d'utilisateur personnalisé si vous en avez un.
        fields = ('username', 'password')