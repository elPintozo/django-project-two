from django.db import models
from apps.photos.models import Photo


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    photos = models.ManyToManyField(Photo, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    ##la forma en como será visible el objeto al momento de ser pasado a string
    def __str__(self):
        return self.title

"""
Tips para extraer los datos de la bd:
En la terminal

##Obtener toda la información de toda la base de datos
- python3 manage.py dumpdata 

# obtener la información de todos los registros de Category
- python3 manage.py dumpdata categories.Category 

# obtener la información de todos los registros de Category en formato Json
- python3 manage.py dumpdata categories.Category --format=json 

# obtener la información de todos los registros de Category en formato Json
- python3 manage.py dumpdata categories.Category --format=json
 
# obtener la información de todos los registros de Category en formato Json y con una visualizacion en terminal
- python3 manage.py dumpdata categories.Category --format=json --indent=4

# obtener la información de todos los registros de Category en formato Json y con una visualizacion en terminal
- python3 manage.py dumpdata categories.Category --format=json --indent=4 > apps/categories/fixtures/categories_072020.json

# para cargar la data ya almacenada dentro de un Json en el proyecto/ loaddata inspecciona las carpetas fixture de cada app
- python3 manage.py loaddata categories072020.json
"""