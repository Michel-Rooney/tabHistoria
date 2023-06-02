from django import template

register = template.Library()

@register.filter
def index_post(value, page):
    if page <= 1:
        return value
    return value + (page -1) * 10
