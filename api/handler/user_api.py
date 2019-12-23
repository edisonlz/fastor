# coding=utf-8
import os,sys
from api.view.base import BaseHandler , CachedPlusHandler
from api.document.doc_tools import *
from app.iclass.models import *
from app.iclass.utils import get_primary_key
import datetime
import time
import logging

        
@handler_define
class GetUserInfo(CachedPlusHandler):

    def get_cache_expire(self):
        return 60 * 1

    def get_cache_key(self):
        return {
            'user_id': self.arg('user_id', ''),
        }

    @api_define("GetUserInfo", r'/user/info/detail',
                [
                    Param('user_id', True, str, "", "201702071511512892383865", u'用户id'),
                ],
                description="""读取用户基本信息""",
                return_desc="""
                (0, '普通用户'),
                    (1, '老师'),
                    (2, '助教'),
                    (3, '教务'),
                    (4, '销售'),
                    (5, '系统用户'),
                    (6, '应用用户'),
                    (9, '测试帐号'),
                """
                )
    def get(self):
        user_id = self.arg('user_id')

        user = BaseUser.objects.filter(user_id=user_id).first()
        if not user:
            response = {
                "code": 0,
                "status": "fail",
                "msg": "用户不存在",
            }
            return self.write(result)


        response = {
            "status": "success",
            "code": 200,
            "user":user.to_json()
        }
        return self.write(response)




@handler_define
class CreateUser(BaseHandler):
    """用户注册"""

    @api_define("CreateUser", r'/api/create/user', [
        Param('from', True, str, "", "web", u'平台|android,ios,web'),
        Param('username', True, str, "", "15860608080", u'手机号'),
        Param('nickname', True, str, "", "", u'昵称'),
        Param('image_url', True, file, "", "", u'image_url 上传图片'),
        Param('password', True, str, "", "d785c99d298a4e9e6e13fe99e602ef42", u'MD5(password)'),
    ], description="用户注册", return_desc="""""")
    def post(self):
        
        register_from = self.arg("from", "web")
        channel_code = self.arg("channel", "")
        username = self.arg("username")
        image_url = self.arg('image_url')
        nickname = self.arg('nickname')
        password = self.arg("password")
        user_id = get_primary_key()
        
        user = BaseUser.objects.filter(username=username).first()

        if user:
            response = {
                "code": 0,
                "status": "fail",
                "msg": "用户已存在",
            }
            return self.write(response)
       
        user = BaseUser()
        user.user_id = get_primary_key()
        user.image_url = image_url
        user.username = username
        user.nickname = nickname
        user.password = password
        user.last_login_time = datetime.datetime.now()
        user.create_time = datetime.datetime.now()
        user.register_from = BaseUser.RegisterFromDic.get(register_from,0)
        user.save()


        response = {
            "code": 200,
            "status": "success",
            "msg": "请求成功",
        }

        return self.write(response)

@handler_define
class SetUserInfo(BaseHandler):

    @api_define("SetUserInfo", r'/user/info/set',
                [
                    Param('user_id', True, str, "", "201702071511512892383865", u'用户id'),
                    Param('nick_name', False, str, "", "", u'nick_name'),
                    Param('image_url', False, str, "", "", u'image_url'),
                ],
                description="更新用户基本信息",
                return_desc=""""""
                )
    def post(self):

        user_id = self.arg('user_id')
        nick_name = self.arg('nick_name', '')
        image_url = self.arg('image_url', '')

        user = BaseUser.objects.filter(user_id=user_id)
        if not user:
            result = {
                "status": "fail",
                "msg": "用户不存在",
                "code" : 0
            }
            return self.write(result)


        changed = False
        if nick_name:
            user.nickname = nick_name
            changed = True

        if image_url:
            user.image_url = image_url
            changed = True

        if changed:
            user.save()

        result = {
            "status": "success",
            "code" : 200
        }
        return self.write(result)



