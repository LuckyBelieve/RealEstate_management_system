# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView, LoginView, logout_view, login_page, register_page , dashboard

urlpatterns = [
    path('v1/register/', RegisterView.as_view(), name='register'),
    path('v1/login/', LoginView.as_view(), name='login'),
    path('v1/logout/', logout_view , name='logout'),
    path('login/', login_page, name='login_page'),
    path('register/', register_page, name='register_page'),
    path('dashboard/', dashboard, name='dashboard'),
]
