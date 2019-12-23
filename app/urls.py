# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import RedirectView
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Uncomment the next line to enable the admin:

    # 用户和权限 带有admin或user的path需要验证登录
    url(r'', include('app.user.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'app.iclass.views.dashboard_index', name='dashboard_index'),
    url(r'^dashboard_index$', 'app.iclass.views.dashboard_index', name='dashboard_index'),


    url(r'^signin/$', 'django.contrib.auth.views.login', {'template_name': 'sign_in_new.html'}, name="signin"),
    url(r'^signout/$', 'django.contrib.auth.views.logout_then_login',  name="signout"),


    url(r'', include('app.iclass.urls')),

)


if settings.DEBUG is False:
   urlpatterns += patterns('',url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}))