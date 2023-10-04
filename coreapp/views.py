from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import Tenantform 
from django.views.decorators.csrf import csrf_protect
from .models import Tenants  # Import your Tenant model
from django.db import IntegrityError
from django.core.exceptions import MultipleObjectsReturned
 # Import your custom form

def home(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pword = request.POST.get('pass')
        # Attempt to authenticate as a regular user
        try:
            tenant = Tenants.objects.get(username=uname)
        except MultipleObjectsReturned:  
            messages.error(request, "Authentication failed. Please check your credentials.")
        except Tenants.DoesNotExist:
            tenant = None
        if tenant is not None and tenant.check_password(pword):
            login(request, tenant, backend='coreapp.backend.TenantBackend')
            return render(request, 'tnt_hom.html', {'username': uname})   # Pass the 
        # If tenant authentication fails, then check regular user authentication
        user = authenticate(request, username=uname, password=pword)
        if user is not None:
            login(request, user)
            return redirect('admins')

        # Authentication failed for both regular user and tenant
        messages.error(request, "Authentication failed. Please check your credentials.")
    return render(request, 'home.html')

def unit(request):  
    return render(request, 'unit.html')

def admins(request):  
    return render(request, 'admins.html')



def creacc(request):
    if request.method == 'POST':
        form = Tenantform(request.POST)
        if form.is_valid():
            # Extract the values from the form fields
            tent_name = form.cleaned_data['tent_name']
            uname = form.cleaned_data['tent_uname']  # Use the uname field for username
            unit_type = form.cleaned_data['unit_type']
            tent_pnum = form.cleaned_data['tent_pnum']
            tent_emel = form.cleaned_data['tent_emel']
            tent_pword = form.cleaned_data['tent_pword']

            try:
                # Create a new Tenantaccs instance
                tenant = Tenants.objects.create(
                    tent_name=tent_name,
                    username=uname,  # Assign the uname as the username
                    unit_type=unit_type,
                    tent_pnum=tent_pnum,
                    tent_emel=tent_emel,
                    password=tent_pword
                )
                messages.success(request, "Account created successfully.")
            except IntegrityError:
                # Handle the case where a duplicate username is detected
                messages.error(request, "A user with this username already exists.")
    else:
        form = Tenantform()
    return render(request, 'creacc.html', {'form': form})

def ad_hom(request):  
    return render(request, 'ad_hom.html')

def ad_tent(request):  
    return render(request, 'ad_tent.html')

def tnt_hom(request):  
    return render(request, 'tnt_hom.html')

def homepage(request):  
    return render(request, 'homepage.html')

