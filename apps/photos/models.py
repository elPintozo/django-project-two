from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save

# Create your models here.
class Photo(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0) #12345678.00
    create_at = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField()
    slug = models.SlugField(null=False, blank=False, unique=True)

    # def save(self, *args, **kwargs):
    #     ## haciendo uso de una funcion, notificamos que haga el slug a partir del titulo
    #     self.slug = slugify(self.title)
    #     super(Photo, self).save(*args, **kwargs)

    ##la forma en como será visible le objeto al momento de ser pasado a string
    def __str__(self):
        return self.title

def set_slug(sender, instance, *args, **kwargs):
    """
    Función que ayuda a generar el parametro slug de un object
    Photo antes de ser creado.

    ##se hace uso de una de las funciones -callback- para poder generar el slug antes de
    ##crear una instancia de "Photo"

    :param sender (Class): se indica la clase que se sobreescribirá un parametro
    :param instance (Photo): instancia del objeto acrear
    :return:
    """
    instance.slug = slugify(instance.title)

##Se le indica al pre_save que función correr antes de hacer el save() y sobre que Objects
pre_save.connect(set_slug, sender=Photo)