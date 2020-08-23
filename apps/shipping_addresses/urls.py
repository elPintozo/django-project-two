from django.urls import path
from .views import ShippingAddressListView, create, ShippingAddressUpdateView, ShippingAddressDeleteView

app_name = 'shipping_addresses'

urlpatterns=[
    path('', ShippingAddressListView.as_view(), name='shipping_address'),
    path('nuevo', create, name='create'),
    path('editar/<int:pk>', ShippingAddressUpdateView.as_view(), name='update'),
    path('eliminar/<int:pk>', ShippingAddressDeleteView.as_view(), name='delete')
]