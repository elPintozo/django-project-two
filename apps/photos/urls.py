from django.urls import path
from .views import PhotoDetailView

urlpatterns = [
    path('<slug:slug>', PhotoDetailView.as_view(), name='product_detail')
]