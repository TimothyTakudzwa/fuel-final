from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('suppliers/', views.suppliers_list, name="suppliers_list"),
    path('buyers/', views.buyers_list, name="buyers_list"),
    path('supplier_user_create/<int:sid>', views.supplier_user_create, name="supplier_user_create"),
    path('buyer_user_create/<int:sid>', views.buyer_user_create, name="buyer_user_create"),
    path('supplier_user_delete/<int:sid>', views.suppliers_delete, name="suppliers_delete"),
    path('buyer_user_delete/<int:sid>', views.buyers_delete, name="buyers_delete"),
    path('supplier_user_delete/<int:cid>/<int:sid>', views.supplier_user_delete, name="supplier_user_delete"),


    # path('/index/', views.index, name="home")
    # path('/index/', views.index, name="home")

]