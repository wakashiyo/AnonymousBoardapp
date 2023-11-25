import os
from django import template

register = template.Library()

@register.simple_tag
def get_env_variable(key):
    return os.environ.get(key)