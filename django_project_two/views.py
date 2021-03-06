from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from .forms import RegisterForm
from apps.photos.models import Photo
#from django.contrib.auth.models import User
from apps.users.models import User
from django.http import HttpResponseRedirect

def index(request):
    """
    funcion principal
    :param request:
    :return:
    """
    data = dict()

    data = {
        'title': 'Fotos',
        'message': 'Lista de Fotos',
        'photo_list': Photo.objects.all().order_by('-id')
    }
    return render(request, 'index.html', data)

def login_view(request):
    """
    Funcion en donde los usuarios se podrán registrar
    :param request (POST): username and password
    :return (render/redirect):
    """

    ## valido para evitar ingresar por URL
    if request.user.is_authenticated:
        return redirect('index')

    ##variab que contiene las variabels usadas en el template
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

            # Si el usuario no esta registrado, el login_required lo redirecciona
            # al login junto con la variable next, que es la vistaq que quería ir
            if request.GET.get('next'):
                # una vez logueado se redirecciona a la vista que quería acceder
                # pero que faltaba su login
                return HttpResponseRedirect(request.GET.get('next'))

            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña no validos.')

    data={
        'title':'Login'
    }
    return render(request, 'users/login.html', data)

def logout_view(request):
    """
    Funcion que me ayuda a cerrar la sesión de un usuario
    :param request (None):
    :return (redirect):
    """
    logout(request)
    messages.success(request, 'Su sesión ha sido cerrada con éxito.')
    return redirect('login')

def register(request):
    """
    Funcion que me ayuda a registrar nuevos usuarios
    :param request (POST):
    :return (render):
    """
    ## valido para evitar ingresar por URL
    if request.user.is_authenticated:
        return redirect('index')

    ##variab que contiene las variabels usadas en el template
    data = dict()

    ##formulario solicitado
    form = RegisterForm(request.POST or None)

    ##se valida que se realizo una consulta post y que el formulario es valido
    if request.method == 'POST' and form.is_valid():

        ##se procede a crear el registro de tipo User, sin permisos de administrador
        new_user = form.save()

        ##si el registro no es un None, es porque se creo exitosamente
        if new_user:

            ##se procede a loguear al nuevo usuario
            login(request, new_user)

            ##se genera el mensaje de creación exitosa del usuario
            messages.success(request, 'Usuario {}, creado exitosamente.'.format(new_user.username))

            ##se redirecciona a la página principal
            return redirect('index')

    data ={
        'form':form,
        'title':'Registro'
    }
    return render(request, 'users/register.html', data)