from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
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
    username = forms.CharField()
    user_type = forms.CharField(label='User Type', widget=forms.Select(choices=OPTIONS))
    position = forms.CharField()
    


    class Meta:
        model = User   
        fields = ['image', 'username','user_type', 'position','password1', 'password2']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']
