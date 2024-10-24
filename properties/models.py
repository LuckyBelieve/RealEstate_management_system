from django.db import models

class Property(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    property_type = models.CharField(max_length=50)  # Rent or Sale
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    square_feet = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='property_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

