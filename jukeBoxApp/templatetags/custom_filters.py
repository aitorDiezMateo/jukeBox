"""
Filtros personalizados de plantilla para jukeBoxApp
"""
from django import template

register = template.Library()


@register.filter(name='length_is')
def length_is(value, arg):
    """
    Devuelve True si la longitud del valor es igual al argumento.
    Reemplazo para el filtro length_is eliminado en Django 5.0+
    
    Uso: {% if my_list|length_is:"3" %}
    """
    try:
        return len(value) == int(arg)
    except (ValueError, TypeError):
        return False
