from .models import Order
from django.urls import reverse

def get_or_create_order(request, cart):
    """
    Función que me ayuda con la gestión de la orden de compra
    evalua si existe sino la crea
    :param request (session): obtengo el usuario logueado si es que existe
    :param cart (Cart): carrito actual del usuario
    :return (Order): retorno la orden existente o la nueva que se ha creado
    """

    # Obtengo la orden de compra del carrito
    order = cart.order

    # valido si existe una orden, sino se crea una
    if order is None and request.user.is_authenticated:
        order = Order.objects.create(cart=cart, user=request.user)

    if order:
        # Agrego el id de la orden a la sesión
        request.session['order_id'] = order.order_id

    return order

def breadcrumb(products=True, addres=False, payment=False, confirmation=False):
    """
    Funcion que me ayudará a generar de forma dinámica los enlaces para mi
    breadcrumb
    :param products (Boolean):indica si debe aparecer o no
    :param addres (Boolean):indica si debe aparecer o no
    :param payment (Boolean):indica si debe aparecer o no
    :param confirmation (Boolean): indica si debe aparecer o no
    :return (list): lista con los parametros de cada uno de los pasos
    """
    return [
        {'title': 'Productos', 'active': products, 'url': reverse('orders:order')},
        {'title': 'Dirección', 'active': addres, 'url': reverse('orders:order')},
        {'title': 'Pago', 'active': payment, 'url': reverse('orders:order')},
        {'title': 'Confirmación', 'active': confirmation, 'url': reverse('orders:order')},
    ]