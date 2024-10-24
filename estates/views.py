from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from estates.forms import EstateForm
from users.models import User
from estates.models import Estate
# Create your views here.

def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            return HttpResponseForbidden("You are not authorized to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
def estate_listing(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    
    user = request.user
    estates = Estate.objects.all()
    return render(request, 'estates/estates_listing.html',{'estates':estates,'user':user})


@login_required
@admin_only
def addEstateView(request):
    if request.method == 'POST':
        form = EstateForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('estates_listing')
    else:
        form = EstateForm()
    
    return render(request,'estates/estate_form.html',{'form':form})


@login_required
@admin_only
def updateEstateView(request,pk):
    currentEstate = get_object_or_404(Estate,pk=pk)

    if request.method == 'POST':
        form = EstateForm(request.POST,instance=currentEstate)

        if form.is_valid():
            form.save()
            return redirect('estates_listing')
    else:
        form = EstateForm(instance=currentEstate)

    return render(request, 'estates/estate_form.html',{'form':form})


@login_required
@admin_only
def deleteEstateView(request,pk):
    estateToBeDeleted = get_object_or_404(Estate, pk=pk)

    if request.method == 'POST':
        estateToBeDeleted.delete()
        return redirect('estates_listing')
    
    return render(request,'estates/deleteEstate.html',{'estate':estateToBeDeleted})