import inspect, handler

from piston.handler import typemapper
from piston.handler import handler_tracker

from django.core.urlresolvers import get_resolver, get_callable, get_script_prefix
from django.shortcuts import render_to_response
from django.template import RequestContext

def generate_doc(handler_cls):
    """
    Returns a `HandlerDocumentation` object
    for the given handler. Use this to generate
    documentation for your API.
    """
    if not type(handler_cls) is handler.HandlerMetaClass:
        raise ValueError("Give me handler, not %s" % type(handler_cls))
        
    return HandlerDocumentation(handler_cls)
    
class HandlerMethod(object):
    def __init__(self, method, stale=False):
        self.method = method
        self.stale = stale
        
    def iter_args(self):
        args, _, _, defaults = inspect.getargspec(self.method)

        for idx, arg in enumerate(args):
            if arg in ('self', 'request', 'form'):
                continue

            didx = len(args)-idx

            if defaults and len(defaults) >= didx:
                yield (arg, str(defaults[-didx]))
            else:
                yield (arg, None)
        
    @property
    def signature(self, parse_optional=True):
        spec = ""

        for argn, argdef in self.iter_args():
            spec += argn
            
            if argdef:
                spec += '=%s' % argdef
            
            spec += ', '
            
        spec = spec.rstrip(", ")
        
        if parse_optional:
            return spec.replace("=None", "=<optional>")
            
        return spec
        
    @property
    def doc(self):
        return inspect.getdoc(self.method)
    
    @property
    def name(self):
        return self.method.__name__
    
    @property
    def http_name(self):
        if self.name == 'read':
            return 'GET'
        elif self.name == 'create':
            return 'POST'
        elif self.name == 'delete':
            return 'DELETE'
        elif self.name == 'update':
            return 'PUT'
    
    def __repr__(self):
        return "<Method: %s>" % self.name
    
class HandlerDocumentation(object):
    def __init__(self, handler):
        self.handler = handler
        
    def get_methods(self, include_default=False):
        for method in "read create update delete".split():
            met = getattr(self.handler, method, None)

            if not met:
                continue
                
            stale = inspect.getmodule(met) is handler

            if not self.handler.is_anonymous:
                if met and (not stale or include_default):
                    yield HandlerMethod(met, stale)
            else:
                if not stale or met.__name__ == "read" \
                    and 'GET' in self.allowed_methods:
                    
                    yield HandlerMethod(met, stale)
        
    def get_all_methods(self):
        return self.get_methods(include_default=True)
        
    @property
    def is_anonymous(self):
        return handler.is_anonymous

    def get_model(self):
        return getattr(self, 'model', None)
            
    @property
    def has_anonymous(self):
        return self.handler.anonymous
            
    @property
    def anonymous(self):
        if self.has_anonymous:
            return HandlerDocumentation(self.handler.anonymous)
            
    @property
    def doc(self):
        return self.handler.__doc__
    
    @property
    def name(self):
        return self.handler.__name__
    
    @property
    def allowed_methods(self):
        return self.handler.allowed_methods
    
    def get_resource_uri_template(self):
        """
        URI template processor.
        
        See http://bitworking.org/projects/URI-Templates/
        """
        def _convert(template, params=[]):
            """URI template converter"""
            paths = template % dict([p, "{%s}" % p] for p in params)
            return u'%s%s' % (get_script_prefix(), paths)
        
        try:
            resource_uri = self.handler.resource_uri()
            
            components = [None, [], {}]

            for i, value in enumerate(resource_uri):
                components[i] = value
        
            lookup_view, args, kwargs = components
            lookup_view = get_callable(lookup_view, True)

            possibilities = get_resolver(None).reverse_dict.getlist(lookup_view)
            
            for possibility, pattern in possibilities:
                for result, params in possibility:
                    if args:
                        if len(args) != len(params):
                            continue
                        return _convert(result, params)
                    else:
                        if set(kwargs.keys()) != set(params):
                            continue
                        return _convert(result, params)
        except:
            return None
        
    resource_uri_template = property(get_resource_uri_template)
    
    def __repr__(self):
        return u'<Documentation for "%s">' % self.name

def documentation_view(request):
    """
    Generic documentation view. Generates documentation
    from the handlers you've defined.
    """
    docs = [ ]

    for handler in handler_tracker: 
        docs.append(generate_doc(handler))

    def _compare(doc1, doc2): 
       #handlers and their anonymous counterparts are put next to each other.
       name1 = doc1.name.replace("Anonymous", "")
       name2 = doc2.name.replace("Anonymous", "")
       return cmp(name1, name2)    
 
    docs.sort(_compare)
       
    return render_to_response('documentation.html', 
        { 'docs': docs }, RequestContext(request))
