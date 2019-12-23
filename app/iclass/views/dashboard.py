# coding=utf-8

import json
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from wi_model_util.imodel import get_object_or_none
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from app.iclass.utils import redefine_item_pos
from app.iclass.models import *
from base.core.dateutils import *
import datetime
import random

@login_required
def dashboard_index(request):
    """
    这里展示系统的应用统计数据
    """

    qd = request.GET
    current_user = request.user
    now = datetime.datetime.now()

    start_time = qd.get("start_time", days_ago(30).strftime("%Y-%m-%d %H:%M"))
    end_time = qd.get("end_time", zero_date().strftime("%Y-%m-%d %H:%M"))

    if type(start_time) == str or type(start_time) == unicode:
        start_time = datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M')

    if type(end_time) == str or type(end_time) == unicode:
        end_time = datetime.datetime.strptime(end_time,'%Y-%m-%d %H:%M')

    _start_time = datetime_to_timestamp(start_time)
    _end_time = datetime_to_timestamp(end_time)

    
    context = {
        "course": {
            "course_count":random.randint(10,100),
            "course_guake_count":random.randint(10,100),
        },
        "subject":{
            "subject_count":random.randint(10,100),
            "mock_page_count":random.randint(10,100)
        },
        "paper":{
            "paper_count":random.randint(10,100),
        },
        "question":{
            "question_count":random.randint(10,100),
        },
        "app":'fastor',
    }

    context['user_incr_datas'] = ((u'11-23', 238L), (u'11-24', 747L), (u'11-25', 632L), (u'11-26', 470L), (u'11-27', 408L), (u'11-28', 408L), (u'11-29', 318L), (u'11-30', 248L), (u'12-01', 269L), (u'12-02', 358L), (u'12-03', 401L), (u'12-04', 343L), (u'12-05', 422L), (u'12-06', 299L), (u'12-07', 236L), (u'12-08', 317L), (u'12-09', 436L), (u'12-10', 484L), (u'12-11', 351L), (u'12-12', 287L), (u'12-13', 279L), (u'12-14', 301L), (u'12-15', 266L), (u'12-16', 336L), (u'12-17', 374L), (u'12-18', 404L), (u'12-19', 357L), (u'12-20', 279L), (u'12-21', 218L), (u'12-22', 264L))
    context['user_incr_success_datas'] = ((u'11-23', 238L), (u'11-24', 747L), (u'11-25', 632L), (u'11-26', 470L), (u'11-27', 408L), (u'11-28', 408L), (u'11-29', 318L), (u'11-30', 248L), (u'12-01', 269L), (u'12-02', 357L), (u'12-03', 401L), (u'12-04', 343L), (u'12-05', 422L), (u'12-06', 299L), (u'12-07', 235L), (u'12-08', 317L), (u'12-09', 436L), (u'12-10', 484L), (u'12-11', 351L), (u'12-12', 287L), (u'12-13', 279L), (u'12-14', 301L), (u'12-15', 266L), (u'12-16', 336L), (u'12-17', 374L), (u'12-18', 404L), (u'12-19', 357L), (u'12-20', 279L), (u'12-21', 218L), (u'12-22', 264L))
    context["sql_area_count"] = ((u'\u5e7f\u4e1c\u7701', 387L), (u'\u5317\u4eac', 376L), (u'\u6c5f\u82cf\u7701', 316L), (u'\u9ed1\u9f99\u6c5f\u7701', 310L), (u'\u5e7f\u4e1c', 300L), (u'\u6d59\u6c5f', 282L))   
    context["order_time_datas"] = ((u'00', 35L), (u'01', 10L), (u'02', 8L), (u'05', 2L), (u'06', 8L), (u'07', 18L), (u'08', 47L), (u'09', 35L), (u'10', 108L), (u'11', 65L), (u'12', 61L), (u'13', 50L), (u'14', 54L), (u'15', 65L), (u'16', 39L), (u'17', 43L), (u'18', 20L), (u'19', 43L), (u'20', 48L), (u'21', 77L), (u'22', 34L), (u'23', 34L))
    context["start_time"] = start_time
    context["end_time"] = end_time
    context["now"] = now.strftime("%Y-%m-%d")
    context["device_data"] = ((u'iPhon', 78425L), (u'phone', 69710L), (u'HUAWE', 30187L), (u'Xiaom', 17106L), (u'OPPO-', 16214L), (u'vivo-', 16134L), (u'iPad1', 13548L), (u'Meizu', 4509L), (u'samsu', 3361L), (u'OnePl', 1110L))

    return render(request, 'cms_index/basecontent.html', context)



    
    




