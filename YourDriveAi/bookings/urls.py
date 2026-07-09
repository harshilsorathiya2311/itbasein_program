from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_bookings, name='my_bookings'),
    path('create/<int:car_id>/', views.create_booking, name='create_booking'),
]
