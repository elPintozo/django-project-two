from django.contrib import admin
from .models import Photo

#Clase que no ayuda a indicar al admin que
#campos considerar del modelo
class PhotoAdmin(admin.ModelAdmin):

    ##Solo estos campos serán visibles en el admin
    fields = ('title',
              'description',
              'price',
              'stock',)

    ##indicamos los campos a mostrar al momento de listar
    list_display = ('__str__', 'slug', 'create_at',)

## indicamos al admin la presencia de nuestro model
## Indicamos los parametros a considerar de nuestro model
admin.site.register(Photo, PhotoAdmin)

