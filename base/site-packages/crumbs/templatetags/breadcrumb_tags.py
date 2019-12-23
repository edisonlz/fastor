import copy
import pprint

from django import template
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

from crumbs.templatetags import CaktNode, parse_args_kwargs


register = template.Library()


class AddCrumbNode(CaktNode):
    def render_with_args(self, context, crumb, url=None, *args):
        href = None
        if url:
            if '/' in url:
                href = url
            else:
                href = reverse(url, args=args)
        if 'request' in context:
            if not hasattr(context['request'], 'breadcrumbs'):
                context['request'].breadcrumbs = []
            context['request'].breadcrumbs.append((crumb, href))
        return ''


@register.tag
def add_crumb(parser, token):
    tag_name, args, kwargs = parse_args_kwargs(parser, token)
    return AddCrumbNode(*args, **kwargs)


@register.inclusion_tag('breadcrumbs/crumbs.html', takes_context=True)
def render_breadcrumbs(context):
    if 'request' in context and hasattr(context['request'], 'breadcrumbs'):
        crumbs = context['request'].breadcrumbs
    else:
        crumbs = None
    if crumbs and len(crumbs) == 1:
        crumbs = None
    return {
        'crumbs': crumbs,
    }
