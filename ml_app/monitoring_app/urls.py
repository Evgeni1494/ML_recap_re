
from django.urls import path
from . import views

urlpatterns = [
    path('monitoring/', views.combined_view, name='combined_view'),
    # path('test_sql/', views.test_sql, name='test_sql'),
]
