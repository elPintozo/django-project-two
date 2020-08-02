from django.contrib import admin
from .models import Profile
from .models import User
from django.contrib.auth.admin import UserAdmin

## indicamos al admin la presencia de nuestro model
## Indicamos los parametros a considerar de nuestro model
admin.site.register(Profile)
admin.site.register(User, UserAdmin)

