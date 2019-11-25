from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BuyerRegisterForm, BuyerUpdateForm, ProfileUpdateForm
from supplier.forms import FuelRequestForm
from buyer.models import User, Company
import secrets
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from datetime import datetime


#def token_gen(request):

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = BuyerRegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            # Company.objects.create(name='example', address='123', industry='test', company_type='BUYER')
            # company = Company.objects.get(name='example')
            User.objects.create(email=email, phone_number=phone_number, first_name=first_name, last_name=last_name, is_active=False)
            # user.save() 
            token = secrets.token_hex(12)
            domain = request.get_host()
            user = User.objects.get(email=email)
            url = f'{domain}/verification/{token}/{user.id}'

            sender = f'Fuel Finder Accounts<tests@marlvinzw.me>'
            subject = 'User Registration'
            message = f"Dear {first_name} {last_name} , please complete signup here : \n {url} \n."
            
            try:
                msg = EmailMultiAlternatives(subject, message, sender, [f'{email}'])
                msg.send()

                messages.success(request, f"{first_name} {last_name} Registered Successfully")
                return redirect('users:supplier_user_create', sid=user.id)

            except BadHeaderError:
                messages.warning(request, f"Oops , Something Wen't Wrong, Please Try Again")
                return redirect('users:supplier_user_create', sid=user.id)
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

            
