from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics_dashboard, name='analytics_dashboard'),
    path('api/stats/', views.api_dashboard_data, name='api_dashboard_data'),
    path('api/brands/', views.api_brand_analysis, name='api_brand_analysis'),
    path('api/bookings/', views.api_booking_analysis, name='api_booking_analysis'),
    path('api/popular/', views.api_popular_cars, name='api_popular_cars'),
    path('api/price/', views.api_price_stats, name='api_price_stats'),
    path('api/users/', views.api_user_growth, name='api_user_growth'),
]
