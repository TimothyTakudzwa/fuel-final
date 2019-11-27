from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, FuelRequest
from .constants import *
from django.contrib.auth import get_user_model

User = get_user_model()


class BuyerRegisterForm(forms.ModelForm):
    email = forms.EmailField()
    phone_number = forms.CharField()
    first_name = forms.CharField() 
    last_name = forms.CharField()

    class Meta: 
        model = User
        fields = ['email', 'phone_number', 'first_name', 'last_name']

OPTIONS= [
('BUYER', 'Buyer'),
('SUPPLIER', 'supplier'),
]


class SupplierUserForm(forms.Form):
    company = forms.CharField()
    phone_number = forms.CharField()
    supplier_role = forms.CharField()


    
class BuyerUpdateForm(UserCreationForm):
    company_id = forms.CharField(label='Company', widget=forms.Select(choices=COMPANY_CHOICES))
    user_type = forms.CharField(label='User Type', widget=forms.Select(choices=OPTIONS))
    company_position = forms.CharField()
    class Meta:
        model = User   
        fields = ['image', 'company_id','user_type', 'company_position','password1', 'password2']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']

class FuelRequestForm(forms.ModelForm):
    OPTIONS= [
    ('SELF COLLECTION', 'self collection'),
    ('DELIVERY', 'delivery'),
    ]

    delivery_method = forms.CharField(label='Delivery Method', widget=forms.Select(choices=OPTIONS))
    
    class Meta:
        model = FuelRequest
        fields = ['amount','payment_method', 'delivery_method', 'fuel_type']
