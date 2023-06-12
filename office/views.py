from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from office.form import *
from .models import *

def upload_isu(request):
    action = "issuu.document.upload"
    apiKey = "hukprh6d967ap9w8mu41lgi79kk8fr36"
    name = "racing"
    title = "Race Cars"
    
    import hashlib
    sig = f"actionissuu.document.uploadapiKey{apiKey}nameracingtitleRace Cars"

    # Create an instance of the MD5 hash object
    md5_hash = hashlib.md5()

    # Update the hash object with the string
    md5_hash.update(sig.encode())

    # Get the hexadecimal representation of the hash
    md5_hash_hex = md5_hash.hexdigest()

    print(md5_hash_hex)

    
    context = {
        'sig': md5_hash_hex,
    }
    return render(request, 'upload.html', context)

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
    return render(request, 'office/invoices.html')

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
