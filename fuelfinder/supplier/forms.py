from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Profile, FuelUpdate, FuelRequest
from django.contrib.auth import get_user_model

User = get_user_model()


class PasswordChange(PasswordChangeForm):
    class Meta:
        widgets = {

        }
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


class RegistrationForm(UserCreationForm):
    class Meta:
        widgets = {
            'password': forms.PasswordInput()
        }

        model = User
        fields = ['username', 'password1', 'password2']


class RegistrationProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone']


class RegistrationEmailForm(forms.Form):
    email = forms.EmailField()


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone']


class ProfilePictureUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture']


class FuelRequestForm(forms.ModelForm):
    OPTIONS= [
    ('SELF COLLECTION', 'self collection'),
    ('DELIVERY', 'delivery'),
    ]

    delivery_method = forms.CharField(label='Delivery Method', widget=forms.Select(choices=OPTIONS))
    
    class Meta:
        model = FuelRequest
        fields = ['amount', 'split', 'payment_method', 'delivery_method', 'fuel_type']


