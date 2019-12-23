# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    # 用户 (权限暂时只分管理员和普通账户)
    url(regex='^user/list/$', view='user.views.user_list', name=u'user_list'),
    url(regex='^user/edit/$', view='user.views.user_edit', name=u'user_add'),
    url(regex='^user/create/$', view='user.views.user_create', name=u'user_create'),
    url(regex='^user/delete/$', view='user.views.user_delete', name=u'user_delete'),
    url(regex='^find/user$', view='user.views.find_user', name=u'find_user'),
    url(regex='^search/user$', view='user.views.user_search', name=u'search_user'),


    # 系统用户管理
    url(r'^system_user/list$', 'user.views.system_user_list', name='system_user_list'),
    url(r'^system_user/detail$', 'user.views.system_user_new', name='system_user_new'),
    url(r'^system_user/password$', 'user.views.change_password', name='change_password'),
    url(r'^system_user/delete$', 'user.views.system_user_delete', name='system_user_delete'),

)