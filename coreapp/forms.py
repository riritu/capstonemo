from django import forms
from .models import Tenants
from .models import Booked
from .models import Payment

class Tenantform(forms.ModelForm):
    class Meta:
        model = Tenants
        fields = ['tent_name', 'tent_uname', 'unit_type', 'tent_emel', 'tent_pnum', 'tent_pword']


class Requestform(forms.ModelForm):
    class Meta:
        model = Booked
        fields = ['name', 'unit', 'pnum', 'date', 'emel', 'bookt']

class Paymentform(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['name', 'unit', 'mop', 'date', 'amount', 'ref', 'tenant']
