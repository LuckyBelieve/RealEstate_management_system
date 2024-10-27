from django.db import models
from django.conf import settings

class Estate(models.Model):
    property_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    # Use the custom User model
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='estates')
    property_type = models.CharField(max_length=50, choices=[('House', 'House'), ('Apartment', 'Apartment')])
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Add the property image field
    property_image = models.ImageField(upload_to='property_images/', blank=True, null=True)
    
    @property
    def rental_agreements(self):
        """Get all rental agreements for this estate"""
        return RentalAgreement.objects.filter(estate=self)

    @property
    def is_available(self):
        """Check if the estate is available for rent"""
        active_agreements = RentalAgreement.objects.filter(
            estate=self, 
            status='active'
        )
        return not active_agreements.exists()

    @property
    def current_agreement(self):
        """Get the current active rental agreement if any"""
        return RentalAgreement.objects.filter(
            estate=self, 
            status='active'
        ).first()

    def __str__(self):
        return self.property_name



