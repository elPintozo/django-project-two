from .models import Order

def get_or_create_order(request, cart):
    """
    Función que me ayuda con la gestión de la orden de compra
    evalua si existe sino la crea
    :param request (session): obtengo el usuario logueado si es que existe
    :param cart (Cart): carrito actual del usuario
    :return (Order): retorno la orden existente o la nueva que se ha creado
    """

    # Obtengo la orden de compra del carrito
    order = Order.objects.filter(cart=cart).first()

    # valido si existe una orden, sino se crea una
    if order is None and request.user.is_authenticated:
        order = Order.objects.create(cart=cart, user=request.user)

    if order:
        # Agrego el id de la orden a la sesión
        request.session['order_id'] = order.id

    return order