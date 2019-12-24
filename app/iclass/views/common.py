# coding=utf-8

from django.db.models import Max, Q
from django.core.exceptions import FieldError
from django.http import HttpResponse
import json
from django.contrib.auth.decorators import login_required
from wi_model_util.imodel import get_object_or_none
from app.iclass.models import *
from app.iclass.utils import  upload_django_local_file 
import random

MIMEANY = '*/*'
MIMEJSON = 'application/json'
MIMETEXT = 'text/plain'

def img_upload(request):
    if request.method == 'POST':
        file_obj = request.FILES[u'files[]']
        screenshot_type = request.POST.get("type")
        

        if False and screenshot_type:
            screenshot_size = "480x270" if screenshot_type == "0" else "270x480"

        a = random.randint(1000,1000000)
        b = random.randint(1000,1000000)
        c = random.randint(1000,1000000)

        file_name = "%s_%s_%s.%s" % (a, b, c, file_obj.name.split(".")[-1])
        remote_url = upload_django_local_file(file_obj , file_name)


        if not remote_url:
            response_data = {
                "e":{
                    "code": -1
                }
            }
        else:
            response_data = {
                "files": [
                    {
                        "name": file_obj.name,
                        "type": file_obj.content_type,
                        "size": file_obj.size,
                        "url": remote_url,
                    }
                ]
            }

        response = JSONResponse(response_data, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    else:
        return HttpResponse('OK')





def upload_editor_img(request):
    if request.method == 'POST':
        file_obj = request.FILES[u'files[]']

        a = random.randint(1000,1000000)
        b = random.randint(1000,1000000)
        c = random.randint(1000,1000000)

        file_name = "%s_%s_%s.%s" % (a, b, c, file_obj.name.split(".")[-1])

        remote_url = upload_django_local_file(file_obj, file_name)

        if not remote_url:
            data = {
                "e":{
                    "desc":"error",
                    "code": -1
                }
            }

        else:
            data = {
                "state": "SUCCESS",
                "originalName": file_obj.name,
                "size": str(file_obj.size),
                "name": file_obj.name,
                "type": file_obj.content_type,
                "url": remote_url
            }


        response = JSONResponse(data, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    else:
        return HttpResponse('OK')






@login_required()
def common_status(request):
    item_id = request.POST["item_id"]
    item_class = eval(request.POST['item_class'])
    item = get_object_or_none(item_class, pk=item_id)
    if item and item.status == '1':
        item.status = '0'
    else:
        item.status = '1'
    item.save()

    resp = {
        "code": 200,
        "msg": u"操作成功！",
        "result": {
            "status": item.status,
        }
    }
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required()
def common_update_status(request):
    item_id = request.POST["item_id"]
    item_class = eval(request.POST['item_class'])
    item = get_object_or_none(item_class, pk=item_id)
    if item and item.status:
        item.status = 0
    else:
        item.status = 1
    item.save()

    resp = {
        "code": 200,
        "msg": u"操作成功！",
        "result": {
            "status": item.status,
        }
    }
    return HttpResponse(json.dumps(resp), content_type="application/json")


def set_position(instance, model, query_dict=None):
    if query_dict:
        try:
            position = model.objects.filter(**query_dict).aggregate(Max('position'))['position__max']
        except (FieldError, TypeError):
            position = 0
    else:
        position = model.objects.all().aggregate(Max('position'))['position__max']
    if position is None:
        position = 0
    setattr(instance, 'position', position+1)


def response_mimetype(request):
    """response_mimetype -- Return a proper response mimetype, accordingly to
    what the client accepts, as available in the `HTTP_ACCEPT` header.

    request -- a HttpRequest instance.

    """
    can_json = MIMEJSON in request.META['HTTP_ACCEPT']
    can_json |= MIMEANY in request.META['HTTP_ACCEPT']
    return MIMEJSON if can_json else MIMETEXT


class JSONResponse(HttpResponse):
    """JSONResponse -- Extends HTTPResponse to handle JSON format response.

    This response can be used in any view that should return a json stream of
    data.

    Usage:

        def a_iew(request):
            content = {'key': 'value'}
            return JSONResponse(content, mimetype=response_mimetype(request))

    """

    def __init__(self, obj='', json_opts=None, mimetype=MIMEJSON, *args, **kwargs):
        json_opts = json_opts if isinstance(json_opts, dict) else {}
        content = json.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)


