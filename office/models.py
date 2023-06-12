from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class LandLoad(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)

    logo = models.ImageField(upload_to='media/landloads')
    location = models.CharField(max_length=50)
    
class Tenant(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.user.email
class Office(models.Model):
    landload = models.ForeignKey(LandLoad, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    picture = models.ImageField(upload_to='media/office', null=True, blank=True)
    price = models.IntegerField(default=0)
    size = models.IntegerField(null=True, blank=True, default=0)
    is_available = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    
class OfficeBooking(models.Model):
    tenant = models.ForeignKey(Tenant, null=True, blank=True, on_delete=models.CASCADE)
    office =  models.ForeignKey(Office, null=True, blank=True, on_delete=models.CASCADE)
    CH = (("PENDING", "PENDING"), ("PAID" , "PAID"), ("CONTRACT OVER" , "CONTRACT OVER"))
    status = models.CharField(max_length=100, choices=CH, default="PENDING")

    def __str__(self):
        return self.tenant.user.username
    
class Invoice(models.Model):
    booking = models.ForeignKey(OfficeBooking, null=True, blank=True,  on_delete=models.CASCADE)
    issued_date = models.DateTimeField(auto_now=True)
    choice = (("Paid", "Paid"), ("Pending" , "Pending"))
    status = models.CharField(max_length=200, choices=choice, null=True, blank=True)        