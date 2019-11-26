from django.shortcuts import render, get_object_or_404, redirect

from django.shortcuts import Http404
from supplier.models import *
from supplier.forms import *
from buyer.models import *
from buyer.forms import *
from .forms import *
import secrets
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from datetime import datetime
from django.contrib import messages
from buyer.models import User, Company
from django.contrib.auth import authenticate

def index(request):
    return render(request, 'users/index.html')


def supplier_user_edit(request, cid):
    supplier = User.objects.filter(id=cid).first()

    if request.method == "POST":
        supplier.company = request.POST['company']
        supplier.phone_number = request.POST['phone_number']
        supplier.user_type = request.POST['user_type']
        supplier.supplier_role = request.POST['supplier_role']
        supplier.save()
        messages.success(request, 'Your Changes Have Been Saved')



def stations(request):
    #user = authenticate(username='john', password='secret')
    #admin_ = User.objects.filter(company_id='Marshy').first()
    # print(admin_.company)
    stations = ServiceStation.objects.all()

    return render(request, 'users/service_stations.html', {'stations': stations})    


def audit_trail(request):
    return render(request, 'users/audit_trail.html', {'stations': stations})    

        

def suppliers_list(request):
    #user = authenticate(username='john', password='secret')
    suppliers = User.objects.filter(supplier_role='Staff').all()
    #print(admin_.company)
    #suppliers = User.objects.all()
    
    if request.method == 'POST':
        form1 = SupplierContactForm(request.POST)
        print('--------------------tapinda---------------')
        user_count = User.objects.filter(company_id='ZUVA').count()
        print(user_count)
        if user_count > 10:
            raise Http404("Your organisation has reached the maximum number of users, delete some ")

        if form1.is_valid():
            print('--------------------tapinda---------------')
            username = form1.cleaned_data['username']
            email = form1.cleaned_data['email']
            password = form1.cleaned_data['password']
            phone_number = form1.cleaned_data['phone_number']
            company = form1.cleaned_data['company']
            supplier_role = 'Staff'

            print(type(User))
            User.objects.create(username=username,email=email,password=password,company_id=company,phone_number=phone_number,supplier_role=supplier_role)
            messages.success(request, f"{username} Registered Successfully")

            token = secrets.token_hex(12)
            user = User.objects.get(username=username)
            TokenAuthentication.objects.create(token=token, user=user)
            domain = request.get_host()
            url = f'{domain}/verification/{token}/{user.id}' 

            sender = f'Fuel Finder Accounts<tests@marlvinzw.me>'
            subject = 'User Registration'
            message = f"Dear {username} , please complete signup here : \n {url} \n. Your password is {password}"
            
            try:
                msg = EmailMultiAlternatives(subject, message, sender, [f'{email}'])
                msg.send()

                messages.success(request, f"{username} Registered Successfully")
                return redirect('users:buyers_list')

            except BadHeaderError:
                messages.warning(request, f"Oops , Something Wen't Wrong, Please Try Again")
                return redirect('users:buyers_list')
            #contact.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('users:suppliers')
            print(token)
            print("above is the token")
    else:
        form1 = SupplierContactForm()           
    
    return render(request, 'users/suppliers_list.html', {'form1': form1, 'suppliers': suppliers})

def suppliers_delete(request, sid):
    supplier = User.objects.filter(id=sid).first()
    if request.method == 'POST':
        supplier.delete()    

    return redirect('users:suppliers_list')

def buyers_list(request):
    buyers = Profile.objects.all()
    edit_form = ProfileEditForm()
    delete_form = ActionForm()
    return render(request, 'users/buyers_list.html', {'buyers': buyers, 'edit_form': edit_form, 'delete_form': delete_form})

def buyers_delete(request, sid):
    buyer = Profile.objects.filter(id=sid).first()
    if request.method == 'POST':
        buyer.delete()    

    return redirect('users:buyers_list')


def supplier_user_delete(request,cid,sid):
    contact = SupplierContact.objects.filter(id=cid).first()
    if request.method == 'POST':
        contact.delete()

    return redirect('users:supplier_user_create', sid=sid)  

# Begining Of Supplier Management

