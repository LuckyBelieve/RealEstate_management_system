from django.urls import path
from . import views

urlpatterns = [
    path('properties/', views.property_list, name='property_list'),
    path('properties/details', views.property_detail, name='property_detail'),
]
