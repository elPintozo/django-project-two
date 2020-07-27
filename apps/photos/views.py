from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Photo

# Create your views here.
class PhotoListView(ListView):
    template_name = 'index.html'
    queryset = Photo.objects.all().order_by('-id')

    ##sobreescribo la funcion que pasa los datos del view al template,
    ##para asi poder agregar más data al tempalte
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Fotos'
        context['message'] = 'Lista de Fotos'
        return context