from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Photo

# Create your views here.
class PhotoListView(ListView):
    """
    Clase que me ayuda listar un determinado
    grupo de elementos de un Models en particular
    en un template
    """

    #se indica sobre que template se desplegará la información
    template_name = 'index.html'

    ##se indica el listado de registros a mostrar
    queryset = Photo.objects.all().order_by('-id')

    ##sobreescribo la funcion que pasa los datos del view al template,
    ##para asi poder agregar más data al tempalte
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Fotos'
        context['message'] = 'Lista de Fotos'
        return context

class PhotoDetailView(DetailView):
    """
    Clase que me ayuda a visualizar en un template los detalles de un Objeto
    en particular de un models
    """

    ##se indica a la clase el modelo del cual obtener los detalles
    model = Photo

    # se indica sobre que template se desplegará la información
    template_name = 'photos/photo.html'

    ##sobreescribo la funcion que pasa los datos del view al template,
    ##para asi poder agregar más data al tempalte
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalles'
        return context



