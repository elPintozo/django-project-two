from django.db import models
from apps.users.models import User
from apps.photos.models import Photo

# Create your models here.
class Cart(models.Model):
    #Una relacion uno a muchos
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    #Una relacion muchos a muchos
    photos = models.ManyToManyField(Photo)
    total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    subtotal = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ''
