from django.urls import path
from .views import BookingAPIView, CreateUserView, LandLoadAPIView, TenantAPIView, OfficeAPIView, OfficeBookingAPIView, InvoiceAPIView, DownloadContract


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # api url for creating a user
    path('users/create/', CreateUserView.as_view(), name='create_user'),
    path('users/update/', CreateUserView.as_view(), name='update_user'),

    path('users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('landloads/', LandLoadAPIView.as_view()),
    path('tenants/', TenantAPIView.as_view()),
    path('offices/', OfficeAPIView.as_view()),
    path('offices/<str:office_id>/book/', BookingAPIView.as_view()),
    path('offices/<str:id>/', OfficeAPIView.as_view()),

    path('officebookings/', OfficeBookingAPIView.as_view()),
    path('officebookings/<str:booking_id>/', OfficeBookingAPIView.as_view()),
    
    path('invoices/', InvoiceAPIView.as_view()),
    
    path('download_contract/', DownloadContract.as_view(), name='download_contract')
    
]
