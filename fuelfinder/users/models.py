from django.db import models
from django.dispatch import receiver

from supplier.models import *

from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages

class SupplierContact(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    supplier_profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    telephone = models.CharField(max_length=300, blank=True)
    cellphone = models.CharField(max_length=300, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['user__last_name']

    def __str__(self):
        return self.cellphone

    def disable(self):
        self.user.active = False
        self.user.save()
        self.active = False
        self.save()

    def enable(self):
        self.user.active = True
        self.user.save()
        self.active = True
        self.save()

class BuyerContact(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    buyer_profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    phone = models.CharField(max_length=300, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['user__last_name']

    def __str__(self):
        return self.phone

    def disable(self):
        self.user.active = False
        self.user.save()
        self.active = False
        self.save()

    def enable(self):
        self.user.active = True
        self.user.save()
        self.active = True
        self.save()

