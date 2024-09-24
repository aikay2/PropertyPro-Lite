from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        user = self.create_user(email, password, **extra_fields)

        if extra_fields.get('is_agent'):
            Agent.objects.create(user=user) 
        elif extra_fields.get('is_customer'):
            Customer.objects.create(user=user) 

        return user
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('agent', 'Agent'),
        ('customer', 'Customer'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=False, blank=False)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=45)
    address = models.TextField(max_length=75)
    phoneNumber = PhoneNumberField(null=False, blank=False, unique=False)
    created_on = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'address', 'phoneNumber', 'user_type']
    
    objects = CustomUserManager()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not hasattr(self, 'agent_profile') and self.user_type == 'agent':
            Agent.objects.create(user=self)
        elif not hasattr(self, 'customer_profile') and self.user_type == 'customer':
            Customer.objects.create(user=self)
            
    
    def __str__(self):
        return self.username

class Agent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, related_name='agent_profile')
    is_agent = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Agent: {self.user.username}"
    
class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, related_name='customer_profile')
    is_customer = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Customer: {self.user.username}"
    
@receiver(post_delete, sender=Agent)
def delete_user_on_agent_delete(sender, instance, **kwargs):
    user = instance.user
    user.delete()
    
@receiver(post_delete, sender=Customer)
def delete_user_on_agent_delete(sender, instance, **kwargs):
    user = instance.user
    user.delete()