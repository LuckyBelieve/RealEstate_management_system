from django.shortcuts import render, get_object_or_404
from .models import Property

def property_list(request):
    return render(request, 'properties/property_detail.html',{'properties':"property"})

def property_detail(request):
    return render(request, 'properties/property_detail.html')

