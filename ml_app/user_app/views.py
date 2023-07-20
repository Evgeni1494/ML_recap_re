from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserCreationFormCustom




class SignupPage(CreateView):
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    form_class = UserCreationFormCustom
    
    
