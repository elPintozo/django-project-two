from django.urls import path
from .views import order, address, select_address, check_address

app_name = 'orders'

urlpatterns =[
    path('', order, name='order'),
    path('direccion', address, name='address'),
    path('seleccionar/direccion', select_address, name='select_address'),
    path('establecer/direcion/<int:pk>', check_address, name='check_address')
]