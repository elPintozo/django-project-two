from django.urls import path
from .views import cart, add

app_name='carts'

urlpatterns = [
    path('', cart, name='cart'),
    path('add', add, name='add')
]