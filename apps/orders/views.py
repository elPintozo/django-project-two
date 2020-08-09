from django.shortcuts import render
from .models import Order
from apps.carts.utils import get_or_create_cart
from .utils import get_or_create_order

def order(request):
    """
    Función que me ayuda a visualizar una orden de compra
    :param request (None):
    :return (template):
    """
    # diccionario con data para el template
    data = dict()

    # Obtengo el carrito que se está usando
    cart = get_or_create_cart(request)

    # Obtengo la orden de compra
    order = get_or_create_order(request, cart)

    return render(request, 'orders/order.html', data)