"""
Template tags which can do retrieval of content from any model.

"""


from django import template
from django.db.models import get_model

from template_utils.nodes import ContextUpdatingNode, GenericContentNode


class RandomObjectsNode(GenericContentNode):
    """
    A subclass of ``GenericContentNode`` which overrides
    ``_get_query_set`` to apply random ordering.
    
    """
    def _get_query_set(self):
        return self.query_set.order_by('?')


class RetrieveObjectNode(ContextUpdatingNode):
    """
    ``Node`` subclass which retrieves a single object -- by
    primary-key lookup -- from a given model.

    Because this is a primary-key lookup, it is assumed that no other
    filtering is needed; hence, the settings-based filtering performed
    by ``GenericContentNode`` is not used here.
    
    """
    def __init__(self, model, pk, varname):
        self.pk = template.Variable(pk)
        self.varname = varname
        self.model = get_model(*model.split('.'))
        if self.model is None:
            raise template.TemplateSyntaxError("Generic content tag got invalid model: %s" % model)
    
    def get_content(self, context):
        return { self.varname: self.model._default_manager.get(pk=self.pk.resolve(context))}


def do_latest_object(parser, token):
    """
    Retrieves the latest object from a given model, in that model's
    default ordering, and stores it in a context variable.
    
    Syntax::
    
        {% get_latest_object [app_name].[model_name] as [varname] %}
    
    Example::
    
        {% get_latest_object comments.freecomment as latest_comment %}
    
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes three arguments" % bits[0])
    if bits [2] != 'as':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
    return GenericContentNode(bits[1], 1, bits[3])


def do_latest_objects(parser, token):
    """
    Retrieves the latest ``num`` objects from a given model, in that
    model's default ordering, and stores them in a context variable.
    
    Syntax::
    
        {% get_latest_objects [app_name].[model_name] [num] as [varname] %}
    
    Example::
    
        {% get_latest_objects comments.freecomment 5 as latest_comments %}
    
    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError("'%s' tag takes four arguments" % bits[0])
    if bits [3] != 'as':
        raise template.TemplateSyntaxError("third argument to '%s' tag must be 'as'" % bits[0])
    return GenericContentNode(bits[1], bits[2], bits[4])

def do_random_object(parser, token):
    """
    Retrieves a random object from a given model, and stores it in a
    context variable.
    
    Syntax::
    
        {% get_random_object [app_name].[model_name] as [varname] %}
    
    Example::
    
        {% get_random_object comments.freecomment as random_comment %}
    
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes three arguments" % bits[0])
    if bits [2] != 'as':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])
    return RandomObjectsNode(bits[1], 1, bits[3])


def do_random_objects(parser, token):
    """
    Retrieves ``num`` random objects from a given model, and stores
    them in a context variable.
    
    Syntax::
    
        {% get_random_objects [app_name].[model_name] [num] as [varname] %}
    
    Example::
    
        {% get_random_objects comments.freecomment 5 as random_comments %}
    
    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError("'%s' tag takes four arguments" % bits[0])
    if bits [3] != 'as':
        raise template.TemplateSyntaxError("third argument to '%s' tag must be 'as'" % bits[0])
    return RandomObjectsNode(bits[1], bits[2], bits[4])


def do_retrieve_object(parser, token):
    """
    Retrieves a specific object from a given model by primary-key
    lookup, and stores it in a context variable.
    
    Syntax::
    
        {% retrieve_object [app_name].[model_name] [pk] as [varname] %}
    
    Example::
    
        {% retrieve_object flatpages.flatpage 12 as my_flat_page %}
    
    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError("'%s' tag takes four arguments" % bits[0])
    if bits[3] != 'as':
        raise template.TemplateSyntaxError("third argument to '%s' tag must be 'as'" % bits[0])
    return RetrieveObjectNode(bits[1], bits[2], bits[4])

register = template.Library()
register.tag('get_latest_object', do_latest_object)
register.tag('get_latest_objects', do_latest_objects)
register.tag('get_random_object', do_random_object)
register.tag('get_random_objects', do_random_objects)
register.tag('retrieve_object', do_retrieve_object)
