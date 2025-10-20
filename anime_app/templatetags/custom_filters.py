from django import template
from pytils.translit import slugify

register = template.Library()

@register.filter
def truncate_chars(value, max_length):
    if len(value) > max_length:
        return value[:max_length - 3] + '...'
    return value
