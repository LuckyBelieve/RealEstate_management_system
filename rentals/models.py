from django.db import models
from properties.models import Property
# from clients.models import Client

class RentalAgreement(models.Model):
    # client = models.ForeignKey(Client, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)  # Active, Terminated

    def __str__(self):
        return f"Rental Agreement for {self.property.name} by {self.client.user.username}"

class Payment(models.Model):
    rental_agreement = models.ForeignKey(RentalAgreement, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    status = models.CharField(max_length=20)  # Paid, Pending
