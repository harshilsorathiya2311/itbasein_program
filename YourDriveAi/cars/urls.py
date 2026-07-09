from django.urls import path
from . import views

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('<int:car_id>/', views.car_detail, name='car_detail'),
    path('compare/', views.car_compare, name='car_compare'),
    path('brand/<int:brand_id>/', views.brand_cars, name='brand_cars'),
]
