from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.contrib.auth.hashers import make_password, check_password
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.db import transaction

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
    APPROVAL_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    )
    bookt = models.CharField(max_length=255,default='duration')
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    pnum = models.CharField(max_length=20)  
    date = models.DateField(max_length=255)
    emel = models.CharField(max_length=255, validators=[EmailValidator()], default='custom@example.com')    
    approval_status = models.CharField(max_length=20, choices=APPROVAL_CHOICES, default='pending')

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
    assigned_unit = models.ForeignKey(Units, on_delete=models.SET_NULL, null=True, blank=True)
    
    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the instance is being created (not updated)
            # Check if the chosen unit is available
            try:
                booked_unit = Units.objects.get(unit_type=self.unit_type, unt_availability=True)  # Get the matching unit
                # Check if the unit is not already assigned to another tenant
                if not Tenants.objects.filter(assigned_unit=booked_unit).exists():
                    booked_unit.unt_availability = False
                    booked_unit.save()
                    self.assigned_unit = booked_unit
                else:
                    # Handle the case where the unit is already assigned to another tenant
                    raise Exception("Selected unit is already assigned to another tenant.")
            except Units.DoesNotExist:
                # Handle the case where no matching unit is found
                raise Exception("No available unit found with the specified type.")
            except Exception as e:
                # Handle other exceptions if necessary
                raise Exception("Error occurred while processing the request: {}".format(str(e)))

            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    # ... other methods ...

    def delete(self, *args, **kwargs):
        # Check if the tenant has an associated booked unit
        if Units.objects.filter(unit_type=self.unit_type, unt_availability=True).exists():                # If the unit is available, set its approval status to 'unavailable'
            booked_unit = Units.objects.get(unit_type=self.unit_type, unt_availability=True)
            booked_unit.unt_availability = False
            booked_unit.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.tent_name

User.groups.field.remote_field.related_name = 'user_groups'
User.user_permissions.field.remote_field.related_name = 'user_permissions'
Tenants.groups.field.remote_field.related_name = 'tenant_groups'
Tenants.user_permissions.field.remote_field.related_name = 'tenant_permissions'

