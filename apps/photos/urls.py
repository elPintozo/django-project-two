from django.urls import path
from .views import PhotoDetailView, PhotoSearchListView

##Al declarar el app_name, evitamos problemas de duplicado de nombre
app_name = 'photos'

urlpatterns = [
    path('search', PhotoSearchListView.as_view(), name='product_search'),
    path('<slug:slug>', PhotoDetailView.as_view(), name='product_detail')
]