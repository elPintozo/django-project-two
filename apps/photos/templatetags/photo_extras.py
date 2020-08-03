from django import template

#Genero una instancia de template para registrar filter
register = template.Library()

@register.filter()#se registra la función como un filter
def price_format(value):
    """
    Función que ayuda a generar un formato
    de precio con el signo de plata
    :param value (float): un valor con decimales
    :return (sintr):
    """
    #.2f : indica que despues del punto decimal serán visible 2 digitos
    return '${0:.2f}'.format(value)

