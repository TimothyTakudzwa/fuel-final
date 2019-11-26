from django.shortcuts import render
import requests
from validate_email import validate_email
from .constants import *
from buyer.views import token_is_send
from supplier.models import FuelRequest, Offer, Transaction
from finder.reccomend import recommend
# from django.core.validators import validate_email
from buyer.models import User


def send_message(phone_number, message):
    payload = {
        "phone": phone_number,
        "body": message
    }
    url = "https://eu33.chat-api.com/instance78632/sendMessage?token=sq0pk8hw4iclh42b"
    r = requests.post(url=url, data=payload)
    print(r)
    return r.status_code


def bot_action(request, user, message):
    if message.lower() == 'menu' and user.stage != 'registration':
        user.position = 1
        user.stage = 'requesting'
        user.save()
        return requests_handler(user, message)
    if user.stage == 'registration':
        response_message = registration_handler(request, user, message)
    elif user.stage == 'requesting':
        response_message = requests_handler(user, message)
    elif user.stage == 'transacting':
        response_message = transacting_handler(user, message)
    else:
        response_message = ''
    return response_message


def registration_handler(request, user, message):
    if user.position == 1: 
       response_message = greetings_message
       user.position = 2
       user.save()
    elif user.position == 2: 
        
    elif user.position ==3 : 
        response_message = "Can i have your company email address.\n*NB* using your personal email address gets you lower precedence in the fuel finding process"
        try:
            user.first_name, user.last_name = message.split(' ', 2)
        except:
            user.first_name = message 
        user.position = 4
        user.save()
    elif user.position == 4:
        # if 'gmail' in message or 'yahoo' in message: 
        #     return "Please type in your company email address"
      
        is_valid = validate_email(message, verify=True)
        print("******************************",is_valid)
        if is_valid is None:           
            pass
        else: 
            return "*_This email does not exist_*.\n\nPlease enter the a valid email address"         
        response_message = "What kind of user are your.\n\n1. Fuel Supplier\n2. Fuel Buyer"
        user.email = message
        user.position = 4 
        user.save()
    elif user.position == 4:
        response_message = "We have sent a verification email to your supplied email, Please visit the link to complete the registration process"
        user.user_type = 'Supplier' if message == "1" else "Buyer"
        username =initial_username = user.first_name[0] + user.last_name 
        i = 0
        while User.objects.filter(username=username.lower()).exists():
            username = initial_username + str(i)
        user.position = 4 
        user.save()
        if token_is_send(request, user):
            response_message = "We have sent a verification email to your supplied email, Please visit the link to complete the registration process"
            user.is_active = True
            user.save()
        else:
            response_message = "*_We have failed to register you to the platform_*.\n\nPlease enter a valid email address"
            user.position = 3
            user.save()
    return response_message


def requests_handler(user, message):    
    if user.position == 1:
        response_message = "Which type of fuel do you want\n\n1. Petrol\n2. Diesel"
        user.position = 3
        user.save()
    elif user.position == 2:
        try:
            selected_option = user_types[int(message)]
        except Ec
    elif user.position == 3:
        response_message = "How many litres do you want?"
        fuel_type = "Petrol" if message == '1' else "Diesel"
        fuel_request = FuelRequest.objects.create(fuel_type=fuel_type, name=user.name)
        user.fuel_request = fuel_request
        user.position = 4
        user.save()
    elif user.position == 4:
        fuel_request = FuelRequest.objects.get(id=user.fuel_request.id)
        fuel_request.amount = message
        fuel_request.save()
        user.position = 5
        user.save()
        response_message = "*Please select delivery method*\n\n1. Pick Up\n2. Delivery"       
    elif user.position == 5: 
        delivery_method = "SELF COLLECTION" if message == '1' else "DELIVERY"
        fuel_request = FuelRequest.objects.get(id=user.fuel_request.id)
        fuel_request.delivery_method = delivery_method
        fuel_request.save()
        user.position = 6 
        user.save()
        response_message = 'What is your payment method.\n\n1. ZWL(Cash)\n2. Ecocash\n3. RTGS(Swipe)/Transfer\n'
    elif user.position == 6:
        choice = payment_methods[int(message)]
        fuel_request = FuelRequest.objects.get(id=user.fuel_request.id)
        fuel_request.payment_method = choice
        fuel_request.save()
        response = recommend(fuel_request.fuel_type, fuel_request.amount, user.name.id, fuel_request.price)
        if response == False:
            pass
        else:
            offer = Offer.objects.filter(id=response).first()
            response_message = suggested_choice.format(offer.supplier.company.name, offer.request.fuel_type, offer.quantity, offer.price, offer.id)
        
        response_message = suggested_choice
    return response_message

def transacting_handler(user, message):
    if user.position == 1:
        if 'accept' in message.lower():
            offer_id = ''.join(x for x in message if x.isdigit())
            offer =  Offer.objects.filter(id=offer_id).first()
            if offer is not None:
                Transaction.objects.create(request_name=offer.request, buyer_name=user)
                response_message = 'This transaction has been completed'
        elif message.lower() == 'wait':
            pass
    return response_message




def fuel_finder():
    return 