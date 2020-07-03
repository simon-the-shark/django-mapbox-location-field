from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def transform_map_attrs_to_js(id, key, map_attr):
    """renders javascript variable from python attribute"""
    js_pattern = "map_attrs['{id}'].{key} = ".format(id=id, key=key)
    if type(map_attr) == list or type(map_attr) == tuple:
        return mark_safe(js_pattern + str(list(map_attr)) + ";")
    elif type(map_attr) == bool:
        return mark_safe(js_pattern + str(map_attr).lower() + ";")
    else:
        return mark_safe(js_pattern + "'{str}'".format(str=map_attr) + ";")
