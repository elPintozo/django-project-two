from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login


def index(request):
    """
    funcion principal
    :param request:
    :return:
    """
    data =dict()

    data = {
        'title': 'Fotos',
        'message': 'Lista de Fotos',
        'list_photos': [
            {
                'title': "Animal's Photos",
                'price': 150,
                'stock': True
            },{
                'title': "Plant's Photos",
                'price': 250,
                'stock': False
            },{
                'title': "Car's Photos",
                'price': 350,
                'stock': True
            },{
                'title': "Pen's Photos",
                'price': 50,
                'stock': False
            }
        ]
    }
    return render(request, 'index.html', data)

def login_view(request):
    """
    Funcion en donde los usuarios se podrán registrar
    :param request:
    :return:
    """
    data = dict()

    if request.method == 'POST':

        ##obtengo los datos del formulario
        username = request.POST.get('username')
        password = request.POST.get('password')

        ## valido si existe el usuario
        user = authenticate(username=username, password=password)

        #se valida si el usuario ingresado es valido y con los datos correctos
        if user is not None:
            ##se autentica al usuario
            login(request, user)
            messages.success(request, 'Bienvenido {}.'.format(username))
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña no validos.')

    return render(request, 'users/login.html', data)