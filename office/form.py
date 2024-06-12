from django import forms
from .models import *

from django import forms
from .models import LandLoad, Tenant, Office, OfficeBooking, Invoice

class MainForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MainForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.required = True
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
                field.required = False

            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'

                


class LandLoadForm(MainForm):
    class Meta:
        model = LandLoad
        exclude =['user']


class TenantForm(MainForm):
    class Meta:
        model = Tenant
        exclude =['user']

class OfficeForm(MainForm):
    class Meta:
        model = Office
        exclude = ['landload']

    def __init__(self, *args, **kwargs):
        super(OfficeForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = False


class OfficeBookingForm(MainForm):
    class Meta:
        model = OfficeBooking
        fields = '__all__'

class InvoiceForm(MainForm):
    class Meta:
        model = Invoice
        fields = '__all__'
