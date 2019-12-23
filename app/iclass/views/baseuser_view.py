# coding=utf-8

import json
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from wi_model_util.imodel import get_object_or_none
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from app.iclass.utils import redefine_item_pos
from app.iclass.utils.common import get_paged_dict
from app.iclass.models import *

@login_required
def baseuser_list(request):
    
    qd = request.GET
    datas = BaseUser.objects.filter().order_by("-pk")
    search_key = qd.get('search_key', '')
    if search_key:
        datas = datas.filter(title__contains=search_key)
    context = {}
    context.update(get_paged_dict(datas, request.GET.get('page'), 20, 'datas'))
    return render(request, 'baseuser/list.html', context)
    


@login_required
def baseuser_new(request):
    if request.method == 'POST':
        qd = request.POST
        _id = qd.get("itemid", "")
        if _id:
            item = BaseUser.objects.get(pk=_id)
        else:
            item = BaseUser()
        
        item.user_id = qd.get("user_id", '')
        item.username = qd.get("username", '')
        item.nickname = qd.get("nickname", '')
        item.password = qd.get("password", '')
        item.image_url = qd.get("image_url", '')
        item.sex = qd.get("sex", '')
        item.email = qd.get("email", '')
        item.status = qd.get("status", '')
        item.register_from = qd.get("register_from", '')
        item.last_login_time = qd.get("last_login_time", '')
        item.create_time = qd.get("create_time", '')
        item.save()
        return HttpResponseRedirect(reverse("baseuser_list"))
    else:
        qd = request.GET
        _id = qd.get("itemid", "")
        if _id:
            item = BaseUser.objects.get(pk=_id)
        else:
            item = BaseUser()
        context = {
            "item": item,
        }
        
        return render(request, 'baseuser/new.html', context)
