from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'office'
urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('', views.signup, name='signup'),
    path('dashbboard/', views.dashboard   ,  name="dashboard"),
    path('bookings/', views.bookings   ,  name="bookings"),
    path('tenants/', views.tenants   ,  name="tenants"),
    path('invoices/', views.invoices   ,  name="invoices"),
    path('download_invoice/<str:id>/', views.download_invoice   ,  name="download_invoice"),
    path('customers/', views.customers   ,  name="customers"),
    path('offices/', views.offices   ,  name="offices"),
    path('landloads/', views.landloads , name="landloads"),
    path('profile/', views.profile , name="profile"),
    
    path('logout/', views.logout_user , name="logout"),
    # path('upload_isu/', views.upload_isu, name="upload_isu"),
    path('edit_booking/<str:id>/', views.edit_booking, name="edit_booking"),

    path('delete_office/<str:id>/', views.delete_office, name="delete_office"),
    path('edit_office/', views.edit_office, name="edit_office"),

    path('delete_landload/<str:id>/', views.delete_landload, name="delete_landload"),
    path('delete_tenant/<str:id>/', views.delete_tenant, name="delete_tenant"),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

