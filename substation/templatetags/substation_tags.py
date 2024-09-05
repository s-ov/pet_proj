from django import template
from substation.models import Substation

register = template.Library()


@register.inclusion_tag('substation/substations_list.html')
def show_substations():
    return {'substations': Substation.objects.all(),}
