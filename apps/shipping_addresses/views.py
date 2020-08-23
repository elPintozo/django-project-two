from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import ListView

from .models import Shipping_address
from .forms import ShippingAddressForm


class ShippingAddressListView(LoginRequiredMixin, ListView):
    """
    Clase que ayuda a redireccionar a las direcciones que
    tiene el usuario para realizar el despacho de su orden
    de compra
    """
    #variable que va de la mano con LoginRequiredMixin
    login_url = 'login'

    model = Shipping_address
    template_name = 'shipping_addresses/shipping_addresses.html'

    def get_queryset(self):
        return Shipping_address.objects.filter(user=self.request.user).order_by('-default')

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
        shipping_address.default = not Shipping_address.objects.filter(user=request.user).exists()
        #guardo la instancia en la bd
        shipping_address.save()

        ##Notifico al usuario de que se ha creado la dirección
        messages.success(request, 'Dirección creada con exitosamente')
        #redirecciono luego de crear la dirección nueva
        return redirect('shipping_addresses:shipping_address')

    #envio el formulario al template
    data['form'] = form

    return render(request, 'shipping_addresses/create.html', data)