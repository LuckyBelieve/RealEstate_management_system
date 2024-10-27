from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from estates.models import Estate
from rentalAgreements.models import RentalAgreement
from .forms import RentalAgreementForm

@login_required
def create_rental_agreement(request, estate_id):
    estate = get_object_or_404(Estate, id=estate_id)
    
    # Check if the user is a client
    if request.user.role != 'client':
        messages.error(request, "Only clients can create rental agreements.")
        return redirect('estate_detail', estate_id=estate_id)

    if request.method == 'POST':
        form = RentalAgreementForm(request.POST)
        if form.is_valid():
            rental_agreement = form.save(commit=False)
            rental_agreement.estate = estate
            rental_agreement.tenant = request.user
            rental_agreement.owner = estate.owner  # Assuming the estate has an owner field
            rental_agreement.status = 'pending'  # Set initial status to pending
            rental_agreement.save()
            messages.success(request, "Rental agreement created successfully. Waiting for owner approval.")
            return redirect('rental_agreement_detail', agreement_id=rental_agreement.id)
    else:
        form = RentalAgreementForm()

    return render(request, 'rental_agreements/create_agreement.html', {'form': form, 'estate': estate})


@login_required
def update_rental_agreement(request, agreement_id):
    rental_agreement = get_object_or_404(RentalAgreement, id=agreement_id)
    
    # Check if the user is the owner of the estate
    if request.user != rental_agreement.owner or request.user.role != 'admin':
        messages.error(request, "Only the owner of the estate can update the rental agreement.")
        return redirect('rental_agreement_detail', agreement_id=agreement_id)

    if request.method == 'POST':
        form = RentalAgreementForm(request.POST, instance=rental_agreement)
        if form.is_valid():
            updated_agreement = form.save(commit=False)
            
            # Check if status is being changed to 'active'
            if updated_agreement.status == 'active' and rental_agreement.status != 'active':
                updated_agreement.activate()
                messages.success(request, "Rental agreement has been activated.")
            else:
                updated_agreement.save()
                messages.success(request, "Rental agreement updated successfully.")
            
            return redirect('rental_agreement_detail', agreement_id=agreement_id)
    else:
        form = RentalAgreementForm(instance=rental_agreement)

    context = {
        'form': form,
        'agreement': rental_agreement
    }
    return render(request, 'rental_agreements/update_agreement.html', context)


@login_required
def update_rental_agreement_status(request, agreement_id):
    rental_agreement = get_object_or_404(RentalAgreement, id=agreement_id)
    
    # Check if the user is the owner of the estate and an admin
    if request.user != rental_agreement.owner or request.user.role != 'admin':
        messages.error(request, "Only the owner of the estate can update the rental agreement status.")
        return redirect('rental_agreement_detail', agreement_id=agreement_id)

    if request.method == 'POST':
        form = RentalAgreementStatusForm(request.POST, instance=rental_agreement)
        if form.is_valid():
            new_status = form.cleaned_data['status']
            
            if new_status == 'active':
                rental_agreement.activate()
                messages.success(request, "Rental agreement has been activated.")
            elif new_status == 'terminated':
                rental_agreement.terminate()
                messages.success(request, "Rental agreement has been terminated.")
            elif new_status == 'expired':
                rental_agreement.expire()
                messages.success(request, "Rental agreement has been marked as expired.")
            else:
                rental_agreement.status = new_status
                rental_agreement.save()
                messages.success(request, f"Rental agreement status updated to {new_status}.")
            
            return redirect('rental_agreement_detail', agreement_id=agreement_id)
    else:
        form = RentalAgreementStatusForm(instance=rental_agreement)

    context = {
        'form': form,
        'agreement': rental_agreement
    }
    return render(request, 'rental_agreements/update_agreement_status.html', context)


@login_required
def rental_agreement_detail(request, agreement_id):
    rental_agreement = get_object_or_404(RentalAgreement, id=agreement_id)

    # Ensure only admin or tenant involved in the agreement can view it
    if request.user != rental_agreement.owner and request.user != rental_agreement.tenant:
        messages.error(request, "You don't have permission to view this rental agreement.")
        return redirect('home')

    return render(request, 'rental_agreements/agreement_detail.html', {'agreement': rental_agreement})

@login_required
def delete_rental_agreement(request, agreement_id):
    rental_agreement = get_object_or_404(RentalAgreement, id=agreement_id)

    # Ensure only the owner can delete the agreement
    if request.user != rental_agreement.owner or request.user.role != 'admin':
        messages.error(request, "Only the owner of the estate can delete the rental agreement.")
        return redirect('rental_agreement_detail', agreement_id=agreement_id)

    if request.method == 'POST':
        estate_id = rental_agreement.estate.id
        rental_agreement.delete()
        messages.success(request, "Rental agreement has been deleted successfully.")
        return redirect('estate_detail', estate_id=estate_id)

    return render(request, 'rental_agreements/delete_agreement.html', {'agreement': rental_agreement})