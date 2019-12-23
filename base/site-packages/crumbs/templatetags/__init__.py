import re

from django.template import Node, NodeList, Variable, Library
from django.template import TemplateSyntaxError, VariableDoesNotExist


def parse_args_kwargs(parser, token):
    contents = token.split_contents()
    tag_name = contents[0]
    args_list = contents[1:]
    args = []
    kwargs = {}
    
    for value in args_list:
        if '=' in value:
            k, v = value.split('=', 1)
            kwargs[str(k)] = v
        else:
            args.append(value)
    
    return tag_name, args, kwargs


class CaktNode(Node):
    def __init__(self, *args, **kwargs):
        self.args = [Variable(arg) for arg in args]
        self.kwargs = dict([(k, Variable(arg)) for k, arg in kwargs.items()])
        
    def render_with_args(self, context, *args, **kwargs):
        raise Exception('render_with_args must be implemented the class that inherits CaktNode')
    
    def render(self, context):
        args = []
        for arg in self.args:
            try:
                args.append(arg.resolve(context)) 
            except VariableDoesNotExist:
                args.append(None)
        
        kwargs = {}
        for k, arg in self.kwargs.items():
            try:
                kwargs[k] = arg.resolve(context)
            except VariableDoesNotExist:
                kwargs[k] = None
        
        return self.render_with_args(context, *args, **kwargs)
