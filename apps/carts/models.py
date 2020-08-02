from django.db import models
from apps.users.models import User
from apps.photos.models import Photo
from django.db.models.signals import pre_save
import uuid

# Create your models here.
class Cart(models.Model):
    #Para no exponer nuestro id de carrito se hace uso de otro identificardor de carrito
    cart_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    #Una relacion uno a muchos
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    #Una relacion muchos a muchos
    photos = models.ManyToManyField(Photo)
    total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    subtotal = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

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

#Asigno al pre_save la función que actuará antes de guardar, e indico a que class corresponde
pre_save.connect(set_cart_id, sender=Cart)

