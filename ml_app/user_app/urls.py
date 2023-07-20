from django.urls import path
from .views import login_view, signup_view, dashboard_view, logout_view

app_name = 'user_app'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
]