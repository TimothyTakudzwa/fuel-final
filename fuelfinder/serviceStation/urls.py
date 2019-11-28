from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

#from .views import user_profile

urlpatterns = [
    path('serviceStation/', views.fuel_updates, name="serviceStation"),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('allocated_fuel/', views.allocated_fuel, name='allocated_fuel'),
    
]