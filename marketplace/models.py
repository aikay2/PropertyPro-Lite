from django.db import models
from authentication.models import CustomUser

# Create your models here.

class Property(models.Model):
    STATUS_CHOICES = (
        ('sold', 'Sold'),
        ('available', 'Available')
    )
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status =  models.CharField(max_length=10, choices=STATUS_CHOICES)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address = models.TextField(max_length=75)
    type = models.CharField(max_length=20, help_text="e.g 2 bedroom, 3 bedroom, etc.")
    created_on = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.type} in {self.city}, {self.state} - {self.status} (${self.price})"
    
    
class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to='properties/')
    
    def __str__(self):
        return f"Image for {self.property.type} in {self.property.city} [${self.property.price}]"
    

class Flags(models.Model):
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    reason = models.CharField(max_length=15, help_text="e.g pricing, weird demands, etc.")
    description = models.TextField(max_length=40)
   
    def __str__(self):
       return f"Flag on {self.property_id} - [{self.reason}]"
    
