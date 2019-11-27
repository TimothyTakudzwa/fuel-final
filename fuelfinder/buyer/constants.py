from buyer.models import Company

companies = Company.objects.all()
COMPANY_CHOICES = ''
for company in companies: 
    COMPANY_CHOICES = tuple([(company.id, company.name) for company in companies])
        

# COMPANY_CHOICES = (('ZB FINANCIAL HOLDINGS', 'ZB Financial Holdings'),('CBZ FINANCIAL HOLDINGS', 'CBZ Financial Holdings'),('DOVES HOLDINGS ZIMBABWE', 'Doves Holdings Zimbabwe'))
# print(COMPANY_CHOICES)
sender = f'Fuel Finder Accounts<tests@marlvinzw.me>'
subject = 'User Registration'