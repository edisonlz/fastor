#coding=utf-8
import re
import hashlib
import functools
import sys,os
import datetime
from django.shortcuts import render

def check_role_required(role=1):
    
    def func(method):

        @functools.wraps(method)
        def wrapper(request, *args, **kwargs):
            
            if request.user.role == 0:
                return method(request, *args, **kwargs)


            if request.user.role == role:
                return method(request, *args, **kwargs)
            else:
                return render(request, 'permission_deny.html')

        return wrapper
    return func
