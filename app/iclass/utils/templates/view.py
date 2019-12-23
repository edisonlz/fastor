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
def {{folder}}_list(request):
    {% if has_position %}
    if request.method == 'POST':
        item_ids = request.POST.get('item_ids')
        if item_ids:
            try:
                redefine_item_pos({{clazz}}, 'pk', item_ids)
                response = {'status': 'success'}
            except Exception, e:
                response = {'status': 'error'}
        else:
            response = {'status': 'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        qd = request.GET
        datas = {{clazz}}.objects.filter().order_by("position")
        search_key = qd.get('search_key', '')
        if search_key:
            datas = datas.filter(title__contains=search_key)
        context = {}
        context.update({"datas": datas})
        {% if foreign_key_gen_select %}{% for field in field_list %}{% if field.foreign_key_cls %}
        limit = 100
        {{field.foreign_key_datas}} = {{field.foreign_key_cls}}.objects.filter().order_by("id")[:limit]
        context["{{field.foreign_key_datas}}"] = {{field.foreign_key_datas}}{% endif %}{% endfor %}{% endif %}
        return render(request, '{{folder}}/list.html', context)
    {% else %}
    qd = request.GET
    datas = {{clazz}}.objects.filter().order_by("-pk")
    search_key = qd.get('search_key', '')
    if search_key:
        datas = datas.filter(title__contains=search_key)
    context = {}
    context.update(get_paged_dict(datas, request.GET.get('page'), 20, 'datas'))
    return render(request, '{{folder}}/list.html', context)
    {% endif %}


@login_required
def {{folder}}_new(request):
    if request.method == 'POST':
        qd = request.POST
        _id = qd.get("itemid", "")
        if _id:
            item = {{clazz}}.objects.get(pk=_id)
        else:
            item = {{clazz}}()
        {% for field in field_list %}
        item.{{field.attname}} = qd.get("{{field.attname}}", ''){% endfor %}
        item.save()
        return HttpResponseRedirect(reverse("{{folder}}_list"))
    else:
        qd = request.GET
        _id = qd.get("itemid", "")
        if _id:
            item = {{clazz}}.objects.get(pk=_id)
        else:
            item = {{clazz}}()
        context = {
            "item": item,
        }
        {% if foreign_key_gen_select %}{% for field in field_list %}{% if field.foreign_key_cls %}
        limit = 100
        {{field.foreign_key_datas}} = {{field.foreign_key_cls}}.objects.all().order_by("pk")[:limit]
        context["{{field.foreign_key_datas}}"] = {{field.foreign_key_datas}}
        {% endif %}{% endfor %}{% endif %}
        return render(request, '{{folder}}/new.html', context)
