from django.shortcuts import render

# Create your views here.
def cart(request):
    """
    Función que me ayuda a manegar lo que quiere comprar el usuario
    :param request:
    :return (template):
    """
    #diccionario con data para el template
    data = dict()

    #Se crea una sesión para el usuario
    request.session['cart_id'] = '1'

    return render(request, 'carts/cart.html', data)