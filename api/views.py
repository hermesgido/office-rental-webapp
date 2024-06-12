from base64 import b64encode
from django.http import HttpResponse
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from office.models import LandLoad, Tenant, Office, OfficeBooking, Invoice
from office.views import bookings
from .serializers import LandLoadSerializer, TenantSerializer, OfficeSerializer, OfficeBookingSerializer, InvoiceSerializer
from django.contrib.auth.models import User

from django.template.loader import get_template
# from xhtml2pdf import pisa
from django.conf import settings
from io import BytesIO

from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication


def send_sms(number, message):
    import requests
    from requests.auth import HTTPBasicAuth
    url = "https://apisms.beem.africa/v1/send"

    data = {
        "source_addr": "INFO",
        "encoding": 0,
        "message": message,
        "recipients": [
            {
                "recipient_id": 1,
                "dest_addr": f"{number}"
            }
        ]
    }
    password = "MGVjMjVhOTQ1N2U0MmM2MzQwNjc2YzI3MjdiMzk2YzViZjVhNDcyZGRkODViMDc3MGFlYTkzYzQ1YTAyMjAwZg=="
    username = "ce64e6750d9de50e"

    response = requests.post(url, json=data, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:
        print("SMS sent successfully!")
    else:
        print("SMS sending failed. Status code:", response.status_code)
        print("Response:", response.text)




class CreateUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        # You can include other user fields as needed

        if username and password and email:
            try:
                user = User.objects.create_user(username=username, password=password, email=email)
                tn = Tenant.objects.create(user= user )
                tn.save()
                return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        # You can include other user fields as needed

        if username and email:
            try:
                user = User.objects.get(username=username)
                user.email = email
                if password:
                    user.set_password(password)
                user.save()
                return Response({'message': 'User updated successfully'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        
class LandLoadAPIView(APIView):
    def get(self, request):
        landloads = LandLoad.objects.all()
        serializer = LandLoadSerializer(landloads, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LandLoadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class TenantAPIView(APIView):
    def get(self, request):
        tenants = Tenant.objects.all()
        serializer = TenantSerializer(tenants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TenantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class OfficeAPIView(APIView):
    def get(self, request, id=None):
        if id:
            office = Office.objects.get(id=id)
            serializer = OfficeSerializer(office)
            return Response(serializer.data)
        else:
            offices = Office.objects.filter(is_available=True)
            serializer = OfficeSerializer(offices, many=True)
            return Response(serializer.data)

            
    
    def post(self, request):
        
        serializer = OfficeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

def send_sms_api(  message, 
             recipients, 
              ):
    content_type="application/json"
    schedule_time=None
    recipient_id=None
    dest_addr=None
    encoding=0
    api_key = ""
    secret_key = "=="
    source_addr = "INFO"
    
    url = "https://apisms.beem.africa/v1/send"
    headers = {
        "Content-Type": content_type
    }
    auth = (api_key, secret_key)
    data = {
        "source_addr": source_addr,
        "message": message,
        "recipients": recipients,
        "encoding": encoding
    }
    if recipient_id:
        data["recipient_id"] = recipient_id
    if dest_addr:
        data["dest_addr"] = dest_addr
    if schedule_time:
        data["schedule_time"] = schedule_time

    response = requests.post(url, headers=headers, auth=auth, json=data)
    
    return response.json()

    

# Example usage:

# message = "Hello from Beem Africa!"
# recipients = ["255621189850"]  # Example destination number
# response = send_sms_api(message, recipients)
# print(response)


def send_sms2():
    import requests
    from requests.auth import HTTPBasicAuth
    url = "https://apisms.beem.africa/v1/send"

    data = {
        "source_addr": "INFO",
        "encoding": 0,
        "message": "SMS Test from Python API",
        "recipients": [
            {
                "recipient_id": 1,
                "dest_addr": "255655060606"
            }
        ]
    }
    username = "<api_key>"
    password = "<secret-key>"
    response = requests.post(url, json=data, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:
        print("SMS sent successfully!")
    else:
        print("SMS sending failed. Status code:", response.status_code)
        print("Response:", response.text)
        
class BookingAPIView(APIView):
    ##authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        data = request.data
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        print(token)
        office_id = data.get('office_id')
        user = request.user

        user = Tenant.objects.first().user
        print(user)
        if office_id and user:
            office = Office.objects.get(id=office_id)
            print(office.is_available)
            if office.is_available:
                book = OfficeBooking.objects.create(tenant=user.tenant, office=Office.objects.get(id=office_id))
                book.save()
                office.is_available = False
                office.save()
                
                response = {
                    "office_id": office_id,
                    "success": True,
                    "message": "Your office booking is successful"
                }
                phone_no = ""
                if office.landload.phone_number:
                    phone_no = office.landload.phone_number
                else:
                    phone_no = "255621189850"
                message = f"Someone booked your office:  {office.name} login to the system to view"
                send_sms(phone_no, message)
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "office_id": office_id,
                    "success": False,
                    "message": "Office Already Booked"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        else:
            response = {
                "office_id": office_id,
                "success": False,
                "message": "Your office booking is not successful"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    
class OfficeBookingAPIView(APIView):
    def get(self, request, booking_id = None):
        user_id = request.GET.get('user_id')
        if user_id:
           user = request.user
           print(user)
           office_bookings = OfficeBooking.objects.filter(tenant = user.tenant)
           print(office_bookings)
           serializer = OfficeBookingSerializer(office_bookings, many=True)
           return Response(serializer.data)
       
        if booking_id:
           office_bookings = OfficeBooking.objects.get(id = booking_id)
           serializer = OfficeBookingSerializer(office_bookings, many=False)
           return Response(serializer.data)

        office_bookings = OfficeBooking.objects.all()
        serializer = OfficeBookingSerializer(office_bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OfficeBookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class InvoiceAPIView(APIView):
    def get(self, request):
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)




def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return result.getvalue()
    return None

class DownloadContract(APIView):
    def get(self, request):
        booking_id = request.GET.get("booking_id")
        if booking_id:
            try:
                booking = OfficeBooking.objects.get(id=booking_id)
                context = {
                    'booking_id': booking.id,
                    # Add other necessary context variables here
                }
                pdf = render_to_pdf('contract.html', context)
                if pdf:
                    response = HttpResponse(content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename="contract.pdf"'
                    response.write(pdf)
                    return response
                return HttpResponse("Failed to generate PDF", status=500)
            except OfficeBooking.DoesNotExist:
                return HttpResponse("Invalid booking_id", status=400)
        return HttpResponse("Missing booking_id", status=400)





# def payments_download_invoice(request, amount, *args, **kwargs):
#     context = {
#         'user_info':"kk",
   
#     }
#     pdf_response = download_invoice(context)
#     pdf = pdf_response.content

#     return pdf_response