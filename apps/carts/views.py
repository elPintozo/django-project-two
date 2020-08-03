from django.shortcuts import render
from .models import Cart
from .utils import get_or_create_cart
from apps.photos.models import Photo

# Create your views here.
def cart(request):
    """
    Función que me ayuda a manegar lo que quiere comprar el usuario
    :param request:
    :return (template):
    """
    #diccionario con data para el template
    data = dict()

    #Obtengo el carrito que se está usando
    cart = get_or_create_cart(request)

    return render(request, 'carts/cart.html', data)

def add(request):
    """
    Función para agregar photos al carrito de compra
    :param request (POST):
    :return (template):
    """
    #diccionario con data para el template
    data = dict()

    # Obtengo el carrito que se está usando
    cart = get_or_create_cart(request)

    # Obtengo la photo del articulo que se quiere agregar al carrito
    photo = Photo.objects.get(pk=request.POST.get('photo_id'))

    #asocio la foto al carrito
    cart.photos.add(photo)

    data['photo']=photo
    return render(request, 'carts/add.html', data)