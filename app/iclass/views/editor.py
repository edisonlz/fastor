# coding=utf-8

import json
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from wi_model_util.imodel import get_object_or_none
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from app.iclass.utils import redefine_item_pos
from app.iclass.utils.short_id import ShortID
from app.iclass.utils.common import get_paged_dict
from app.iclass.models import Editor


@login_required
def editor_list(request):
    
    qd = request.GET
    datas = Editor.objects.filter(status=Editor.STATUS_NORMAL).order_by("-pk")
    search_key = qd.get('search_key', '')
    if search_key:
        datas = datas.filter(title__contains=search_key)
    context = {
        "search_key": search_key,
    }
    context.update(get_paged_dict(datas, request.GET.get('page'), 20, 'datas'))
    return render(request, 'editor/editor_list.html', context)


@login_required
def editor_new(request):
    if request.method == 'POST':
        qd = request.POST
        _id = qd.get("itemid", "")
        if _id:
            item = Editor.objects.get(pk=_id)
        else:
            item = Editor()
            item.status = Editor.STATUS_NORMAL
        
        item.title = qd.get("title", '')
        item.content = qd.get("body", '')

        item.save()
        return HttpResponseRedirect(reverse("editor_list"))
    else:
        qd = request.GET
        _id = qd.get("itemid", "")
        if _id:
            item = Editor.objects.get(pk=_id)
        else:
            item = Editor()
        context = {
            "item": item,
        }
        
        return render(request, 'editor/editor_new.html', context)


def show_editor(request, short_id):
    _id = ShortID().toID(short_id)
    editor = Editor.objects.get(pk=_id)

    response = render(request, 'editor/editor_show.html', {
        'editor': editor,
        'created_at': editor.created_at.strftime('%Y-%m-%d'),
    })

    return response

