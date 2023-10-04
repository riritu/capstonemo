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
    
class Unit(models.Model):
    unit_name = models.CharField(max_length=255)
    price = models.FloatField(max_length=255)
    unit_avail = models.BooleanField(default=True)
    num_book = models.IntegerField()

    def __str__(self):
        return self.unit_name



class Tenants(AbstractUser):
    tent_name = models.CharField(max_length=255)
    tent_uname = models.CharField(max_length=255)
    unit_type = models.CharField(max_length=255)
    tent_pnum = models.CharField(max_length=255)
    tent_emel = models.CharField(max_length=255, validators=[EmailValidator()], default='custom@example.com')
    tent_pword = models.CharField(max_length=255)
    
    # Add related_name attributes to fields causing clashes
    
    def check_password(self, raw_password):
        # Validate the password using Django's built-in function
        return check_password(raw_password, self.password)
    
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