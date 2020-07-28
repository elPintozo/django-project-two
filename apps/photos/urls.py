from django.urls import path
from .views import PhotoDetailView, PhotoSearchListView

urlpatterns = [
    path('search', PhotoSearchListView.as_view(), name='product_search'),
    path('<slug:slug>', PhotoDetailView.as_view(), name='product_detail')
]