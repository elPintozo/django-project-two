from django import template

register = template.Library()

@register.filter()
def quantity_photo_format(quantity=1):
    """
    Funcion que modifica el texto en singular o plurar
    según la cantidad de productos a agregar al carrito
    :param quantity (int): cantidad de productoa a agregar al carrito
    :return (string): texto en singular o plural
    """
    return '{} {}'.format(quantity, 'productos' if quantity>1 else 'Producto')

@register.filter()
def quantity_add_format(quantity=1):
    """
    Funcion que modifica el texto en singular o plurar
    según la cantidad de productos a agregar al carrito
    :param quantity (int): cantidad de productoa a agregar al carrito
    :return (string): texto en singular o plural
    """
    return "{} {}".format(
        quantity_photo_format(quantity), 'agregados' if quantity>1 else 'agregado'
    )