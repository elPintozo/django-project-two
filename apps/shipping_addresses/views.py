from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from .models import ShippingAddress
from .forms import ShippingAddressForm
from ..carts.utils import get_or_create_cart
from ..orders.utils import get_or_create_order


class ShippingAddressListView(LoginRequiredMixin, ListView):
    """
    Clase que ayuda a redireccionar a las direcciones que
    tiene el usuario para realizar el despacho de su orden
    de compra
    """
    #variable que va de la mano con LoginRequiredMixin
    login_url = 'login'

    #indico el model del cual debe conectar
    model = ShippingAddress

    #indico el template sobre cual actuar
    template_name = 'shipping_addresses/shipping_addresses.html'

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user).order_by('-default')

class ShippingAddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Clase que me ayuda a poder cargar la vista para editar
    la dirección de un usuario
    """
    # variable que va de la mano con LoginRequiredMixin
    login_url = 'login'

    # indico el model del cual debe conectar
    model = ShippingAddress

    #indico el form del cual debe tomar para editar los campos
    form_class = ShippingAddressForm

    # indico el template sobre cual actuar
    template_name = 'shipping_addresses/update.html'

    #Hago uso de los message de Django para informar al usuario de que se logró editar
    success_message="Dirección actualizada exitosamente"

    def get_success_url(self):
        """
        Función que me ayuda a indicar a donde redireccionar
        una vez se halla realizado las modificaciones a la
        dirección
        :return (URL):
        """
        return reverse('shipping_addresses:shipping_address')

    def dispatch(self, request, *args, **kwargs):
        """
        Función que me ayuda a realizar validaciones al momento
        de ejecutar la función
        :param request (session):
        :param args (dict):
        :param kwargs (dict):
        :return (redirect):
        """
        #valido si la dirección a editar le corresponde al usuario logueado
        if request.user.id != self.get_object().user_id:
            # si no le corresponde es redireccionado
            return redirect('carts:cart')

        return super(ShippingAddressUpdateView, self).dispatch(request, *args, **kwargs)

class ShippingAddressDeleteView(LoginRequiredMixin, DeleteView):
    """
    Función que me ayuda a eliminar una dirección seleccionada por el usuario
    """
    # variable que va de la mano con LoginRequiredMixin
    login_url = 'login'

    # indico el model del cual debe conectar
    model = ShippingAddress

    # indico el template sobre cual actuar
    template_name = 'shipping_addresses/delete.html'

    #indico donde debe ser redireccionado al momento de realizar la eliminacion
    success_url= reverse_lazy('shipping_addresses:shipping_address')

    def dispatch(self, request, *args, **kwargs):
        """
        Función que me ayuda a realizar validaciones al momento
        de ejecutar la función
        :param request (session):
        :param args (dict):
        :param kwargs (dict):
        :return (redirect):
        """
        #valido que la dirección a eliminar no sea la por defecto
        if self.get_object().default:
            # si no le corresponde es redireccionado
            return redirect('shipping_addresses:shipping_address')

        # valido si la dirección a editar le corresponde al usuario logueado
        if request.user.id != self.get_object().user_id:
            # si no le corresponde es redireccionado
            return redirect('carts:cart')

        return super(ShippingAddressDeleteView, self).dispatch(request, *args, **kwargs)

@login_required(login_url='login')
def create(request):
    """
    Función que me ayuda a crear nu
    :param request:
    :return:
    """
    #diccionario con datos para el template
    data = dict()

    ##inicializamos el formulario
    form = ShippingAddressForm(request.POST or None)

    #valido la solicitud y el formulario
    if request.method=='POST' and form.is_valid():
        #genero una instancia
        shipping_address = form.save(commit=False)
        #asigno el usuario a la dirección
        shipping_address.user = request.user
        #hago a validación de asignación de dirección por defecto
        shipping_address.default = not request.user.has_shipping_address()
        #guardo la instancia en la bd
        shipping_address.save()

        #pregunto si existe la variable en la url ingresada
        if request.GET.get('next'):
            # valido si la variable tiene la url esperada luego de crear una direccion
            if request.GET['next'] == reverse('orders:address'):
                #Como la petición de crear una direccion viene desde una orden
                #se busca la orden y se redicciona para ella nuevamenete

                # Obtengo el carrito que se está usando
                cart = get_or_create_cart(request)
                # Obtengo la orden de compra
                order = get_or_create_order(request, cart)

                #asigno la direccion recien creada a la orden que no contaba con una direccion
                order.update_shipping_address(shipping_address)
                #una vez finalizado el tema de la direccion y orden de compra, redirecciono donde quedo el usuario
                return HttpResponseRedirect(request.GET['next'])

        ##Notifico al usuario de que se ha creado la dirección
        messages.success(request, 'Dirección creada con exitosamente')
        #redirecciono luego de crear la dirección nueva
        return redirect('shipping_addresses:shipping_address')

    #envio el formulario al template
    data['form'] = form

    return render(request, 'shipping_addresses/create.html', data)

@login_required(login_url='login')
def default(request, pk):
    """
    Función que me ayuda a seleccionar una dirección por defecto
    :param request (user):
    :param pk (int): pk de la dirección
    :return (redirect):
    """

    #Obtengo la dirección seleccionada
    shipping_address = get_object_or_404(Shipping_address, pk=pk)

    #valido si la dirección es del usuario
    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')

    #obtengo la dirección anterior para que deje de ser la principal
    if request.user.has_shipping_address():
        request.user.shipping_address.update_default(False)

    #asigno la dirección por defecto
    shipping_address.update_default(True)

    #redirecciono a la vista principal de las direcciones
    return redirect('shipping_addresses:shipping_address')