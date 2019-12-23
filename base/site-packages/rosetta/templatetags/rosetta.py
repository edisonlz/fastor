from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape
import re

register = template.Library()
rx = re.compile(r'(%(\([^\s\)]*\))?[sd])')

def format_message(message):
    return mark_safe(rx.sub('<code>\\1</code>', escape(message).replace(r'\n','<br />\n')))
format_message=register.filter(format_message)


def lines_count(message):
    return 1 + sum([len(line)/50 for line in message.split('\n')])
lines_count=register.filter(lines_count)

def mult(a,b):
    return int(a)*int(b)
mult=register.filter(mult)

def minus(a,b):
    try:
        return int(a) - int(b)
    except:
        return 0
minus=register.filter(minus)
    

def gt(a,b):
    try:
        return int(a) > int(b)
    except:
        return False
gt=register.filter(gt)
