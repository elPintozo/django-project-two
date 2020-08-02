from django.shortcuts import render
from .models import Cart
from .utils import get_or_create_cart

# Create your views here.
def cart(request):
    """
    Función que me ayuda a manegar lo que quiere comprar el usuario
    :param request:
    :return (template):
    """
    #diccionario con data para el template
    data = dict()

    cart = get_or_create_cart(request)

    return render(request, 'carts/cart.html', data)