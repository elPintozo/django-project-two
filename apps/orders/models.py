import uuid
from django.db import models
from enum import Enum
from apps.users.models import User
from apps.carts.models import Cart
from apps.shipping_addresses.models import ShippingAddress
from django.db.models.signals import pre_save

# Create your models here.
class OrderStatus(Enum):
    CREATED = 'CREATED'
    PAYED = 'PAYED'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'

##opciones disponibles a partir de un Enum
choices = [ (tag, tag.value) for tag in OrderStatus]

class Order(models.Model):
    order_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=50,
                              choices=choices,
                              default=OrderStatus.CREATED)
    shipping_total = models.DecimalField(default=5,
                                         max_digits=8,
                                         decimal_places=2)
    total = models.DecimalField(default=5,
                                max_digits=8,
                                decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(ShippingAddress,
                                         null=True,
                                         blank=True,
                                         on_delete=models.CASCADE)

    ##la forma en como será visible el objeto al momento de ser pasado a string
    def __str__(self):
        return self.order_id

    def get_or_set_shipping_address(self):
        """
        Funcion que me ayuda a gestionar el tema de la dirección asociada
        a un registro de orden
        :return (ShippingAddress):
        """
        ## si ya posee una dirección se le retorna esa
        if self.shipping_address:
            return self.shipping_address

        #Obtengo la dirección por defecto del usuario
        shipping_address = self.user.shipping_address

        ##Si tiene una dirección por defecto se le asociará esa
        if shipping_address:
            #asigno esa dirección por defecto a la orden
            self.update_shipping_address(shipping_address)

        return shipping_address

    def update_shipping_address(self, shipping_address):
        """
        Función que me ayuda a reasignar una dirección a una
        orden
        :param shipping_address (ShippingAddress):
        :return (None):
        """
        self.shipping_address = shipping_address
        self.save()

    def update_total(self):
        """
        Función que me ayuda a mantener el
        total actualizado
        :return (None):
        """
        self.total = self.get_total()
        self.save()

    def get_total(self):
        """
        Función que suma los totales tanto del carrito
        como del envio de la orden
        :return (int): total
        """
        return self.cart.total +self.shipping_total


def set_order_id(sender, instance, *args, **kwargs):
    """
    Función que me ayuda a generar un identificador
    cada vez que se crea un Object Order
    :param sender (Class): sobre que Class se aplicará el cambio
    :param instance (Object): La instancia que se creará
    :param args (list): otros parametros
    :param kwargs (list): otros parametros
    :return (None):
    """
    # Se valida si ya posee un order_id
    if not instance.order_id:
        # uuid.uuid4(): nos permite crear un identificador unico
        instance.order_id = str(uuid.uuid4())

def set_total(sender, instance, *args, **kwargs):
    """
    Función que me ayuda a generar generar el total
    de la orden al momento de guardar la orden
    :param sender (Class): sobre que Class se aplicará el cambio
    :param instance (Object): La instancia que se creará
    :param args (list): otros parametros
    :param kwargs (list): otros parametros
    :return (None):
    """
    instance.total = instance.get_total()

#Asigno al pre_save la función que actuará antes de guardar, e indico a que class corresponde
pre_save.connect(set_order_id, sender=Order)
pre_save.connect(set_total, sender=Order)