from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_item_tuple(dictionary, keys):
    start_time, end_time = keys.split(',')
    return dictionary.get((start_time, end_time))