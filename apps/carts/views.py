from django.shortcuts import render
from .models import Cart
# Create your views here.
def cart(request):
    """
    Función que me ayuda a manegar lo que quiere comprar el usuario
    :param request:
    :return (template):
    """
    #diccionario con data para el template
    data = dict()

    #obtengo la instancia del user registrado
    user = request.user if request.user.is_authenticated else None

    #obtengo el id del carrito
    cart_id = request.session.get('cart_id')

    #valido si hay un carrito
    if cart_id:
        #el usuario posee un carrito de compra
        cart = Cart.objects.get(cart_id=int(cart_id))
    else:
        #si el usuario no tiene un carrito se le asigna uno
        cart = Cart.objects.create(user=user)


    request.session['cart_id'] =cart.cart_id

    return render(request, 'carts/cart.html', data)