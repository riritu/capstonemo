from django import forms
from .models import Payment, Booked, Tenants, Units, Issues

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

class Compform(forms.ModelForm):
    class Meta:
        model = Issues
        fields = ['name', 'issue', 'solution']

class Propform(forms.ModelForm):
    class Meta:
        model = Units
        fields = ['unit_type', 'unit_blt', 'unt_availability', 'unt_price']

    def clean_email(self):
        unit_blt = self.cleaned_data.get('unit_blt')
        if Units.objects.filter(unit_blt=unit_blt).exists():
            raise forms.ValidationError("This unit already exist.")
        return unit_blt

