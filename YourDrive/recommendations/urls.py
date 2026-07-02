from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_recommendations, name='recommendations'),
    path('retrain/', views.retrain_model, name='retrain_model'),
]
