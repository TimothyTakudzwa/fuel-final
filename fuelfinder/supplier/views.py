from django.contrib.auth import authenticate, update_session_auth_hash, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.contrib import messages
import secrets

from datetime import date
import time

from .forms import PasswordChange, RegistrationForm, RegistrationProfileForm, \
    RegistrationEmailForm, UserUpdateForm, ProfilePictureUpdateForm, ProfileUpdateForm, FuelRequestForm
from .models import Profile, FuelUpdate, FuelRequest, Transaction, Profile, TokenAuthentication
from django.contrib.auth import get_user_model

User = get_user_model()

# today's date
today = date.today()


def register(request):
    context = {
        'title': 'Fuel Finder | Register',
        'email': RegistrationEmailForm(),
        'registration': RegistrationForm()
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 == pass2:
            User.objects.create_user(username=username, email=email, password=pass1)

            user = User.objects.get(username=username)
            user.is_active = False
            user.save()

            token = secrets.token_hex(12)
            TokenAuthentication.objects.create(token=token, user = user)
            domain = request.get_host()
            url = f'{domain}/verification/{token}/{user.id}'

            sender = f'Fuel Finder Accounts<tests@marlvinzw.me>'
            subject = 'User Registration'
            message = f"Dear {username} , complete signup here : \n {url} \n. Your password is {pass1}"

            try:
                msg = EmailMultiAlternatives(subject, message, sender, [f'{email}'])
                msg.send()

                messages.success(request, f"{username} Registered Successfully")
                return redirect('dashboard')

            except BadHeaderError:
                messages.warning(request, f"Oops , Something Wen't Wrong, Please Try Again")
                return redirect('register')
        else:
            messages.warning(request, "Passwords don't match")
            return redirect('register')
    return render(request, 'supplier/accounts/register.html', context=context)


def verification(request, token, user_id):
    context = {
        'title': 'Fuel Finder | Verification',
    }
    check = User.objects.filter(id=user_id)
    print("here l am ")
    
    if check.exists():
        user = User.objects.get(id=user_id)
        print(user)

        token_check = TokenAuthentication.objects.filter(user=user, token=token)
        result = bool([token_check])
        print(result)
        if result == True:
            print("tapindawo")
            user.is_active = True
            user.save()
            messages.success(request, f'Welcome {user.username}, your account is now verified')

        else:
            messages.warning(request, 'Wrong verification token')
            return redirect('login')
    else:
        messages.warning(request, 'Wrong verification id')
        return redirect('login')
    return render(request, 'supplier/accounts/verification.html', context=context)


def sign_in(request):
    context = {
        'title': 'Fuel Finder | Login',
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        authenticated = authenticate(username=username, password=password)
        if authenticated:
            client = User.objects.get(username=username)
            login(request, client)

            messages.success(request, 'Welcome {client.username}')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Incorrect username or password')
            return redirect('login')

    return render(request, 'supplier/accounts/login.html', context=context)


@login_required()
def change_password(request):
    context = {
        'title': 'Fuel Finder | Change Password',
        'password_change': PasswordChange(user=request.user)
    }
    if request.method == 'POST':
        old = request.POST.get('old_password')
        new1 = request.POST.get('new_password1')
        new2 = request.POST.get('new_password2')

        if authenticate(request, username=request.user.username, password=old):
            if new1 != new2:
                messages.warning(request, "Passwords Don't Match")
                return redirect('change-password')
            else:
                user = request.user
                user.set_password(new1)
                user.save()
                update_session_auth_hash(request, user)

                messages.success(request, 'Password Successfully Changed')
                return redirect('dashboard')
        else:
            messages.warning(request, 'Wrong Old Password, Please Try Again')
            return redirect('change-password')
    return render(request, 'supplier/accounts/change_password.html', context=context)


@login_required()
def account(request):
    context = {
        'title': 'Fuel Finder | Account',
        'user': UserUpdateForm(instance=request.user)

    }
    if request.method == 'POST':
        userform = UserUpdateForm(request.POST, instance=request.user)
        if userform.is_valid():
            userform.save()
            messages.success(request, f'Profile successfully updated')
            return redirect('account')
        else:
            messages.warning(request, f'Something went wrong while saving your changes')
            return redirect('account')
    return render(request, 'supplier/accounts/account.html', context=context)


@login_required()
def fuel_request(request):
    context = {
        'title': 'Fuel Finder | Fuel Request',
        'requests': FuelRequest.objects.filter(date=today)
    }
    if request.method == 'POST':
        submitted_id = request.POST.get('request_id')
        if FuelRequest.objects.filter(id=submitted_id).exists():
            request_id = FuelRequest.objects.get(id=submitted_id)
            buyer_id = Profile.objects.get(id='')
            Transaction.objects.create(request_id=request_id,
                                       buyer_id=buyer_id)
            messages.success(request, f'You have accepted a request for {request_id.amount} litres from {buyer_id.name}')
            return redirect('fuel-request')
    return render(request, 'supplier/accounts/fuel_request.html', context=context)


@login_required()
def rate_supplier(request):
    context = {
        'title': 'Fuel Finder | Rate Supplier',
    }
    return render(request, 'supplier/accounts/ratings.html', context=context)

@login_required
def fuel_update(request):
    if request.method == 'POST':
        form = FuelUpdateForm(request.POST)
        if form.is_valid:
            closing_time = time.strftime("%H:%M:%S")
            max_amount = request.POST.get('max_amount')
            min_amount = request.POST.get('min_amount')
            deliver = request.POST.get('deliver')
            payment_method = request.POST.get('payment_method')
            supplier = Profile.objects.get(name=request.user)
            FuelUpdate.objects.create(closing_time=closing_time, max_amount=max_amount, min_amount=min_amount, deliver=deliver, payment_method=payment_method)
            message.success(request, 'Capacity updated successfully')
            return redirect('fuel-request')
        else:
            message.warning(request, 'Oops something went wrong!')
            return redirect('fuel-request')

    return render(request, 'supplier/accounts/ratings.html', {'form':form})

