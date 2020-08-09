from django.db import models
from apps.users.models import User
from apps.photos.models import Photo
from django.db.models.signals import pre_save, m2m_changed, post_save
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
        self.subtotal = sum( [ cp.quantity * cp.photo.price for cp in self.photo_related() ] )
        self.save()

    def update_total(self):
        """
        Función que calcula el total más la comision asociada y ya definida
        :return:
        """
        self.total = self.subtotal * decimal.Decimal(Cart.COMISION)
        self.save()

    def photo_related(self):
        """
        Funcion que me retorna una queryset entre la instancia actual Cart
        con la clase CartPhotos
        :return (queyset):
        """
        return self.cartphotos_set.select_related('photo')

class CartPhotosManager(models.Manager):

    def create_or_update_quantity(self, cart, photo, quantity=1):
        """
        Función que me ayuda a crear o modificar un parametro del registro
        CartPhotos
        :param cart (Cart): cart del usuario
        :param photo (Photo): foto que selecciono para agregar
        :param quantity (int): cantidad a comprar
        :return (CartPhotos): registro que fue creado y/o modificado
        """
        #get_or_create: la funcion se encarga de crear o obtener el objeto con esos parametros
        object, created = self.get_or_create(cart=cart, photo=photo)

        #valido si ya existe el registro con esos campos
        if not created:
            #actualizo uno de sus parametros
            quantity = object.quantity + quantity

        object.update_quantity(quantity)
        return object

class CartPhotos(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    create_at = models.DateTimeField(auto_now_add=True)

    #Indico la clase que me ayudará con el objects en las queryset
    objects = CartPhotosManager()

    def update_quantity(self, quantity=1):
        self.quantity =quantity
        self.save()

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

def post_save_update_totals(sender, instance, *args, **kwargs):
    instance.cart.update_totals()

#Asigno al pre_save la función que actuará antes de guardar, e indico a que class corresponde
pre_save.connect(set_cart_id, sender=Cart)

#Asigno al post_save la función que actuará después de guardar, e indico a que class corresponde
post_save.connect(post_save_update_totals, sender=CartPhotos)

#Asigno al m2m_changed la función que actuará antes actualizaciones de .photos, e indico a que class corresponde
m2m_changed.connect(update_totals, sender=Cart.photos.through)

