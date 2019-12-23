# -*- coding: utf-8 -*-

import time
import random
import hmac, hashlib
import binascii
import base64
from urlparse import urlparse
from tencentyun import conf

class Auth(object):

    def __init__(self, secret_id, secret_key):
        self.AUTH_URL_FORMAT_ERROR = -1
        self.AUTH_SECRET_ID_KEY_ERROR = -2

        self._secret_id,self._secret_key = secret_id,secret_key

    
    def get_app_sign_v2(self, bucket, fileid, expired=0, userid='0'):
        """ GET V2 SIGN USE FILEID 
        copy and del operation must have fileid and set expired=0

        Args:
            bucket: user bucket
            fileid: user defined fileid, not urlencoded
            expired: expire time
            userid: user id, pls ignore or set to '0'
        """
        
        if isinstance(fileid, unicode):
            fileid = fileid.encode("utf-8")

        if not self._secret_id or not self._secret_key:
            return self.AUTH_SECRET_ID_KEY_ERROR

        app_info = conf.get_app_info()
        appid = app_info['appid']

        puserid = ''
        if userid != '':
            if len(userid) > 64:
                return self.AUTH_URL_FORMAT_ERROR
            puserid = userid

        now = int(time.time())
        rdm = random.randint(0, 999999999)
        plain_text = 'a=' + appid + '&b=' + bucket +'&k=' + self._secret_id + '&e=' + str(expired) + '&t=' + str(now) + '&r=' + str(rdm) + '&u=' + puserid + '&f=' + fileid
        
        bin = hmac.new(self._secret_key, plain_text, hashlib.sha1)
        s = bin.hexdigest()
        s = binascii.unhexlify(s)
        s = s + plain_text
        signature = base64.b64encode(s).rstrip()    #生成签名
        return signature

    def get_info_from_url(self, url):
        app_info = conf.get_app_info()
        end_point = app_info['end_point']
        info = urlparse(url)
        end_point_info = urlparse(end_point)
        if (info.hostname == urlparse(conf.API_IMAGE_END_POINT).hostname or info.hostname == urlparse(conf.API_VIDEO_END_POINT).hostname) :
            # 非下载url
            if info.path :
                parts = info.path.split('/')
                if len(parts) == 5:
                    cate = parts[1]
                    ver = parts[2]
                    appid = parts[3]
                    userid = parts[4]
                    return {'cate':cate, 'ver':ver, 'appid':appid, 'userid':userid}
                elif len(parts) == 6:
                    cate = parts[1]
                    ver = parts[2]
                    appid = parts[3]
                    userid = parts[4]
                    fileid = parts[5]
                    return {'cate':cate, 'ver':ver, 'appid':appid, 'userid':userid, 'fileid':fileid}
                elif len(parts) == 7:
                    cate = parts[1]
                    ver = parts[2]
                    appid = parts[3]
                    userid = parts[4]
                    fileid = parts[5]
                    oper = parts[6]
                    return {'cate':cate, 'ver':ver, 'appid':appid, 'userid':userid, 'fileid':fileid, 'oper':oper}
                else:
                    return {}
            else:
                return {}
        else :
            if info.path :
                parts = info.path.split('/')
                if len(parts) == 5:
                    appid = parts[1]
                    userid = parts[2]
                    fileid = parts[3]
                    style = parts[4]
                    return {'appid':appid, 'userid':userid, 'fileid':fileid, 'style':style}
                else:
                    return {}
            else:
                return {}

    def get_info_from_url_v2(self, url):
        app_info = conf.get_app_info()
        end_point = app_info['end_point_v2']
        info = urlparse(url)
        end_point_info = urlparse(end_point)
        if (info.hostname == urlparse(conf.API_IMAGE_END_POINT_V2).hostname) :
            # 非下载url
            if info.path :
                parts = info.path.split('/')
                if len(parts) == 6:
                    cate = parts[1]
                    ver = parts[2]
                    appid = parts[3]
                    bucket = parts[4]
                    userid = parts[5]
                    return {'cate':cate, 'ver':ver, 'appid':appid, 'bucket':bucket, 'userid':userid}
                elif len(parts) == 7:
                    cate = parts[1]
                    ver = parts[2]
                    appid = parts[3]
                    bucket = parts[4]
                    userid = parts[5]
                    fileid = parts[6]
                    return {'cate':cate, 'ver':ver, 'appid':appid, 'bucket':bucket, 'userid':userid, 'fileid':fileid}
                elif len(parts) == 8:
                    cate = parts[1]
                    ver = parts[2]
                    appid = parts[3]
                    bucket = parts[4]
                    userid = parts[5]
                    fileid = parts[6]
                    oper = parts[7]
                    return {'cate':cate, 'ver':ver, 'appid':appid, 'bucket':bucket, 'userid':userid, 'fileid':fileid, 'oper':oper}
                else:
                    return {}
            else:
                return {}
        else :
            if info.path :
                parts = info.path.split('/')
                if len(parts) == 5:
                    arr = parts[1].split('-')
                    if len(arr) != 2:
                        return {}
                    bucket = arr[0]
                    appid = arr[1]
                    userid = parts[2]
                    fileid = parts[3]
                    style = parts[4]
                    return {'appid':appid, 'bucket':bucket, 'userid':userid, 'fileid':fileid, 'style':style}
                else:
                    return {}
            else:
                return {}                

    def app_sign_v2(self, url, expired=0):
        if not self._secret_id or not self._secret_key:
            return self.AUTH_SECRET_ID_KEY_ERROR

        url_info = self.get_info_from_url_v2(url)

        if len(url_info) == 0:
            return self.AUTH_URL_FORMAT_ERROR

        if 'cate' in url_info:
            cate    = url_info['cate']
        else:
            cate = ''
        if 'ver' in url_info:    
            ver     = url_info['ver']
        else:
            ver = ''

        appid   = url_info['appid']
        bucket  = url_info['bucket']
        userid  = url_info['userid']
        
        if 'oper' in url_info:
            oper = url_info['oper']
        else:
            oper = ''
        if 'fileid' in url_info:
            fileid  = url_info['fileid']
        else:
            fileid = ''
        if 'style' in url_info:
            style = url_info['style']
        else:
            style = ''

        once_opers = ['del', 'copy']
        if oper in once_opers:
            expired = 0
        if not oper and not style and fileid:
            fileid = ''

        puserid = ''
        if userid != '':
            if len(userid) > 64:
                return self.AUTH_URL_FORMAT_ERROR
            puserid = userid

        now = int(time.time())
        rdm = random.randint(0, 999999999)
        plain_text = 'a=' + appid + '&k=' + self._secret_id + '&e=' + str(expired) + '&t=' + str(now) + '&r=' + str(rdm) + '&u=' + puserid + '&f=' + fileid
        bin = hmac.new(self._secret_key, plain_text, hashlib.sha1)
        s = bin.hexdigest()
        s = binascii.unhexlify(s)
        s = s + plain_text.encode('ascii')
        signature = base64.b64encode(s).rstrip()    #生成签名
        return signature

    def app_sign(self, url, expired=0):
        if not self._secret_id or not self._secret_key:
            return self.AUTH_SECRET_ID_KEY_ERROR

        url_info = self.get_info_from_url(url)

        if len(url_info) == 0:
            return self.AUTH_URL_FORMAT_ERROR

        if 'cate' in url_info:
            cate    = url_info['cate']
        else:
            cate = ''
        if 'ver' in url_info:    
            ver     = url_info['ver']
        else:
            ver = ''

        appid   = url_info['appid']
        userid  = url_info['userid']
        
        if 'oper' in url_info:
            oper = url_info['oper']
        else:
            oper = ''
        if 'fileid' in url_info:
            fileid  = url_info['fileid']
        else:
            fileid = ''
        if 'style' in url_info:
            style = url_info['style']
        else:
            style = ''

        once_opers = ['del', 'copy']
        if oper in once_opers:
            expired = 0

        puserid = ''
        if userid != '':
            if len(userid) > 64:
                return self.AUTH_URL_FORMAT_ERROR
            puserid = userid

        now = int(time.time())
        rdm = random.randint(0, 999999999)
        plain_text = 'a=' + appid + '&k=' + self._secret_id + '&e=' + str(expired) + '&t=' + str(now) + '&r=' + str(rdm) + '&u=' + puserid + '&f=' + fileid
        bin = hmac.new(self._secret_key, plain_text, hashlib.sha1)
        s = bin.hexdigest()
        s = binascii.unhexlify(s)
        s = s + plain_text.encode('ascii')
        signature = base64.b64encode(s).rstrip()    #生成签名
        return signature

