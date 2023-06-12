from rest_framework import serializers
from office.models import LandLoad, Tenant, Office, OfficeBooking, Invoice

class LandLoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandLoad
        fields = ['id', 'user', 'email', 'name', 'description', 'logo', 'location']

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['id', 'user', 'email', 'name']

class OfficeSerializer(serializers.ModelSerializer):
    landload = LandLoadSerializer()

    class Meta:
        model = Office
        fields = ['id', 'name', 'landload', 'location', 'picture', 'price', 'size', 'is_available']

class OfficeBookingSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer()
    office = OfficeSerializer()

    class Meta:
        model = OfficeBooking
        fields = ['id','status', 'tenant', 'office']

class InvoiceSerializer(serializers.ModelSerializer):
    booking = OfficeBookingSerializer()

    class Meta:
        model = Invoice
        fields = ['id', 'booking', 'issued_date', 'status']
