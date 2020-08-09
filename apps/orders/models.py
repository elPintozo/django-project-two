from django.db import models
from enum import Enum
from apps.users.models import User
from apps.carts.models import Cart

# Create your models here.
class OrderStatus(Enum):
    CREATED = 'CREATED'
    PAYED = 'PAYED'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'

##opciones disponibles a partir de un Enum
choices = [ (tag, tag.value) for tag in OrderStatus]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=50,
                              choices=choices,
                              default=OrderStatus.CREATED)
    shipping_total = models.DecimalField(default=5,
                                         max_digits=8,
                                         decimal_places=2)
    total = models.DecimalField(default=5,
                                max_digits=8,
                                decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)

    ##la forma en como será visible el objeto al momento de ser pasado a string
    def __str__(self):
        return ''
