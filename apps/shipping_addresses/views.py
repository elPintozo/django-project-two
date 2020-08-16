from django.shortcuts import render
from django.views.generic import ListView
from .models import Shipping_address

# Create your views here.
class ShippingAddressListView(ListView):

    model = Shipping_address
    template_name = 'shipping_addresses/shipping_addresses.html'

    def get_queryset(self):
        return Shipping_address.objects.filter(user=self.request.user).order_by('-default')