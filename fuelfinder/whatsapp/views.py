from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from supplier.models import Profile
from .helper_functions import bot_action, send_message
from django.views.decorators.csrf import csrf_exempt
import json 

@csrf_exempt 
def index(request):

    token = request.GET.get('token')
    data = json.loads(request.body)
    message = data['messages'][0]['body']
    
    phone_number = data['messages'][0]['author'].split('@')[0]
    if phone_number == '263718055061':
        return HttpResponse('')
    print(message, phone_number)
    # message = data['message']
    # phone_number = data['phone_number']
    token = 'sq0pk8hw4iclh42b'
    if token != 'sq0pk8hw4iclh42b':
        return HttpResponse('Unauthorized')
    else:
        check = Profile.objects.filter(phone_number = phone_number).exists()
        if check:
            user = Profile.objects.filter(phone_number=phone_number).first()
            if user.name.is_active:
                response_message = bot_action(user, message)                
            else:
                response_message = "Your cannot use this, please create a buyer account and then add the phone number"
        else:
            response_message = "We could not find an account associated with you"

    send_message(phone_number, response_message)
    return HttpResponse(response_message)
