from django.db import models
from django.contrib.auth.models import User


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