from django import template

register = template.Library()


@register.filter
def format_phone(value):
    """Format the phone number as +380 (xx) xxx-xx-xx"""
    if len(value) == 13 and value.startswith('+380'):
        return f'{value[:4]} ({value[4:6]}) {value[6:9]}-{value[9:11]}-{value[11:]}'
    return value  
