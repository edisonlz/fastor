import unittest

from django.http import HttpRequest 

from crumbs.templatetags.breadcrumb_tags import render_breadcrumbs

class CrumbsTestCase(unittest.TestCase):
    def test_render_without_request(self):
        render_breadcrumbs({})
        
    def test_render_with_request(self):
        render_breadcrumbs({'request': ''})
        
    def test_render_with_request_and_crumbs(self):
        context = {}
        context['request'] = HttpRequest() 
        context['request'].breadcrumbs = []
        context['request'].breadcrumbs.append(('Test1', '/'))
        context['request'].breadcrumbs.append(('Test2', '/'))
        render_breadcrumbs(context)
        
    def test_add_without_request(self):
        render_breadcrumbs({})
        
    def test_add_with_request(self):
        render_breadcrumbs({'request': ''})
        
    def test_add_with_request_and_crumbs(self):
        context = {}
        context['request'] = HttpRequest() 
        context['request'].breadcrumbs = []
        context['request'].breadcrumbs.append(('Test1', '/'))
        context['request'].breadcrumbs.append(('Test2', '/'))
        render_breadcrumbs(context)
