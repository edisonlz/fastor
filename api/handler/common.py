#coding=utf-8
import os,sys
from api.view.base import BaseHandler
from api.document.doc_tools import *
from django.conf import settings
from app.api_util.ip.ip_search import *
from redis_model.queue import Client
import datetime
import time
import logging

@handler_define
class IpToRegion(BaseHandler):
    

    @api_define("user", r'/api/ip/to/region', [
        Param('user_ip', True, str, "", "183.159.171.195", u'用户ip'),
    ], description="通过ip地址映射到省市", return_desc="""""")
    def get(self):
        
        user_ip = self.user_ip

        if self.has_arg('user_ip'):
            user_ip = self.arg('user_ip')

        region = IpToRegionSearch.search(user_ip)


        response = {
            "code": 200,
            "status": "success",
            "region":region,
            "user_ip":user_ip,
        }

        return self.write(response)




@handler_define
class AsyncDemo(BaseHandler):
    

    @api_define("AsyncDemo", r'/api/async/demo', [
        Param('user_id', True, str, "" , "123456" , u'用户ID'),
        Param('course_name', True, str, "","Ed老师的python课程" , u'课程名称'),
    ], description="[示例]处理异步事件", return_desc="""""")
    def get(self):
        
        user_id = self.arg("user_id")
        course_name = self.arg("course_name")

        data = {
            "user_id":user_id,
            "course_name":course_name,
        }

        dispatch_client = Client()
        dispatch_client.dispatch("demo.async.send", data)
        
   
        response = {
            "code": 200,
            "status": "success",
        }

        return self.write(response)







