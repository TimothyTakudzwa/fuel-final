from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BuyerRegisterForm, BuyerUpdateForm, ProfileUpdateForm
from supplier.forms import FuelRequestForm
from fuelfinder.settings import AUTH_USER_MODEL as User

import secrets
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from datetime import datetime


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = BuyerRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            

            user = User.objects.create_user(username, email, password)
            user.save() 
            token = secrets.token_hex(12)
            domain = request.get_host()
            url = f'{domain}/verification/{token}/{user.id}'

            sender = f'Fuel Finder Accounts<tests@marlvinzw.me>'
            subject = 'User Registration'
            message = f"Dear {username} , please complete signup here : \n {url} \n. Your password is {password}"
            
            try:
                msg = EmailMultiAlternatives(subject, message, sender, [f'{email}'])
                msg.send()

                messages.success(request, f"{username} Registered Successfully")
                return redirect('users:suppliers_list')

            except BadHeaderError:
                messages.warning(request, f"Oops , Something Wen't Wrong, Please Try Again")
                return redirect('users:suppliers_list')
            #contact.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('users:supplier_user_create', sid=user.id)
        
        else:
            msg = "Error in Information Submitted"
            messages.error(request, msg)

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('buyer-login')
    else:
        form = BuyerRegisterForm
    
    return render(request, 'buyer/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = BuyerUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.Profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, f'Your account has been updated')
            return redirect('buyer-profile')
        
    else:
        u_form = BuyerUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.Profile)

    context = {

        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'buyer/profile.html', context)

@login_required
def fuel_request(request):
    if request.method == 'POST':
        form = FuelRequestForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('buyer-login')
    else:
        form = FuelRequestForm
    
    return render(request, 'buyer/fuel_request.html', {'form': form})

            
