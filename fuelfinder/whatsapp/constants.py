greetings_message = '''
*Hie {0}, Welcome To Intelli Fuel Finder* 

Intelli Fuel Finder is system that brings together individuals and corporates that are looking for fuel.
You can register on the plartform as a Supplier, Individual Buyer or Corporate Buyer.

To begin the registration process please select one of the below options 

*What would you like to register as*
1. Individual Buyer *_(200 litres and below)_* 
2. Corporate Buyer *_(1000 litres and above)_*
3. Bulk Supplier *_(Any amount)_*


Please Type the desired option to continue. 
'''

user_types=['individual', 'buyer', 'supplier']

successful_integration = '''
You have succesfully integrated your Whatsapp with you company account.

If you want to look for fuel, please type *Menu* 

'''

suggested_choice = '''
Please find the below available supplier for you 

*Company Name*: {0}
*Fuel Type*: {1}
*Quantity*: {2}
*Price*: {3}

To Accept this Offer Type *Accept {4}*

To Wait for offers type *Wait*

Type *Menu* to go back to Menu
'''

new_offer = '''
Please find the below offer for you

*Company Name*: {0}
*Fuel Type*: {1}
*Quantity*: {2}
*Price*: {3}

To Accept this Offer Type *Accept {4}*

To Wait for offers type *Wait*

To Close this request type *Close*

Type *Menu* to go back to Menu
'''

payment_methods=['RTGS', 'ECOCASH', 'SWIPE', 'USD']