# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django_qbe.exports import formats

urlpatterns = patterns('django_qbe.views',
    url(r'^$', 'qbe_form', name="qbe_form"),
    url(r'^js/$', 'qbe_js', name="qbe_js"),
    url(r'^results/bookmark/$',
        'qbe_bookmark', name="qbe_bookmark"),
    url(r'^results/export/(?P<format>(%s))/$' % "|".join(formats.keys()),
        'qbe_export', name="qbe_export"),
    url(r'^results/proxy/$',
        'qbe_proxy', name="qbe_proxy"),
    url(r'^results/(?P<query_hash>(.*))/$',
        'qbe_results', name="qbe_results"),
    url(r'^auto/$', 'qbe_autocomplete', name="qbe_autocomplete"),
)
