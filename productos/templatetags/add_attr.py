from django import template
from django.forms.boundfield import BoundField

register = template.Library()


@register.filter(name="add_attr")
def add_attr(field: BoundField, css: str):
    attrs = {}
    clase, valor = css.split(':')
    attrs[clase] = valor
    return field.as_widget(attrs=attrs)
