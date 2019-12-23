#! /usr/bin/env python
# coding=utf-8
import hashlib
import hmac
import json
import random
import re
import string
import time
import uuid
from datetime import datetime
from hashlib import sha1
import os
from django.core.exceptions import ObjectDoesNotExist
import logging
import qrcode
import requests
import urllib



def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")


def json_encode(value):
    return json.dumps(value, default=json_serial)


def gen_qrcode(data):
    """生成二维码"""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    return img


def gen_random_string(n=32):
    assert n > 0
    choiceString = string.ascii_lowercase + string.digits

    if n <= 36:
        return "".join(random.sample(choiceString, n))

    # TODO: 待优化
    aList = []
    for i in xrange(n):
        aList.append(choiceString[random.randint(0, len(choiceString) - 1)])
    return "".join(aList)


def gen_uuid():
    return str(uuid.uuid1()).replace("-", "")


def gen_verify_code():
    return "".join(random.sample(string.digits, 4))


def get_primary_key():
    """
    获取主键：
    之前的做法是用时间字符串+sequence拼成，sequence从数据库中取,
    由于数据库类型已定，只能将错就错
    """
    ss = "%04d" % random.randint(0,9999)
    timestr = datetime.now().strftime("%Y%m%d%H%M%S%f") + ss
    return timestr


def gen_id():
    return int(time.time() * 10 ** 6)


def remove_duplicate(dict_list):
    """字典列表去重"""
    # seen = set()
    # new_dict_list = []
    # for dt in dict_list:
    #     seen.add(tuple(dt.items()))
    # for item in seen:
    #     new_dict_list.append(dict(item))
    # return new_dict_list
    new_list = []
    for item in dict_list:
        if item not in new_list:
            new_list.append(item)
    return new_list


def hmac_sha1_encode(raw, key=""):
    hashed = hmac.new(key, raw, sha1)
    return hashed.digest().encode("base64").rstrip('\n')




def remove_a_tag(value):
    return re.sub(r'</?a.*?>', '', value)


def redefine_item_pos(model, sorted_key, item_ids):
    """
    make the item save the new position after change position
    :param model:
    :param item_ids:
    :return:
    """
    try:
        item_ids = item_ids.split(',')
        items = []
        # primary_key = "%s__in" % sorted_key
        # model.objects.filter(primary_key=item_ids)

        for item_id in item_ids:
            item = model.objects.get(**{sorted_key: item_id})
            items.append(item)
        position_shuffle(items, saved=True)
    except ValueError:
        return
    except ObjectDoesNotExist as e:
        logging.error(e)


def position_shuffle(objs, saved=False):
    """
    :param list objs: objects need to be ordered
    :param bool saved: True / False
    code sample::
        position_shuffle( HomeBox.objects.all(), True)
    """
    if objs:
        for index, obj in enumerate(objs):
            if obj.position != index:
                obj.position = index
                if saved:
                    obj.save()
        return objs
    else:
        return []



def get_primary_key():
    """
    获取主键：
    之前的做法是用时间字符串+sequence拼成，sequence从数据库中取,
    由于数据库类型已定，只能将错就错
    """
    now = datetime.now()
    timestr = datetime.now().strftime("%Y%m%d%H%M%S%f") + \
              "".join(random.sample(string.digits, 4))
    return timestr



if __name__ == "__main__":
  
    print get_primary_key()
