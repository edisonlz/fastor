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
import shutil
import qrcode
import requests
import random
import urllib
import logging

from django.conf import settings

def upload_local_file(memfile,  data=None, _headers=None):
    gobal_path = settings.SAVE_IMAGE_PATH
    
    path  = gobal_path + "/" + memfile.name
    with open(path, 'wb+') as destination:
        for chunk in memfile.chunks():
            destination.write(chunk)

    remote_url = "http://image.zj.yzdongfang.com/%s" % memfile.name
    return remote_url


def upload_memory_local_file(memfile, filename, data=None, _headers=None):
    gobal_path = settings.SAVE_IMAGE_PATH
    
    path  = gobal_path + "/" + filename
   

    with open(path, 'wb') as up:
        up.write(memfile)

    remote_url = "http://image.zj.yzdongfang.com/%s" % filename
    return remote_url , path


def upload_django_local_file(memfile, filename, data=None, _headers=None):
    gobal_path = settings.SAVE_IMAGE_PATH    
    path  = gobal_path + "/" + filename

    with open(path, 'wb') as up:
        up.write(memfile.read())

    remote_url = "%s/%s" % (settings.IMAGE_URL_HOST , filename)
    return remote_url



def save_tmp_file(f, path):
    
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def save_img(img_url, file_name):
    try:
       # 下载图片，并保存到文件夹中
        urllib.urlretrieve(img_url, filename=file_name)
    except IOError as e:
        logging.error('IOError: {}'.format(e))
    except Exception as e:
        logging.error(e)

