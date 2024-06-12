from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from office.form import *


from django.http import HttpResponse
import requests
from django.contrib.auth.models import User
from django.template.loader import get_template
# from xhtml2pdf import pisa
from django.conf import settings
from io import BytesIO
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication



# # def upload_isu(request):
# #     action = "issuu.document.upload"
# #     apiKey = "hukprh6d967ap9w8mu41lgi79kk8fr36"
# #     name = "racing"
# #     title = "Race Cars"
    
# #     import hashlib
# #     sig = f"actionissuu.document.uploadapiKey{apiKey}nameracingtitleRace Cars"

# #     # Create an instance of the MD5 hash object
# #     md5_hash = hashlib.md5()

# #     # Update the hash object with the string
# #     md5_hash.update(sig.encode())

# #     # Get the hexadecimal representation of the hash
# #     md5_hash_hex = md5_hash.hexdigest()

# #     print(md5_hash_hex)

    
# #     context = {
# #         'sig': md5_hash_hex,
# #     }
# #     return render(request, 'upload.html', context)

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully signed in.')
            return redirect('office:dashboard')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.create_user(username=email, password=password, email=email)
            ld = LandLoad.objects.create(email=user.username, user = user)
            ld.save()
            messages.success(request, 'You have successfully signed up.')
            return redirect('office:signin')
        except Exception as e:
            messages.error(request, 'Error creating user: ' + str(e))

    return render(request, 'signup.html')

def logout_user(request):
    logout(request)
    return redirect('office:dashboard')

def home(request):
    
    return render(request, 'office/home.html')

@login_required
def dashboard(request):
    if request.user.is_superuser:
        offices_count = Office.objects.all().count()
        landloads_count = LandLoad.objects.all().count()
        tenants_count = Tenant.objects.all().count()
    else:
        offices_count = Office.objects.filter(landload=request.user.landload).count()
        landloads_count = LandLoad.objects.filter(user=request.user).count()
        tenants_count = Tenant.objects.filter(user=request.user).count()
        
    
    context = {'offices_count': offices_count, 'landloads_count':landloads_count, 'tenants_count':tenants_count}
    return render(request, 'office/dashboard.html', context)

@login_required
def bookings(request):
    form = OfficeBookingForm()
    if request.method == 'POST':
        form = OfficeBookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking added successfully')
            return redirect('office:bookings')
        else:
            form = OfficeBookingForm()
    
    if request.user.is_superuser:
        booking_list = OfficeBooking.objects.all()
    else:
        booking_list = OfficeBooking.objects.filter(office__landload  = request.user.landload)
        
    context = {'form': form, "booking_list": booking_list}
    return render(request, 'office/bookings.html', context)

def edit_booking(request, id):
    booking =  OfficeBooking.objects.get(id=id)
    form =  OfficeBookingForm(instance =  booking)
    if request.method == 'POST':
        form =  OfficeBookingForm(request.POST, instance =  booking)
        if form.is_valid():
            form.save()
            # data = form.save(commit=False)
            print(form.cleaned_data["status"])
            if form.cleaned_data["status"] == "CONTRACT OVER":
                # data.status = "CONTRACT OVER"
                # data.save()
                off = booking.office
                off.is_available = True
                off.save()
            else:
                pass
                # data.save()
            messages.success(request, 'Booking updated successfully')
            return redirect('office:bookings')
        form = OfficeBookingForm(instance = OfficeBooking.objects.get(id=id))
    
    context = {'form': form}
    return render(request, 'office/edit_booking.html', context)

@login_required
def tenants(request):
    form = TenantForm()
    if request.user.is_superuser:  
       tenants_list = enumerate(Tenant.objects.all(), start=1)
    else:
        land = LandLoad.objects.get(user = request.user)
        tenants_list = enumerate(Tenant.objects.filter(officebooking__office__landload = land), start=1)

    if request.method == 'POST':
        form = TenantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tenant added successfully')
            return redirect('office:tenants')
        else:
            form = TenantForm()
    context = {'form': form,  'tenants_list':tenants_list}
    return render(request, 'office/tenants.html', context)

