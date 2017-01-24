from django import template
from django.core import urlresolvers

register = template.Library()


@register.simple_tag
def edit(obj):
    try:
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name
        url = urlresolvers.reverse(
            'admin:' + app_label + '_' + model_name + '_change', args=(obj.id,)
        )
    except:
        url = ''
    return url
