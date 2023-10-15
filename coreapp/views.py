from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import Tenantform 
from .forms import Requestform
from .forms import Paymentform
from django.views.decorators.csrf import csrf_protect
from .models import Tenants  # Import your Tenant model
from .models import Booked  # Import your Tenant model
from .models import Payment  # Import your Tenant model
from django.core.mail import send_mail
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
                messages.success(request, "Booking submitted.")
            except IntegrityError:
                # Handle the case where a duplicate username is detected
                messages.error(request, "Invalid Input.")
    else:
        form = Tenantform()
    return render(request, 'creacc.html', {'form': form})

def ad_hom(request):  
    return render(request, 'ad_hom.html')

def ad_tent(request):  
    queryset = Tenants.objects.all()
    
    # Pass the queryset to the template context
    context = {
        'Tenants': queryset
    }
    return render(request, 'ad_tent.html', context)

def tnt_hom(request):  
    return render(request, 'tnt_hom.html')

def homepage(request):  
    return render(request, 'homepage.html')

def contact(request):  
    return render(request, 'contact.html')

def vtour(request):  
    return render(request, 'vtour.html')

def amnts(request):  
    return render(request, 'amnts.html')

def book(request):  
    if request.method == 'POST':
        form = Requestform(request.POST)
        if form.is_valid():
            #   Extract the values from the form fields
            nem = form.cleaned_data['name']
            emel= form.cleaned_data['emel']
            unit = form.cleaned_data['unit']
            pnum = form.cleaned_data['pnum']
            date = form.cleaned_data['date']
            bookt = form.cleaned_data['bookt']
            try:
                book = Booked.objects.create(
                    name = nem,
                    emel = emel,
                    unit= unit,
                    pnum = pnum,
                    date = date,
                    bookt = bookt
                )
                messages.success(request, "Booking Submit.")
            except IntegrityError:
                messages.error(request, "Invalid Input.")
    else:
        form = Requestform()
    return render(request, 'homepage.html', {'form': form})

def comp(request):  
    return render(request, 'comp.html')


def req(request):  
    queryset = Booked.objects.all()

    # Pass the queryset to the template context
    reqy = {
        'Booked': queryset
    }
    # Sending an email
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'approve':
            # Send email logic
            subject = 'Booking Approved'
            message = 'Your booking has been approved.'
            from_email = 'admin@example.com'
            recipient_list = ['recipient@example.com']

            send_mail(subject, message, from_email, recipient_list)

            # Other approval logic here

        elif action == 'decline':
            messages.error(request, "Invalid Input.")


    return render(request, 'ad_req.html', reqy)


def nav(request):  
    return render(request, 'navbar.html')

def pay(request):  
    return render(request, 'payment.html')

def pay(request):
    username = request.GET.get('username', '')
    tenant = Tenants.objects.get(username=username)
    context = {'username': username, 'tenant_id': tenant.id}
    if request.method == 'POST':
        form = Paymentform(request.POST)
        if form.is_valid():
            # Extract the values from the form fields
            name = form.cleaned_data['name']
            date = form.cleaned_data['date']
            unit = form.cleaned_data['unit']
            ref = form.cleaned_data['ref']
            mop = form.cleaned_data['mop']
            amount = form.cleaned_data['amount']
            tenant_id = form.cleaned_data['tenant']
            try:
                book = Payment.objects.create(
                    name=name,
                    date=date,
                    unit=unit,
                    ref=ref,
                    mop=mop,
                    amount=amount,
                    tenant=tenant_id  # Use tenant.id as the foreign key
                                                    )
                messages.success(request, "Payment Submitted.")

            except IntegrityError:
                messages.error(request, "Invalid Input.")
        else:
            # Form is not valid, return the form back to the template with errors
            messages.error(request, "Invalid Form Data.")
    else:
        form = Paymentform()

    # Pass both context and form separately
    return render(request, 'payment.html', {'form': form, **context})
 