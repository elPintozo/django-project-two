from django.shortcuts import render
from .models import Order
from apps.carts.utils import get_or_create_cart
from .utils import get_or_create_order, breadcrumb
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
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

    #variables utilizadas en template
    data['cart'] = cart
    data['order'] = order
    data['breadcrumb'] = breadcrumb()

    return render(request, 'orders/order.html', data)

@login_required(login_url='login')
def address(request):
    """
    Función que me ayud a establecer la relación entre
    una orden y una dirección
    :param request ():
    :return ():
    """
    # diccionario con data para el template
    data = dict()

    # Obtengo el carrito que se está usando
    cart = get_or_create_cart(request)

    # Obtengo la orden de compra
    order = get_or_create_order(request, cart)

    #variables pra el template
    data['cart'] = cart
    data['order'] = order
    data['breadcrumb'] = breadcrumb(addres=True)

    return render(request, 'orders/address.html', data)
