from django.urls import path
from . import views

urlpatterns = [
    path('agreements/', views.rental_agreements, name='rental_agreements'),
]
