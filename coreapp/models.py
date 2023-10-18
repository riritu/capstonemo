from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.contrib.auth.hashers import make_password, check_password
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

class Admin(models.Model):
    uname = models.CharField(max_length=255)
    pword = models.CharField(max_length=255)
    def __str__(self):
        return self.uname
    
    
class Issues(models.Model):
    name = models.CharField(max_length=255)
    issue = models.CharField(max_length=255)
    solution = models.CharField(max_length=255)

class Units(models.Model):
    unit_type = models.CharField(max_length=255)
    unit_blt = models.CharField(max_length=255, default='location')
    unt_price = models.FloatField()
    unt_availability = models.BooleanField(default=True) 

    def availability_display(self):
        return "Vacant" if self.unt_availability else "Occupied"
    
    def __str__(self):
        return self.unit_type

class Booked(models.Model):
    bookt = models.CharField(max_length=255,default='duration')
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    pnum = models.CharField(max_length=20)  
    date = models.DateField(max_length=255)
    emel = models.CharField(max_length=255, validators=[EmailValidator()], default='custom@example.com')    

class Payment(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    ref = models.IntegerField()
    mop = models.CharField(max_length=255)  
    unit = models.CharField(max_length=255)
    date = models.DateField(max_length=255, default='date')
    tenant = models.ForeignKey('Tenants', on_delete=models.CASCADE)  # Foreign key relationship

class Tenants(AbstractUser):
    tent_name = models.CharField(max_length=255)
    tent_uname = models.CharField(max_length=255)
    unit_type = models.CharField(max_length=255)
    tent_pnum = models.CharField(max_length=20)  
    tent_emel = models.EmailField(max_length=255, validators=[EmailValidator()], default='custom@example.com')
    tent_pword = models.CharField(max_length=255)

    # Add related_name attributes to fields causing clashes
    
    def save(self, *args, **kwargs):
        # Hash the password before saving, but only if it's a new instance
        if not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tent_name

User.groups.field.remote_field.related_name = 'user_groups'
User.user_permissions.field.remote_field.related_name = 'user_permissions'
Tenants.groups.field.remote_field.related_name = 'tenant_groups'
Tenants.user_permissions.field.remote_field.related_name = 'tenant_permissions'

