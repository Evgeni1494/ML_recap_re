from django.urls import path
from .views import login_view, signup_view,logout_view,reset_password,reset_password_confirm, combined_view_scrap,scrap

app_name = 'user_app'

urlpatterns = [
    path('', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('dashboard/', combined_view_scrap, name='combined_view_scrap'),
    path('logout/', logout_view, name='logout'),
    path('reset_password/', reset_password, name='reset_password'),
    path('reset_password/<str:reset_token>/',reset_password_confirm, name='reset_password_confirm'),
    path('scrap/', scrap, name='scrap'),
]


