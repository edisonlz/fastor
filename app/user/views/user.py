# coding=utf-8

from datetime import datetime
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
import json
from itertools import chain
from app.user.models import User


class UserForm(forms.Form):
    email = forms.EmailField(label=_("Email"), error_messages={'invalid': u'请输入合法email地址'})
    name = forms.CharField(max_length=50, error_messages={'required': u'请输入必填字段', 'max_length': u'最大长度是50个字符'})


@login_required()
def user_list(req):
    managers = User.objects.filter(role__in=(0, 2)).order_by("role", "-date_joined")
    normal_users = User.objects.filter(role=1).order_by("role", "-date_joined")
    users = list(chain(managers, normal_users))
    paginator = Paginator(users, 15)
    page = req.GET.get('page', 1)
    add_success = req.GET.get('add_success', "0")
    try:
        pag_users = paginator.page(page)
    except PageNotAnInteger:
        pag_users = paginator.page(1)
    except EmptyPage:
        pag_users = paginator.page(paginator.num_pages)

    for u in pag_users.object_list:
        u.active_str = u'正常' if u.is_active else u'冻结'

    content = {'users': pag_users, 'add_success': add_success}
    return render_to_response("user_list.html", content, context_instance=RequestContext(req))


def user_delete(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        User.objects.filter(pk=uid).delete()
    return HttpResponseRedirect(reverse('user_list'))


def user_create(request):
    if request.method == 'POST':
        post = request.POST
        email = post.get('email', '')
        state = post.get('state', '')
        role = post.get('role', "1")
        name = post.get('name', '')
        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            User.objects.create(first_name=name, username=email, email=email, role=role,
                                is_active=True if state == '1' else False)
            result = {'status': 'success'}
        else:
            result = {'status': 'error', 'msg': 'User(%s) already exists' % email}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        return render_to_response("user_create.html", {'USER': User}, context_instance=RequestContext(request))


@login_required()
def user_edit(request):
    if not request.user.is_super:
        return render_to_response("user_edit.html", {'error1': u'无权限'}, context_instance=RequestContext(request))

    if request.method == 'POST':
        post = request.POST
        uid = post.get('uid', '')
        state = post.get('state', '')
        role = post.get('role', "1")
        name = post.get('name', '')
        if uid:
            User.objects.filter(pk=uid).update(
                role=role,
                first_name=name,
                is_active=True if state == '1' else False)
        return HttpResponseRedirect(reverse('user_list'))
    else:
        _get = request.GET
        uid = _get.get('uid', '')
        if uid:
            try:
                user = User.objects.get(pk=uid)
            except User.DoesNotExist:
                user = User()
        else:
            user = User()
            user.id = ''
        return render_to_response("user_edit.html", {'user_l': user, 'id': user.id},
                                  context_instance=RequestContext(request))


@login_required
def find_user(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        if email:
            try:
                user = User.objects.get(username__iexact=email)
            except User.DoesNotExist, e:
                response = {'status': 0}
            else:
                response = {'status': 1}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required()
def user_search(request):
    # if request.method == 'POST':
    search = request.POST.get('search', '')
    if search.strip() == '':
        users = User.objects.all()
        paginator = Paginator(users, 10)
        page = request.GET.get('page', 1)
        add_success = request.GET.get('add_success', "0")
        try:
            pag_users = paginator.page(page)
        except PageNotAnInteger:
            pag_users = paginator.page(1)
        except EmptyPage:
            pag_users = paginator.page(paginator.num_pages)

        for u in pag_users.object_list:
            u.active_str = u'正常' if u.is_active else u'冻结'

        content = {'users': pag_users, 'add_success': add_success}
        return render_to_response("user_list.html", content, context_instance=RequestContext(request))
    else:

        users = User.objects.filter(email__icontains=search)
        paginator = Paginator(users, 100)
        page = request.GET.get('page', 1)
        try:
            pag_users = paginator.page(page)
        except PageNotAnInteger:
            pag_users = paginator.page(1)
        except EmptyPage:
            pag_users = paginator.page(paginator.num_pages)

        for u in pag_users.object_list:
            u.active_str = u'正常' if u.is_active else u'冻结'
        fail = 0
        if len(users) == 0:
            fail = 1
        content = {'users': pag_users, 'search': search, 'fail': fail}
        return render_to_response("user_list.html", content, context_instance=RequestContext(request))