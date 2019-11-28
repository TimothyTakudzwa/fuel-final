from django.shortcuts import render, get_object_or_404, redirect
import secrets
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from datetime import datetime
from django.contrib import messages
from buyer.models import User, Company
from django.contrib.auth import authenticate
from supplier.forms import UserUpdateForm
from .forms import ProfileUdateForm
from supplier.forms import *
from supplier.models import *
from django.contrib.auth.models import User

def fuel_updates(request):
    updates = FuelUpdate.objects.all()
    if request.method == 'POST':
        if FuelUpdate.objects.filter(date=today, fuel_type=request.POST.get('fuel_type')).exists():
            closing_time = time.strftime("%H:%M:%S")
            max_amount = request.POST.get('max_amount')
            min_amount = request.POST.get('min_amount')
            deliver = request.POST.get('deliver')
            payment_method = request.POST.get('payment_method')
            fuel_type = request.POST.get('fuel_type')
            supplier_id = request.user.id
            FuelUpdate.objects.create(supplier_id=supplier_id, deliver=False, fuel_type=fuel_type, closing_time=closing_time, max_amount=max_amount, min_amount=min_amount, payment_method=payment_method)
            messages.success(request, 'Quantity uploaded successfully')
            return redirect('fuel_updates')
        else:
            fuel_update = FuelUpdate.objects.get(fuel_type=request.POST.get('fuel_type'), date=today)
            fuel_update.max_amount = request.POST.get('max_amount')
            fuel_update.min_amount = request.POST.get('min_amount')
            fuel_update


    return render(request, 'serviceStation/fuel_updates.html', {'updates': updates})


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
    return render(request, 'serviceStation/profile.html', context=context)

'''
def user_profile(request):
    user = User.objects.filter(name=request.name)
    if request.method == 'POST':
        form = ProfileUdateForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            form = ProfileUdateForm()

    else:
        form = ProfileUdateForm()
    return render(request, 'serviceStation/userprofile.html', {'user': user})

'''