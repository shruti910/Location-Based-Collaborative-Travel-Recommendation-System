import json
from django import template
from datetime import date, timedelta

register = template.Library()
@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)