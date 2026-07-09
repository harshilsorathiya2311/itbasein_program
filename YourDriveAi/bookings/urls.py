from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_bookings, name='my_bookings'),
    path('create/<int:car_id>/', views.create_booking, name='create_booking'),
    path('admin/manage/', views.admin_manage_bookings, name='admin_manage_bookings'),
    path('admin/approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('admin/reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),
]
