from buyer.models import *
from supplier.models import *
from user.models import *

def get_hot_client(supplier_id):
    clients = clients.objects.all()
    request_count = 0
    for client in clients:
        