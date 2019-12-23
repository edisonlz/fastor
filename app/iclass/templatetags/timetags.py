#coding=utf-8

from django import template
import datetime
register = template.Library()

def print_timestamp(timestamp):
    if not timestamp:
      return ""

    try:
        #assume, that timestamp is given in seconds with decimal point
        ts = float(timestamp)
        return datetime.datetime.fromtimestamp(ts)
    except ValueError:
        ts = float(timestamp)/1000
        return datetime.datetime.fromtimestamp(ts)


def senconds_format(seconds):
    if not seconds:
      return ''

    seconds = float(seconds)
    if seconds<=60:
        return "1分钟"
    else:
         return "%.2f分钟"  % (seconds / 60 )


register.filter(print_timestamp)
register.filter(senconds_format)





