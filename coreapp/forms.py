from django import forms
from .models import Tenants
from .models import Books

class Tenantform(forms.ModelForm):
    class Meta:
        model = Tenants
        fields = ['tent_name', 'tent_uname', 'unit_type', 'tent_emel', 'tent_pnum', 'tent_pword']


class Requestform(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['name', 'unit', 'pnum', 'date', 'emel']