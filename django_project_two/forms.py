from django import forms
#from django.contrib.auth.models import User
from apps.users.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(required=True,
                               min_length=4,
                               max_length=50,
                               widget=forms.TextInput(attrs={
                                   'class':'form-control',
                                   'placeholder':'Username',
                                   'id':'id_username'
                               }))
    email = forms.EmailField(required=True,
                               widget=forms.EmailInput(attrs={
                                   'class':'form-control',
                                   'placeholder':'email@email.com',
                                   'id': 'id_email'
                               }))
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput(attrs={
                                   'class':'form-control',
                                   'placeholder':'******',
                                   'id': 'id_password'
                               }))
    password2 = forms.CharField(required=True,
                                label='Confirmar password',
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': '******',
                                   'id': 'id_password2'
                               }))

    ## las funciones que comienzan con clean_{field}, son usadas para poder realizar

    ## validaciones sobre el campo username
    def clean_username(self):
        #obtengo el valor ingresado
        username = self.cleaned_data.get('username')

        ##valido si el usuario ya existe para evitar duplicado
        if User.objects.filter(username=username).exists():
            ##se genera el mensaje de error para indicar porque no se puede
            raise forms.ValidationError('El username "{}" ya se encuentra en uso'.format(username))
        else:
            return username

    ## validaciones sobre el campo email
    def clean_email(self):
        # obtengo el valor ingresado
        email = self.cleaned_data.get('email')

        ##valido si el email ya existe para evitar duplicado
        if User.objects.filter(email=email).exists():
            ##se genera el mensaje de error para indicar porque no se puede usar
            raise forms.ValidationError('El email "{}" ya se encuentra en uso'.format(email))
        else:
            return email

    ## cuando un campo depende de otro se puede recurrir a sobreescribir la función clean
    def clean(self):
        ##convierto el formulario en un diccionario para acceder a su data
        cleaned_data = super().clean()

        ##se valida que los campos sean similares
        if cleaned_data.get('password2') != cleaned_data.get('password'):

            #se notifica al usuario que los campos no son iguales
            self.add_error('password2', 'El password no coincide.')

    def save(self):
        return User.objects.create_user(self.cleaned_data.get('username'),
                                        self.cleaned_data.get('email'),
                                        self.cleaned_data.get('password'))