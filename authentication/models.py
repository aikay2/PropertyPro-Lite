from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('agent', 'Agent'),
        ('customer', 'Customer'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address = models.TextField(max_length=75)
    phoneNumber = PhoneNumberField(null=False, blank=False, unique=False)
    created_on = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'address', 'phoneNumber']
    
    def __str__(self):
        return self.username

class Agent(CustomUser):
    is_agent = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Agent: {self.username}"
    

class Customer(CustomUser):
    is_customer = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Customer: {self.username}"