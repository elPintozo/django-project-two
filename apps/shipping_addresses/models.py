from django.db import models
from apps.users.models import User

# Create your models here.
class Shipping_address(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    line1 = models.CharField(max_length=200)
    line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    reference = models.CharField(max_length=300)
    postal_code = models.CharField(max_length=10, null=False, blank=False)
    default = models.BooleanField(default=False) # True/False Direccion por defecto
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.postal_code

    def address(self):
        """
        Función que me ayuda a desplegar la información de la
        dirección de mejor manera cuando se requiera
        :return (string): city-state-country
        """
        return '{} {} {}'.format(self.city, self.state, self.country)

    def update_default(self, default=False):
        """
        Función que cambia el parametro default
        :param default (boolean):
        :return ():
        """
        self.default = default
        self.save()
