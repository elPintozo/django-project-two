import uuid
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
    image = models.ImageField(upload_to='photos/', null=False, blank=False)

    # def save(self, *args, **kwargs):
    #     ## haciendo uso de una funcion, notificamos que haga el slug a partir del titulo
    #     self.slug = slugify(self.title)
    #     super(Photo, self).save(*args, **kwargs)

    ##la forma en como será visible el objeto al momento de ser pasado a string
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
    #valido que el objeto tenga titulo para poder hacer el slug
    if instance.title and not instance.slug:

        #genero un slug para la instancia
        slug = slugify(instance.title)

        #valido que el slug no exista entre los ya existentes
        while Photo.objects.filter(slug=slug).exists():

            ##genero el slug con un formato diferente para evitar duplicados
            slug = slugify('{}-{}'.format(instance.title, str(uuid.uuid4())[:8]))

        #asigno el slug creado a la instancia
        instance.slug = slug

##Se le indica al pre_save que función correr antes de hacer el save() y sobre que Objects
pre_save.connect(set_slug, sender=Photo)


"""
Tips para extraer los datos de la bd:
En la terminal

##Obtener toda la información de toda la base de datos
- python3 manage.py dumpdata 

# obtener la información de todos los registros de Photo
- python3 manage.py dumpdata photos.Photo 

# obtener la información de todos los registros de Photo en formato Json
- python3 manage.py dumpdata photos.Photo --format=json 

# obtener la información de todos los registros de Photo en formato Json y con una visualizacion en terminal
- python3 manage.py dumpdata photos.Photo --format=json --indent=4

# obtener la información de todos los registros de Photo en formato Json y con una visualizacion en terminal
- python3 manage.py dumpdata photos.Photo --format=json --indent=4 > apps/photos/fixtures/photos_072020.json

# para cargar la data ya almacenada dentro de un Json en el proyecto/ loaddata inspecciona las carpetas fixture de cada app
- python3 manage.py loaddata photos_072020.json
"""