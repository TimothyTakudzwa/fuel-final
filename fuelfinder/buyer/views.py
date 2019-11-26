from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BuyerRegisterForm, BuyerUpdateForm, ProfileUpdateForm
from supplier.forms import FuelRequestForm
from buyer.models import User, Company
import requests
import secrets
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from datetime import datetime
from .constants import sender, subject


def token_is_send(request, user):
    token = secrets.token_hex(12)
    domain = request.get_host()            
    url = f'{domain}/verification/{token}/{user.id}'
    message = f"Dear {user.first_name}  {user.last_name}, please complete signup here : \n {url} \n. "            
    try:
        print(message)
        msg = EmailMultiAlternatives(subject, message, sender, [f'{user.email}'])
        msg.send()

        messages.success(request, f"{user.first_name}  {user.last_name} Registered Successfully")
        return True
    except Exception as e:
        print(e)
        messages.warning(request, f"Oops , Something Wen't Wrong, Please Try Again")
        return False              
    messages.success(request, ('Your profile was successfully updated!'))
    return redirect('users:supplier_user_create', sid=user.id)

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = BuyerRegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            full_name = first_name + " " + last_name
            i = 0
            username = initial_username = first_name[0] + last_name
            while  User.objects.filter(username=username.lower()).exists():
                username = initial_username + str(i) 
                i+=1
            user = User.objects.create(email=email, username=username.lower(),  phone_number=phone_number, first_name=first_name, last_name=last_name, is_active=False)        
            if token_is_send(request, user):
                messages.success(request, f"{full_name} Registered Successfully")   
                if user.is_active:
                    send_message(user.phone_number, "You have been registered succesfully")
                    user.stage = 'requesting'
                    user.save()               
                return redirect('users:supplier_user_create', sid=user.id)
            else:
                messages.warning(request, f"Oops , Something Wen't Wrong, Please Try Again")
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

def send_message(phone_number, message):
    payload = {
        "phone": phone_number,
        "body": message
    }
    url = "https://eu33.chat-api.com/instance78632/sendMessage?token=sq0pk8hw4iclh42b"
    r = requests.post(url=url, data=payload)
    print(r)
    return r.status_code

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

            
