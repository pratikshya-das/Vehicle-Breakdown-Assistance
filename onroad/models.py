from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from .models import *
from django.dispatch import receiver #add this
from django.db.models.signals import post_save #add this
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime    

#DataFlair Models

class User(AbstractUser):
    is_mechanic = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    answer1 = models.CharField(max_length = 50, default='Enter your School friend name')


class UserReg(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class PasswordReset(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
   def __unicode__(self):
       return self.user

class Business(models.Model):
    pending = 'pending'
    approved = 'approved'
  
    loggeduser= models.CharField(max_length = 50)
    business = models.CharField(max_length = 50)
    mechanic = models.CharField(max_length = 50)
    service = models.CharField(max_length = 50)
    available=models.CharField(max_length = 50)
    address = models.TextField(max_length = 50)
    mobile = models.CharField(max_length = 10)
    locality = models.TextField(max_length = 50)
    status_CHOICES = [
        (pending, 'pending'),
        (approved, 'approved'),
       
    ]
   
    status = models.CharField(
        max_length=50,
        choices=status_CHOICES,
        default=pending)
    latitude=models.CharField(max_length = 20)
    lantitude=models.CharField(max_length = 20)
    city= models.CharField(max_length =50)
   
    def __str__(self):
       return self.business
class Feedback(models.Model):
  
    loggeduser= models.CharField(max_length = 50)
    
    name = models.CharField(max_length = 20)
    feedback = models.TextField(max_length = 100)
    feedcreateuser= models.CharField(max_length = 50)
    
    def __str__(self):
        return self


class Payment(models.Model):
  
    loggeduser= models.CharField(max_length = 50)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    Name = models.CharField(max_length = 20)
    Cardno = models.CharField(max_length = 14)
    Expirydate = models.DateField()
    CCV=models.CharField(max_length = 3)
    Amount=models.CharField(max_length = 10)
    payuser= models.CharField(max_length = 50)
    
    def __str__(self):
        return self