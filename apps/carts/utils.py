from .models import Cart

def get_or_create_cart(request):
    """
    Función que me ayuda a evaluar si exite o no un carrito
    y si este se encuentra asignado a un usuario
    :param request (session):
    :return (Cart): retorna un carrito de compra
    """
    #obtengo la instancia del user registrado
    user = request.user if request.user.is_authenticated else None
    #obtengo el id del carrito
    cart_id = request.session.get('cart_id')
    #Obtengo el carrito de compra
    cart = Cart.objects.filter(cart_id=cart_id).first()

    #Valido si existe ya un carrito
    if cart is None:
        #Se crea el carrito con o sin user, de no haber pillado no
        cart = Cart.objects.create(user=user)

    #si el carrito existe y luego se loguea alguien y el carrito
    #esta sin user, este se le asigna
    if user and cart.user is None:
        cart.user = user
        cart.save()

    #Paso el id al carrito
    request.session['cart_id']= cart.cart_id

    return cart

