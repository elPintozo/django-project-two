from django.db import models
from django.contrib.auth.models import AbstractUser

#Ejemplo de Sobrescribir un Model Django por completo
"""
Podemos hacer uso de dos models:
-AbstractUser: este nos ayuda a acceder y modificar
    -username
    -first_name
    -last_name
    -email
    -password
    -groups
    -user_permissions
    -is_staff
    -is_active
    -is_superuser
    -last_login
    -date_joined

-AbstractBaseUser
    -id
    -password
    -last_login
"""
class User(AbstractUser):

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

##Ejemplo de un Proxy Model: Un models que hereda de otro y no genera una tabla nueva
class Customer(User):

    #Indico que será un proxy model
    class Meta:
        proxy = True

    #Esta funcion aplica para los Object de tipo User
    def get_photos(self):
        """
        Función que me retorna las fotos compradas por los usuarios
        :return (list):
        """
        return []

class Profile(models.Model):
    # on_delete: indica a django que si el user asociado es elimiado, el Profile también se va con el.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField()
