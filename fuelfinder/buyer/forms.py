from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .constants import COMPANY_CHOICES
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
