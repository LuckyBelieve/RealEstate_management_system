from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from estates.models import Estate

class RentalAgreement(models.Model):
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, related_name='rental_agreements')
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'client'}, related_name='agreements')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'admin'}, related_name='owned_agreements')
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('terminated', 'Terminated'), ('pending', 'Pending')], default='pending')

    def __str__(self):
        return f"Rental Agreement for {self.estate.property_name} - {self.tenant.username}"
