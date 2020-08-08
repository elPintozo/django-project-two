from django.urls import path
from .views import cart, add, remove

app_name='carts'

urlpatterns = [
    path('all', cart, name='cart'),
    path('add', add, name='add'),
    path('remove', remove, name='remove')
]