@login_required
def landloads(request):
    form = LandLoadForm()
    
    landloads_list = enumerate(LandLoad.objects.all(), start=1)
    context = {'landloads_list':landloads_list, 'form': form}
    return render(request, 'office/landloads.html', context)

@login_required
def customers(request):
    return render(request, 'office/customers.html')

@login_required
def invoices(request):
    bookings = OfficeBooking.objects.all()

    
    context = {'booking_list': bookings}
    return render(request, 'office/invoices.html', context)



from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.http import HttpResponse
from io import BytesIO

@login_required
def download_invoice(request, id):
    if id:
        try:
            booking = OfficeBooking.objects.get(id=id)
            context = {
                'booking_id': booking.id,
                'office_name': booking.office.name,
                'tenant_name': booking.tenant.name,
                'total_cost': booking.office.price,
                'status': booking.status,
            }

            # Create a BytesIO buffer to store the PDF content
            buffer = BytesIO()

            # Create a ReportLab PDF document
            doc = SimpleDocTemplate(buffer, pagesize=letter)

            # Define invoice data
            invoice_data = [
                ["Invoice", ""],
                ["Booking ID:", context['booking_id']],
                ["Office Name:", context['office_name']],
                ["Tenant Name:", context['tenant_name']],
              
                ["Total Cost:", f"TSh {context['total_cost']}"],
                ["Status:", context['status']],
            ]

            # Create a table and style
            table = Table(invoice_data)
            style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)])

            table.setStyle(style)

            # Add the table to the PDF document
            doc.build([table])

            # Get the PDF content from the buffer
            pdf_bytes = buffer.getvalue()
            buffer.close()

            # Create an HTTP response with PDF content
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
            response.write(pdf_bytes)
            return response

        except OfficeBooking.DoesNotExist:
            return HttpResponse("Invalid booking_id", status=400)

    return HttpResponse("No ID provided", status=400)

@login_required
def offices(request):
    form = OfficeForm()
    if request.user.is_superuser:
         offices_list = enumerate(Office.objects.all(), start=1)
    else:
        offices_list = enumerate(Office.objects.filter(landload = request.user.landload), start=1)

    if request.method == 'POST':
        form = OfficeForm(request.POST, request.FILES)
        if form.is_valid():
            data =  form.save(commit=False)
            data.landload = LandLoad.objects.get(user = request.user)
            data.save()
            messages.success(request, 'Office added successfully')
            return redirect('office:offices')
        else:
            form = OfficeForm()
    print(offices_list)
    context = {'form': form, 'offices_list': offices_list}
    return render(request, 'office/offices.html', context)

@login_required
def profile(request):
    user = request.user
    initial_data = {'email': user.username}  # Add the field name and its initial value
    
    ld = LandLoad.objects.get(user = request.user)
    if request.method == 'POST':
        form = LandLoadForm(  request.POST, request.FILES, instance = ld,)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('office:profile')
    else:
        form = LandLoadForm(initial=initial_data, instance=ld)  # Pass the initial data to the form

    context = {'form': form}
    return render(request, 'office/profile.html', context)


def delete_office(request, id):
    office = Office.objects.get(id=id)
    office.delete()
    messages.success(request, 'Office deleted successful')
    return redirect(request.META.get('HTTP_REFERER', '/'))


# def edit_office(request, id):
#     messages.success(request, 'Office deleted successful')
#     return redirect(request.META.get('HTTP_REFERER', '/'))


def edit_office(request):
    office = Office.objects.get(id=request.POST.get('idd'))
    if request.method == 'POST':
        form = OfficeForm(request.POST, instance=office)
        if form.is_valid():
            form.save()
            messages.success(request, 'Office deleted successful')
        return redirect(request.META.get('HTTP_REFERER', '/'))
   
def delete_landload(request, id):
    landload= LandLoad.objects.get(id=id)
    landload.delete()
    messages.success(request, 'Landload deleted successful')
    return redirect(request.META.get('HTTP_REFERER', '/'))

  
def delete_tenant(request, id):
    tenant= Tenant.objects.get(id=id)
    tenant.delete()
    messages.success(request, 'Tenant deleted successful')
    return redirect(request.META.get('HTTP_REFERER', '/'))

