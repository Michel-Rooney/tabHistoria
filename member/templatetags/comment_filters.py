from django import template

register = template.Library()

@register.filter(name='existe_comentario')
def existe_comentario(value):
    return False