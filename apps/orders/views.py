from django.shortcuts import render, get_object_or_404, redirect
from apps.carts.utils import get_or_create_cart
from apps.shipping_addresses.models import ShippingAddress
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

    #obtengo la dirección de envio de la orden
    shipping_address = order.get_or_set_shipping_address()

    #variables para el template
    data['cart'] = cart
    data['order'] = order
    data['breadcrumb'] = breadcrumb(addres=True)
    data['shipping_address'] = shipping_address

    return render(request, 'orders/address.html', data)

@login_required(login_url='login')
def select_address(request):
    """
    Función que me ayuda a asociar una dirección diferente
    a la por defecto a una orden
    :param request ():
    :return:
    """
    # diccionario con data para el template
    data = dict()

    # obtengo las direcciones del usuario, las cuales podrá seleccionar
    shipping_addresses = request.user.shippingaddress_set.all()

    # variables para el template
    data['breadcrumb'] = breadcrumb(addres=True)
    data['shipping_addresses'] = shipping_addresses

    return render(request, 'orders/select_address.html', data)

@login_required(login_url='login')
def check_address(request, pk):
    """
    Funcion que establece una dirección particular a una
    orden
    :param request ():
    :param pk (int): pk de una dirección particular
    :return:
    """
    # diccionario con data para el template
    data = dict()

    # Obtengo el carrito que se está usando
    cart = get_or_create_cart(request)

    # Obtengo la orden de compra
    order = get_or_create_order(request, cart)

    #obtengo la dirección seleccionada por el usuario
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)

    # valido si la dirección le corresponde al usuario logueado
    if request.user.id != shipping_address.user_id:
        return redirect('carts:cats')

    ##asigno la dirección seleccionada a la orden actual
    order.update_shipping_address(shipping_address)

    return redirect('orders:address')