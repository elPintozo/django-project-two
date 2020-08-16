from django.urls import path
from .views import ShippingAddressListView

app_name = 'shipping_addresses'

urlpatterns=[
    path('', ShippingAddressListView.as_view(), name='shipping_address')
]