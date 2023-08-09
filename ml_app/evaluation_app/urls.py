
from django.urls import path
from . import views

urlpatterns = [
    path('evaluation/', views.evaluation, name='evaluation'),
]
