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