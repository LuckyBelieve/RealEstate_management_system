from django import forms
from .models import RentalAgreement

class RentalAgreementForm(forms.ModelForm):
    class Meta:
        model = RentalAgreement
        fields = ['start_date', 'end_date', 'monthly_rent', 'security_deposit']
        # Exclude fields that will be set automatically
        exclude = ['estate', 'tenant', 'owner', 'status']
