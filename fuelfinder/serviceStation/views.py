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
        if FuelUpdate.objects.filter(fuel_type=request.POST.get('fuel_type')).exists():
            fuel_update = FuelUpdate.objects.get(fuel_type=request.POST.get('fuel_type'))
            fuel_update.available_quantity = request.POST.get('available_quantity')
            fuel_update.save()
            messages.success(request, 'updated quantity successfully')
            return redirect('serviceStation:serviceStation')
        else:
            available_quantity = request.POST.get('available_quantity')
            price = request.POST.get('price')
            status = request.POST.get('status')
            queue_size = request.POST.get('queue_size')
            fuel_type = request.POST.get('fuel_type')
            payment_method = request.POST.get('payment_method')
            supplier = request.user
            FuelUpdate.objects.create(supplier=supplier, payment_method=payment_method, fuel_type=fuel_type, available_quantity=available_quantity, price=price, queue_size=queue_size, status=status)
            messages.success(request, 'Quantity uploaded successfully')
            return redirect('serviceStation:serviceStation')

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