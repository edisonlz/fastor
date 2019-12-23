# coding=utf-8

import json
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from wi_model_util.imodel import get_object_or_none
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Max, Q
from app.iclass.utils import redefine_item_pos
from app.iclass.utils.common import get_paged_dict
from app.user.models import User


@login_required
def system_user_list(request):

    qd = request.GET
    datas = User.objects.filter(~Q(status=User.STATUS_DELETE)).order_by("-pk")

    search_key = qd.get('search_key', '')
    if search_key:
        datas = datas.filter(username__contains=search_key)
    context = {
        "search_key": search_key,
        "current_user": request.user,
    }
    context.update(get_paged_dict(datas, request.GET.get('page'), 20, 'datas'))
    return render(request, 'system_user/user_list.html', context)


@login_required
def system_user_new(request):

    if request.method == 'POST':
        qd = request.POST
        _id = qd.get("itemid", "")
        if _id:
            item = User.objects.get(pk=_id)
        else:
            item = User()
            item.set_password(qd.get("password", ''))
        item.role = qd.get("role", 0)
        item.username = qd.get("username", '')
        item.email = qd.get("email", '')
        item.first_name = qd.get("first_name", '')
        item.last_name = qd.get("last_name", '')
        item.save()
        return HttpResponseRedirect(reverse("system_user_list"))
    else:
        qd = request.GET
        _id = qd.get("itemid", "")
        if _id:
            item = User.objects.get(pk=_id)
        else:
            item = User()
        context = {
            "item": item,
            "current_user": request.user,

        }

        return render(request, 'system_user/user_new.html', context)


@login_required
def change_password(request):
    if request.method == "POST":
        qd = request.POST
        user_id = qd.get("user_id", 0)
        user = User.objects.filter(pk=user_id).first()
        user.set_password(qd.get("password", ''))
        user.save()
        return HttpResponseRedirect(reverse("system_user_list"))
    else:
        qd = request.GET
        user_id = qd.get("user_id", 0)
        user = User.objects.filter(pk=user_id).first()
        return render(request, 'system_user/user_password.html', {"user": user})


@login_required
def system_user_delete(request):
    from app.user.models import User

    if request.method == 'POST':
        qd = request.POST
        _id = qd.get("item_id")
        user = User.objects.filter(pk=_id).first()

        if not user:
            result = {"success": False}
            return HttpResponse(json.dumps(result), content_type="application/json")

        user.status = User.STATUS_DELETE
        user.save()
        result = {"success": True}
        return HttpResponse(json.dumps(result), content_type="application/json")

