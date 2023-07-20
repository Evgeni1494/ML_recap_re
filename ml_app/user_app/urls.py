from django.urls import path 
from . import views
from . import forms
urlpatterns = [
    path('signup/', views.SignupPage.as_view(), name='signup'),
    path('login/', views.SignupPage.as_view(), name='login')
]