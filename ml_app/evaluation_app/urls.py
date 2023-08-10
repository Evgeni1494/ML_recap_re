
from django.urls import path
from . import views

urlpatterns = [
    path('evaluation/', views.combined_eval, name='combined_eval'),
]
