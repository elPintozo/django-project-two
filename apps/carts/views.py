from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartPhotos
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

    data['cart'] = cart
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
    # photo = Photo.objects.get(pk=request.POST.get('photo_id'))
    photo = get_object_or_404(Photo, pk=request.POST.get('photo_id'))

    #obtengo la cantidad solicitada
    quantity = int(request.POST.get('quantity', 1))

    #asocio la foto al carrito
    cart_photo = CartPhotos.objects.create_or_update_quantity(cart=cart,
                                                              photo=photo,
                                                              quantity=quantity)

    data['photo'] = photo
    data['quantity'] = quantity
    return render(request, 'carts/add.html', data)

def remove(request):
    """
    Función que me ayuda a eliminar una photo del
    carrito de compra
    :param request (POST):
    :return (redirect):
    """
    # diccionario con data para el template
    data = dict()

    # Obtengo el carrito que se está usando
    cart = get_or_create_cart(request)

    # Obtengo la photo del articulo que se quiere agregar al carrito
    #photo = Photo.objects.get(pk=request.POST.get('photo_id'))
    photo = get_object_or_404(Photo, pk=request.POST.get('photo_id'))

    #elimini la relación de la photo con el carrito
    cart.photos.remove(photo)

    return redirect('carts:cart')