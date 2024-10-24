from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from estates.forms import EstateForm
from users.models import User
from estates.models import Estate
# Create your views here.

def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            return redirect('estate_listings')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def estateListingView(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    
    user = request.user
    estates = Estate.objects.all()
    return render(request, 'estates/estates_listing.html',{'estates':estates,'user':user})


@login_required
@admin_only
def addEstateView(request):
    if request.method == 'POST':
        form = EstateForm(request.POST,request.FILES)

        if form.is_valid():
            form.save()
            return redirect('estate_listings')
    else:
        form = EstateForm()
    
    return render(request,'estates/estate_form.html',{'form':form})


@login_required
@admin_only
def updateEstateView(request,pk):
    currentEstate = get_object_or_404(Estate,pk=pk)

    if request.method == 'POST':
        form = EstateForm(request.POST,request.FILES,instance=currentEstate)

        if form.is_valid():
            form.save()
            return redirect('estate_listings')
    else:
        form = EstateForm(instance=currentEstate)

    return render(request, 'estates/estate_form.html',{'form':form})


@login_required
@admin_only
def deleteEstateView(request,pk):
    estateToBeDeleted = get_object_or_404(Estate, pk=pk)

    if request.method == 'POST':
        estateToBeDeleted.delete()
        return redirect('estate_listings')
    else:
        return redirect('estate_listings')


@login_required
def estateDetailView(request, pk):
    estate = get_object_or_404(Estate, pk=pk)
    return render(request, 'estates/estate_detail.html', {'estate': estate, 'user': request.user})