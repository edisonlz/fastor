# coding=utf-8
"""
Requirement:
{%load util_tags%}

System build in https://docs.djangoproject.com/en/dev/ref/templates/builtins/
"""
import datetime
import time
from decimal import Decimal
from django import template
import re
from django.conf import settings

register = template.Library()
@register.filter
def yes_or_no(data):
    if data:
        return True
    else:
        return False


# 两个数相除得百分比
@register.filter
def percent(data1, data2):
    return float(data1)/float(data2) * 100



# 针对state
@register.filter
def dict_get(dict, key):
    """How to Use

    {{ dict|dict_get:key }}

    """

    return dict.get(key, '')


@register.filter(is_safe=True)
def truncate_zh(str, len):
    return str[:len] + '...'


@register.filter
def index_url(value, str):
    if str in value:
        return True
    else:
        return False


@register.filter
def lower(value):  # Only one argument.
    """Converts a string into all lowercase
        How to Use
        {{ value|lower|lower|.... }}
    """
    return value.lower()


@register.filter
def upper(value):  # Only one argument.
    """Converts a string into all lowercase
        How to Use
        {{ value|lower|lower|.... }}
    """
    return value.upper()


@register.filter
def to_int(value):  # Only one argument.
    if value and len(value) > 0:
        result = int(value)
    else:
        result = 0
    return result


@register.filter
def to_str(value):
    return str(value)


@register.filter
def type_of(value):  # Only one argument.
    return type(value)


@register.assignment_tag
def get_current_time(format_string):
    """
    How to Use
    You may then store the result in a template variable using the as argument followed by the variable name, and output it yourself where you see fit:
    {% get_current_time "%Y-%m-%d %I:%M %p" as the_time %}
    <p>The time is {{ the_time }}.</p>
    """
    return datetime.datetime.now().strftime(format_string)


@register.filter
def format_timestamp(timestamp):
    """format a timestamp(int)
        How to Use
        {{ value|format_timestamp }}
    """
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(timestamp))


@register.simple_tag()
def fen_to_yuan(value):
    return "%.2f" % round(value / Decimal(100.0), 2)


@register.filter()
def format_float(num, point=3):
    return ("%." + str(point) + "f") % num


@register.filter()
def ifin_list(value, alist):
    assert isinstance(alist, list)
    if value in alist:
        return True

    return False



@register.filter
def to_query_key_string(dic):
    if dic:
        content = '&'.join(['='.join((k,str(v))) for k,v in dic.iteritems()])
        return content
    return ""

@register.filter
def in_list(paper_id,str_paper_ids):
    paper_id_list = str_paper_ids.split(",")
    if paper_id in paper_id_list:
        return True
    else:
        return False


