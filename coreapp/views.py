from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import Paymentform, Propform, Requestform, Tenantform,Compform
from django.views.decorators.csrf import csrf_protect
from .models import Tenants, Booked, Payment, Units, Issues
from django.core.mail import send_mail
from django.db import IntegrityError
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Sum
from datetime import datetime
from calendar import monthrange
from django.http import HttpResponse
from django.conf import settings
from django.http import JsonResponse
import locale

 # Import your custom form


def user_logout(request):
    logout(request)
    return redirect('home')  

def delete_unit(request, unit_id):
    try:
        unit = Units.objects.get(pk=unit_id)
        unit.delete()
        return JsonResponse({'success': True})
    except Units.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Unit not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
def home(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pword = request.POST.get('pass')
        try:
            tenant = Tenants.objects.get(username=uname)
        except MultipleObjectsReturned:  
            messages.error(request, "Authentication failed. Please check your credentials.")
        except Tenants.DoesNotExist:
            tenant = None
        if tenant is not None and tenant.check_password(pword):
            login(request, tenant, backend='coreapp.backend.TenantBackend')
            return redirect(f'/tnt_hom/?username={uname}', )  # Include the username in the URL   return redirect('tnt_hom', username=uname)  
            return render(request, 'tnt_hom.html', {'username': uname})   # Pass the  
        user = authenticate(request, username=uname, password=pword)
        if user is not None:
            login(request, user)
            return redirect('admins')

        messages.error(request, "Authentication failed. Please check your credentials.")
    return render(request, 'home.html')

def unit(request):  
    return render(request, 'unit.html')


def creacc(request):
    messages.clear()
    if request.method == 'POST':
        form = Tenantform(request.POST)
        if form.is_valid():
            tent_name = form.cleaned_data['tent_name']
            uname = form.cleaned_data['tent_uname'] 
            unit_type = form.cleaned_data['unit_type']
            tent_pnum = form.cleaned_data['tent_pnum']
            tent_emel = form.cleaned_data['tent_emel']
            tent_pword = form.cleaned_data['tent_pword']
            
            try:
                tenant = Tenants.objects.create(
                    tent_name=tent_name,
                    username=uname,  
                    unit_type=unit_type,
                    tent_pnum=tent_pnum,
                    tent_emel=tent_emel,
                    password=tent_pword
                )
                messages.success(request, "Account Created.")
            except IntegrityError:
                messages.error(request, "Invalid Input.")
    else:
        form = Tenantform()
    return render(request, 'creacc.html', {'form': form})


def ad_hom(request):  
    locale.setlocale(locale.LC_ALL, 'en_PH.UTF-8')
    book = Booked.objects.all().order_by('date')
    tent = Tenants.objects.all().order_by('tent_name')
    prop = Units.objects.all()

    total_profit = calculate_total_profit()
    formatted_total_profit = locale.currency(total_profit, grouping=True)
    num_tenants = tent.count()

    reqs = {
        'total_profit': formatted_total_profit,
        'Booked': book,
        'Tenants': tent,
        'Prop': prop,
        'NumTenants': num_tenants  # Add the count of tenants to the context dictionary
    }

    return render(request, 'ad_hom.html', reqs)

def calculate_total_profit():
    total_profit = Payment.objects.aggregate(Sum('amount'))['amount__sum']
    return total_profit

def ad_tent(request):  
    queryset = Tenants.objects.all()

    context = {
        'Tenants': queryset
    }

    return render(request, 'ad_tent.html', context)


def homepage(request):  
    return render(request, 'homepage.html')

def contact(request):  
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        unit_type = request.POST.get('unit')
        comment = request.POST.get('comment')
        move_in_date = request.POST.get('date')

        subject = 'New Contact Form Submission'
        message = f'Name: {name}\nEmail: {email}\nPhone: {phone}\nUnit Type: {unit_type}\nComment: {comment}\nMove-in Date: {move_in_date}'
        from_email = settings.EMAIL_HOST_USER 
        recipient_list = ['robertofaner55@gmail.com']

        send_mail(subject, message, from_email, recipient_list)

        return HttpResponse('Form submitted successfully. Thank you!')
    return render(request, 'contact.html')

def vtour(request):  
    return render(request, 'vtour.html')

def amnts(request):  
    return render(request, 'amnts.html')

def book(request):  
    if request.method == 'POST':
        form = Requestform(request.POST)
        if form.is_valid():
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
    return render(request, 'booking.html', {'form': form})

def comp(request):  
    return render(request, 'comp.html')


def req(request):  
    book = Booked.objects.all().order_by('name')
    queryset = Booked.objects.all()

    reqy = {
        'Booked': book
    }
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'approve':
            subject = 'Booking Approved'
            message = 'Your booking has been approved.'
            from_email = 'admin@example.com'
            recipient_list = ['recipient@example.com']

            send_mail(subject, message, from_email, recipient_list)


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
            name = form.cleaned_data['name']
            date = form.cleaned_data['date']
            unit = form.cleaned_data['unit']
            ref = form.cleaned_data['ref']
            mop = form.cleaned_data['mop']
            amount = form.cleaned_data['amount']
            tenant_id = form.cleaned_data['tenant']
            try:
                Payment = Payment.objects.create(
                    name=name,
                    date=date,
                    unit=unit,
                    ref=ref,
                    mop=mop,
                    amount=amount,
                    tenant=tenant_id  
                                                    )
                messages.success(request, "Payment Submitted.")

            except IntegrityError:
                messages.error(request, "Invalid Input.")
        else:
            messages.error(request, "Invalid Form Data.")
    else:
        form = Paymentform()

    return render(request, 'payment.html', {'form': form, **context})

def prop(request):  
    queryset = Units.objects.all()
    context = {
        'Units': queryset
    }
    if request.method == 'POST':       
        form = Propform(request.POST)       
        if form.is_valid():
            untp = form.cleaned_data['unit_type']
            blt = form.cleaned_data['unit_blt'] 
            avail = form.cleaned_data['unt_availability']
            prc = form.cleaned_data['unt_price']

            try:
                units = Units.objects.create(
                    unit_type=untp,
                    unit_blt=blt,  
                    unt_availability=avail,
                    unt_price=prc
                )
                messages.success(request, "Unit Created.")
                print('dsad')
            except IntegrityError:
                messages.error(request, "Invalid Input.")
                print('sdsad')
        else:
            messages.error(request, "Invalid Form Data.")
            print('dasda')

    else:
        form = Tenantform()
    return render(request, 'property.html', {'form': form, **context})

def rep(request):  
    if request.method == 'GET':
        start_year = int(request.GET.get('start_year', datetime.now().year))
        start_month = int(request.GET.get('start_month', datetime.now().month))
        end_year = int(request.GET.get('end_year', datetime.now().year))
        end_month = int(request.GET.get('end_month', datetime.now().month))

        # Get the first and last day of the start month
        _, last_day_start = monthrange(start_year, start_month)
        start_date = datetime(start_year, start_month, 1).date()
        end_date = datetime(end_year, end_month, last_day_start).date()

        # Query the Payment model to get the total amount for the selected range of months
        total_amount = Payment.objects.filter(date__range=(start_date, end_date)).aggregate(Sum('amount'))['amount__sum']

        # Prepare data to pass to the template
        report_period = f'{start_date.strftime("%B %Y")} - {end_date.strftime("%B %Y")}'
        monthly_sums = {
            report_period: total_amount or 0
        }

        # Get a list of years for the dropdown
        years = [start_year, end_year]  # You can customize this based on your data

        # Get a list of months for the dropdowns
        months = [(str(i), datetime(2000, i, 1).strftime('%B')) for i in range(1, 13)]

        return render(request, 'ad_rep.html', {
            'monthly_sums': monthly_sums,
            'start_year': start_year,
            'start_month': start_month,
            'end_year': end_year,
            'end_month': end_month,
            'report_period': report_period,
            'years': years,
            'months': months
        })
    else:
        # Handle other HTTP methods if necessary
        pass
    
@login_required(login_url='home')  
def admins(request):  
    return render(request, 'admins.html')

@login_required(login_url='home') 
def tnt_hom(request): 
    username = request.GET.get('username', '') 
    print("Received username:", username)  # Add this line for debugging 
    tenant_data = Tenants.objects.filter(username=username).first() 
    if tenant_data:
            tenant_name = tenant_data.tent_name
    else:
        tenant_name = None
    context = {
          'username': username,
         'tenant_name': tenant_name,
    }
    if request.method == 'POST':
        form = Compform(request.POST)
        if form.is_valid():
            nem = form.cleaned_data['name']
            isyu = form.cleaned_data['issue']
            sagot = form.cleaned_data['solution']
            try:
                tissue = Issues.objects.create(
                    name=nem,
                    issue=isyu,
                    solution=sagot
                )
                messages.success(request, "Complaint submitted successfully.")
            except IntegrityError:
                messages.error(request, "Invalid Input.")
        else:
            messages.error(request, "Invalid Form Data.")
    else:
        form = Compform()

    return render(request, 'tnt_hom.html', {'form': form, **context})


def foot(request):  
    return render(request, 'footer.html')





