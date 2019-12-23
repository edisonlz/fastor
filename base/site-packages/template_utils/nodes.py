"""
Subclass of ``template.Node`` for easy context updating.

"""

from django.db.models import get_model
from django.conf import settings
from django import template


class ContextUpdatingNode(template.Node):
    """
    Node that updates the context with certain values.
    
    Subclasses should define ``get_content()``, which should return a
    dictionary to be added to the context.
    
    """
    def render(self, context):
        context.update(self.get_content(context))
        return ''

    def get_content(self, context):
        raise NotImplementedError


class GenericContentNode(ContextUpdatingNode):
    """
    Base Node class for retrieving objects from any model.

    By itself, this class will retrieve a number of objects from a
    particular model (specified by an "app_name.model_name" string)
    and store them in a specified context variable (these are the
    ``num``, ``model`` and ``varname`` arguments to the constructor,
    respectively), but is also intended to be subclassed for
    customization.

    There are two ways to add extra bits to the eventual database
    lookup:

    1. Add the setting ``GENERIC_CONTENT_LOOKUP_KWARGS`` to your
       settings file; this should be a dictionary whose keys are
       "app_name.model_name" strings corresponding to models, and whose
       values are dictionaries of keyword arguments which will be
       passed to ``filter()``.

    2. Subclass and override ``_get_query_set``; all that's expected
       is that it will return a ``QuerySet`` which will be used to
       retrieve the object(s). The default ``QuerySet`` for the
       specified model (filtered as described above) will be available
       as ``self.query_set`` if you want to work with it.
    
    """
    def __init__(self, model, num, varname):
        self.num = num
        self.varname = varname
        lookup_dict = getattr(settings, 'GENERIC_CONTENT_LOOKUP_KWARGS', {})
        self.model = get_model(*model.split('.'))
        if self.model is None:
            raise template.TemplateSyntaxError("Generic content tag got invalid model: %s" % model)
        self.query_set = self.model._default_manager.filter(**lookup_dict.get(model, {}))
        
    def _get_query_set(self):
        return self.query_set
    
    def get_content(self, context):
        query_set = self._get_query_set()
        if self.num == 1:
            result = query_set[0]
        else:
            result = list(query_set[:self.num])
        return { self.varname: result }
