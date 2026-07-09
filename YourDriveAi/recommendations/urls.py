from django.urls import path
from . import views

urlpatterns = [
    path('', views.recommend_cars, name='recommend_cars'),
    path('preferences/', views.save_preferences, name='save_preferences'),
]
