from django.urls import path
from .views import (
    estateListingView,
    addEstateView,
    deleteEstateView,
    estateDetailView,
    updateEstateView
)

urlpatterns = [
    path('estates/', estateListingView, name="estate_listings"),  
    path('v1/estates/create/', addEstateView, name='add_estate'),
    path('v1/estates/update/<int:pk>/', updateEstateView, name='update_estate'),
    path('v1/estates/delete/<int:pk>/', deleteEstateView, name='delete_estate'),
    path('v1/estates/details/<int:pk>/', estateDetailView, name='estate_detail'),
]