def supplier_user_create(request, sid):
    supplier = get_object_or_404(Profile, id=sid) 
    staff = SupplierContact.objects.filter(supplier_profile=supplier)
    count = staff.count()
    delete_form = ActionForm()
    edit_form = ''
    if request.method == 'POST':
        user_count = SupplierContact.objects.filter(supplier_profile=supplier).count()
        if user_count > 5:
            raise Http404("Organisations has 5 users, delete some ")
        form = SupplierContactForm(request.POST)
        staffer_edit_form = SupplierStaffEditForm()
        profile_form = UserUpdateForm(request.POST, instance=request.user)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your Changes Have Been Saved')
            return redirect('users:supplier_user_create', sid=supplier.id)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            cellphone = form.cleaned_data['cellphone']
            telephone = form.cleaned_data['telephone']

            user = User.objects.create_user(first_name, email, password)
            user.last_name = form.cleaned_data['last_name']
            user.first_name = form.cleaned_data['first_name']
            user.save()   
            contact = SupplierContact.objects.create(user=user, cellphone=cellphone, telephone=telephone, profile=supplier)

            token = secrets.token_hex(12)
            domain = request.get_host()
            url = f'{domain}/verification/{token}/{user.id}'

            sender = f'Fuel Finder Accounts<tests@marlvinzw.me>'
            subject = 'User Registration'
            message = f"Dear {first_name} , please complete signup here : \n {url} \n. Your password is {password}"
            
            try:
                msg = EmailMultiAlternatives(subject, message, sender, [f'{email}'])
                msg.send()

                messages.success(request, f"{first_name} Registered Successfully")
                return redirect('users:suppliers_list')

            except BadHeaderError:
                messages.warning(request, f"Oops , Something Wen't Wrong, Please Try Again")
                return redirect('users:suppliers_list')
            #contact.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('users:supplier_user_create', sid=supplier.id)
            
        
        else:
            msg = "Error in Information Submitted"
            messages.error(request, msg)
    else:
        form = SupplierContactForm()
        profile_form = UserUpdateForm(instance=supplier)
        staffer_edit_form = SupplierStaffEditForm()



    return render (request, 'users/add_user.html', {'form': form, 'supplier': supplier, 'staff': staff, 'count': count,
     'delete_form':delete_form, 'edit_form': edit_form, 'profile_form':profile_form, 'staffer_edit_form':staffer_edit_form}) 


def buyer_user_create(request, sid):
    buyer = get_object_or_404(Profile, id=sid) 
    staff = BuyerContact.objects.filter(buyer_profile=buyer)
    count = BuyerContact.objects.all().count()
    delete_form = ''
    edit_form = ''
    if request.method == 'POST':
        user_count = BuyerContact.objects.filter(buyer_profile=buyer).count()
        if user_count > 10:
            raise Http404("Your organisation has reached the maximum number of users, delete some ")
        form = BuyerContactForm(request.POST)
        profile_form = UserUpdateForm(request.POST, instance=buyer)

        if profile_form.is_valid():
            buyer = profile_form.save()
            messages.success(request, 'Your Changes Have Been Saved')
            return redirect('users:buyer_user_create', sid=buyer.id)

        

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            cellphone = form.cleaned_data['phone']
            user = User.objects.create_user(first_name, email, password)
            user.last_name = form.cleaned_data['last_name']
            user.first_name = form.cleaned_data['first_name']
            user.save()   
            contact = BuyerContact.objects.create(user=user, phone=cellphone, buyer_profile=buyer)

            token = secrets.token_hex(12)
            user = User.objects.get(first_name=first_name)
            TokenAuthentication.objects.create(token=token, user=user)
            domain = request.get_host()
            url = f'{domain}/verification/{token}/{user.id}' 

            sender = f'Fuel Finder Accounts<tests@marlvinzw.me>'
            subject = 'User Registration'
            message = f"Dear {first_name} , please complete signup here : \n {url} \n. Your password is {password}"
            
            try:
                msg = EmailMultiAlternatives(subject, message, sender, [f'{email}'])
                msg.send()

                messages.success(request, f"{first_name} Registered Successfully")
                return redirect('users:buyers_list')

            except BadHeaderError:
                messages.warning(request, f"Oops , Something Wen't Wrong, Please Try Again")
                return redirect('users:buyers_list')
            #contact.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('users:buyer_user_create', sid=buyer.id)
            print(token)
            print("above is the token")

        else:
            msg = "Error in Information Submitted"
            messages.error(request, msg)
    else:
        form = BuyerContactForm()
        profile_form = UserUpdateForm(instance=buyer)



    return render (request, 'users/add_buyer.html', {'form': form, 'buyer': buyer, 'staff': staff, 'count': count, 'delete_form':delete_form, 'edit_form': edit_form, 'profile_form':profile_form}) 


def edit_supplier(request,id):
    supplier = get_object_or_404(Profile, id=id)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=supplier)
        if form.is_valid():
            data = form.cleaned_data
            supplier = form.save()
            messages.success(request, 'Changes Successfully Updated')
            return redirect('users.index')
    else:
        form = Profile(instance=supplier)
    return render(request, 'users/supplier_edit.html', {'form': form, 'supplier': supplier})

def edit_buyer(request,id):
    buyer = get_object_or_404(Profile, id=id)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=buyer)
        if form.is_valid():
            data = form.cleaned_data
            buyer = form.save()
            messages.success(request, 'Changes Successfully Updated')
            return redirect('users.index')
    else:
        form = Profile(instance=supplier)
    return render(request, 'users/buyer_edit.html', {'form': form, 'buyer': buyer})

def delete_user(request,id):
    supplier = get_object_or_404(Profile, id=id)

    if request.method == 'POST':
        form = ActionForm(request.POST)
        if form.is_valid():
            supplier.delete()
            messages.success(request, 'User Has Been Deleted')
        return redirect('administrator:blog_all_posts')
    form = ActionForm()    

    return render(request, 'user/supplier_delete.html', {'form': form, 'supplier': supplier})










