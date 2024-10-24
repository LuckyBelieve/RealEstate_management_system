from django.shortcuts import render
from .models import RentalAgreement
from django.contrib.auth.decorators import login_required

def rental_agreements(request):
    return render(request, 'rentals/rental_agreements.html', {'agreements': 10})

