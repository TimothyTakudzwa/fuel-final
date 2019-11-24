from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class BuyerRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_number = forms.CharField()
    username = forms.CharField()

    class Meta: 
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']




class BuyerUpdateForm(forms.ModelForm):
    email = forms.EmailField()


    class Meta:
        model = User   
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']
