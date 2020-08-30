from django.urls import path
from .views import order, address

app_name = 'orders'

urlpatterns =[
    path('', order, name='order'),
    path('direccion', address, name='address')
]