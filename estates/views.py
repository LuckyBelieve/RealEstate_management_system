from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from estates.forms import EstateForm
from users.models import User
from django.contrib import messages
from estates.models import Estate
from rentalAgreements.models import RentalAgreement
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
from django.utils import timezone
# Create your views here.

def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            return redirect('estate_listings')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def estateListingView(request):
    user = request.user
    
    # If user is admin, show only their created estates
    if user.role == 'admin':
        estates = Estate.objects.filter(owner=user).select_related('owner')
    # If user is client, show all estates
    else:
        estates = Estate.objects.all().select_related('owner')

    return render(request, 'estates/estates_listing.html', {'estates': estates, 'user': user})


@login_required
@admin_only
def addEstateView(request):
    if request.method == 'POST':
        form = EstateForm(request.POST, request.FILES)

        if form.is_valid():
            estate = form.save(commit=False)  # Don't save to DB yet
            estate.owner = request.user       # Set the owner to current admin
            estate.save()                     # Now save to DB
            return redirect('estate_listings')
    else:
        form = EstateForm()
    
    return render(request, 'estates/estate_form.html', {'form': form})


@login_required
@admin_only
def updateEstateView(request, pk):
    # Get the estate and verify the current user is the owner
    currentEstate = get_object_or_404(Estate, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = EstateForm(request.POST, request.FILES, instance=currentEstate)

        if form.is_valid():
            form.save()
            return redirect('estate_listings')
    else:
        form = EstateForm(instance=currentEstate)

    return render(request, 'estates/estate_form.html', {'form': form})


@login_required
@admin_only
def deleteEstateView(request, pk):
    # Get the estate and verify the current user is the owner
    estateToBeDeleted = get_object_or_404(Estate, pk=pk, owner=request.user)

    if request.method == 'POST':
        estateToBeDeleted.delete()
        return redirect('estate_listings')
    else:
        return redirect('estate_listings')


@login_required
def estateDetailView(request, pk):
    estate = get_object_or_404(Estate, pk=pk)
    context = {
        'estate': estate,
        'user': request.user,
        'is_owner': request.user == estate.owner
    }
    return render(request, 'estates/estate_detail.html', context)


@login_required
def dashboard_view(request):
    if request.user.role == 'admin':
        # Get admin's estates and agreements
        estates = Estate.objects.filter(owner=request.user)
        agreements = RentalAgreement.objects.filter(owner=request.user)
        
        context = {
            'total_estates': estates.count(),
            'available_estates': estates.filter(status='available').count(),
            'rented_estates': estates.filter(status='rented').count(),
            'total_agreements': agreements.count(),
            'active_agreements': agreements.filter(status='active').count(),
            'pending_agreements': agreements.filter(status='pending').count(),
            'recent_estates': estates.order_by('-created_at')[:5],
            'recent_agreements': agreements.order_by('-created_at')[:5],
            'is_admin': True
        }
    
    elif request.user.role == 'client':
        # Get client's agreements and related estates
        agreements = RentalAgreement.objects.filter(tenant=request.user)
        
        context = {
            'total_agreements': agreements.count(),
            'active_agreements': agreements.filter(status='active').count(),
            'pending_agreements': agreements.filter(status='pending').count(),
            'recent_agreements': agreements.order_by('-created_at')[:5],
            'is_admin': False
        }
    
    else:
        messages.error(request, "You don't have permission to access the dashboard.")
        return redirect('home')

    return render(request, 'estates/dashboard.html', context)