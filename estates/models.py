from django.db import models
from django.conf import settings
from users.models import User

class Estate(models.Model):
    property_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    # Use the custom User model
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='estates')
    property_type = models.CharField(max_length=50, choices=[('House', 'House'), ('Apartment', 'Apartment')])
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Add the property image field
    property_image = models.ImageField(upload_to='property_images/', blank=True, null=True)
    
    @property
    def is_available(self):
        """Check if the estate is available for rent"""
        return not self.rental_agreements.filter(status='active').exists()

    @property
    def current_agreement(self):
        """Get the current active rental agreement if any"""
        return self.rental_agreements.filter(status='active').first()

    def __str__(self):
        return self.property_name



