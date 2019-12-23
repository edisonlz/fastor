"""
Filters for converting plain text to HTML and enhancing the
typographic appeal of text on the Web.

"""


from django.conf import settings
from django.template import Library
from django.utils.safestring import mark_safe

from template_utils.markup import formatter


def apply_markup(value, arg=None):
    """
    Applies text-to-HTML conversion.
    
    Takes an optional argument to specify the name of a filter to use.
    
    """
    if arg is not None:
        return mark_safe(formatter(value, filter_name=arg))
    return mark_safe(formatter(value))
apply_markup.is_safe = True

def smartypants(value):
    """
    Applies SmartyPants to a piece of text, applying typographic
    niceties.
    
    Requires the Python SmartyPants library to be installed; see
    http://web.chad.org/projects/smartypants.py/
    
    """
    try:
        from smartypants import smartyPants
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError("Error in smartypants filter: the Python smartypants module is not installed or could not be imported")
        return value
    else:
        return mark_safe(smartyPants(value))

register = Library()
register.filter(apply_markup)
register.filter(smartypants)
