from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register_drive,name='register'),
    path('login/',views.login_drive,name='login'),
    path('logout/',views.logout_drive,name='logout'),
    path('dashbord/',views.dashbord_drive,name='dashbord')     
]
