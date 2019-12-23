# coding: utf-8

from django.conf.urls import url
from app.iclass.views import *


# 课程 urls
urlpatterns = [


     
    # for common
    url(r'^common/common_update_status', 'iclass.views.common_update_status', name="common_update_status"),
    url(r'^common/common_update_status_str', 'iclass.views.common_status', name="common_update_status_str"),
    url(r'^common/status$', 'iclass.views.common_status', name="common_status"),
    url(r'^default/img/upload', 'iclass.views.img_upload', name='img_upload'),

    
    # 客户管理
    url(r'^customer/list$', 'iclass.views.baseuser_view.baseuser_list', name='baseuser_list'),
    url(r'^customer/detail$', 'iclass.views.baseuser_view.baseuser_new', name='baseuser_new'),



    # 资讯 - 编辑器工具
    url(r'^editor/list$', 'iclass.views.editor_list', name='editor_list'),
    url(r'^editor/new$', 'iclass.views.editor_new', name='editor_new'),
    url(r'^e/(?P<short_id>[A-Za-z0-9]+)$', 'iclass.views.show_editor', name='show_editor'),

]


