from django.contrib import admin
from .models import Category
# Register your models here.

## indicamos al admin la presencia de nuestro model
## Indicamos los parametros a considerar de nuestro model
admin.site.register(Category)