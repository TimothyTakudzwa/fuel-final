from django.contrib import admin
from buyer.models import Profile, User, Company

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username','first_name', 'last_name', 'phone_number')

# Register your models here.
admin.site.register(Profile)
admin.site.register(User, UserAdmin)
# admin.site.register(Company)

