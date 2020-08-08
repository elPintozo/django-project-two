from django.db import models
from apps.users.models import User
from apps.photos.models import Photo
from django.db.models.signals import pre_save, m2m_changed
import uuid
import decimal

# Create your models here.
class Cart(models.Model):
    #Para no exponer nuestro id de carrito se hace uso de otro identificardor de carrito
    cart_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    #Una relacion uno a muchos
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    #Una relacion muchos a muchos
    photos = models.ManyToManyField(Photo, through='CartPhotos')
    total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    subtotal = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)

    #Comision
    COMISION=1.05 #5%

    def __str__(self):
        return self.cart_id

    def update_totals(self):
        """
        Función que actualiza el total a partir de un subtotal
        :return:
        """
        self.update_subtotal()
        self.update_total()

    def update_subtotal(self):
        """
        Función que suma los precios de las photos asociadas a un registro Cart
        :return:
        """
        ##Sumo el precio de todos las photo relacionadas con el registro Cart actual
        self.subtotal = sum( [ photo.price for photo in self.photos.all() ] )
        self.save()

    def update_total(self):
        """
        Función que calcula el total más la comision asociada y ya definida
        :return:
        """
        self.total = self.subtotal * decimal.Decimal(Cart.COMISION)
        self.save()

class CartPhotos(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    create_at = models.DateTimeField(auto_now_add=True)

def set_cart_id(sender, instance, *args, **kwargs):
    """
    Función que me ayuda a generar un identificador
    cada vez que se crea un Object Cart
    :param sender (Class): sobre que Class se aplicará el cambio
    :param instance (Object): La instancia que se creará
    :param args (list): otros parametros
    :param kwargs (list): otros parametros
    :return (None):
    """
    #Se valida si ya posee un cart_id
    if not instance.cart_id:
        #nos ayuda a generar un identificador, no retorna un object
        instance.cart_id = str(uuid.uuid4())

def update_totals(sender, instance, action, *args, **kwargs):
    """
    Funcion que me ayuda a capturar el momento en que se lleva a
    cabo modificaciones en el parametro photos de algun registro
    Cart.
    :param sender (Class):
    :param instance (Object):
    :param action (string):
    :param args (string):
    :param kwargs (dict):
    :return ():
    """
    # post_add: accion cuando se agrega una nueva asociacion en photos
    # post_remove: accion cuando se remueve una asociacion en photos
    # post_clear: actualizacin general de campo photos
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        instance.update_totals()

#Asigno al pre_save la función que actuará antes de guardar, e indico a que class corresponde
pre_save.connect(set_cart_id, sender=Cart)

#Asigno al m2m_changed la función que actuará antes actualizaciones de .photos, e indico a que class corresponde
m2m_changed.connect(update_totals, sender=Cart.photos.through)

