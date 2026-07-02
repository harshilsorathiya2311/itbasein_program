from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:car_id>/', views.book_test_drive, name='book_test_drive'),
    path('book/', views.book_test_drive, name='book_test_drive_empty'),
    path('my/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:pk>/', views.cancel_booking, name='cancel_booking'),
]
