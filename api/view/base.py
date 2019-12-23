#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The base handlers"""
import os
import sys
#
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../../../')))

import re
import hashlib
import functools
from api.util import render
from django.conf import settings
from tornado.web import RequestHandler
from wi_cache import PyPoolMemcache ,PyPoolUserMemcache , get_plus_json
import traceback
from tornado.web import HTTPError

import logging

def login_required(method):
    def auth_filter(api):
        api['need_login'] = True

    api_filters = getattr(method, 'api_filters', [])
    api_filters.append(auth_filter)
    setattr(method, 'api_filters', api_filters)

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user_id:
            raise HTTPError(401)
        return method(self, *args, **kwargs)

    return wrapper

def ip_limit_required(prefix, limits=100 , seconds=10* 60):
    
    def func(method):

        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            ip = self.user_ip
            ip_limit = "%s:ip_%s" % (prefix,str(ip))
            cache_ip_limit = PyPoolUserMemcache.get(ip_limit) or 0
            if int(cache_ip_limit) >= limits:
                ret = {"code": "0", "msg": "获取验证码次数受限"}
                return self.write(ret)
            else:
                PyPoolUserMemcache.set(ip_limit , cache_ip_limit+1 , seconds)

            return method(self, *args, **kwargs)
        return wrapper
    return func



class BaseHandler(RequestHandler):
    """The base handler of all other handlers"""

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.get = self._deco_method(self.get)
        self.post = self._deco_method(self.post)
        self.put = self._deco_method(self.put)
        self.delete = self._deco_method(self.delete)
        self.rt = None
        self.args = Arguments(self)


    def keyword_filte(self, content):
        return content
        #keyword.mark_filte(content)

    def out_content(self, content):
        return content
        #keyword.output(content)


    def has_arg(self, name):
        return self.request.arguments.has_key(name)

    def arg(self, name, default=RequestHandler._ARG_DEFAULT, strip=True):
        return self.get_argument(name, default, strip)

    def arg_int(self, name, default=RequestHandler._ARG_DEFAULT, strip=True):
        return int(self.get_argument(name, default, strip))

    def arg_bool(self, name):
        return self.arg(name, 'false') == 'true'




    def get_sign(self , param_map, skey):
        """生成签名"""
        sort_param = sorted(
            [(key, unicode(value).encode('utf-8')) for key, value in param_map.iteritems()],
            key=lambda x: x[0]
        )
        content = '&'.join(['='.join(x) for x in sort_param])
        
        sign_content = "{0}&key={1}".format(content, skey)
        logging.error(sign_content)
        
        smd5 = hashlib.md5()
        smd5.update(sign_content)
        d = smd5.hexdigest().upper()
        logging.error(d)
        return d



    def get_varnish_expire(self):
        """
        function: control varnish expire time
        """
        return 0

    def set_varnish_cache(self):
        """
        function: provide header 'max-age' to varnish server
        """
        if self.request.method not in ("GET"):
            return

        if self.settings.get("debug", False):
            return
        
        varnish_timeout = self.get_varnish_expire()
        r = None
        if varnish_timeout:
            if type(varnish_timeout) == int:
                #no more than 10m
                if varnish_timeout > 60 * 10:
                    varnish_timeout = 60 * 10
                r = "max-age=%s" % varnish_timeout
        else:
            r = 'max-age=0'

        if r:
            self.set_header("Cache-Control", r)
            
    def write(self, chunk):
        self.set_varnish_cache()  # add header max-age if you want to use varnish
        super(BaseHandler, self).write(self._format_result(chunk))

    def write_no_format(self, chunk):
        self.set_varnish_cache()  # add header max-age if you want to use varnish
        super(BaseHandler, self).write(chunk)

    def flush(self, include_footers=False):
        self._set_content_type()
        super(BaseHandler, self).flush(include_footers)

    def _format_result(self, chunk):
        if not isinstance(chunk, (bool, int, long, float, basestring)):
            if self.rt == 'xml':
                chunk = render.xml(chunk)
            else:
                chunk = render.json(chunk)
                if self.rt == 'text':
                    chunk = self.render_string('templates/json_format.html',
                                               json_content=chunk)
                else:
                    # jsonp supported
                    callback_func = self.get_argument('callback', '')
                    if callback_func:
                        chunk = '{}({})'.format(callback_func, chunk)
        return chunk

    def _set_content_type(self):
        if self.rt == 'xml':
            self.set_header('Content-Type', 'text/xml; charset=UTF-8')
        elif self.rt == 'json':
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
        elif self.rt == 'html':
            self.set_header('Content-Type', 'text/html')


    def _fix_rt(self, args):
        if not self.rt:
            self.rt = args[-1] or 'json'
            args = args[:-1]
        return args

    def _deco_method(self, fn):
        def _func(*args, **kwargs):
            args = self._fix_rt(args)
            setattr(self, '{}_args'.format(self.request.method), (args, kwargs))
            try:
                return fn(*args, **kwargs)
            except Exception, e:
                logging.error(e)
                logging.error(traceback.format_exc())
                return self.send_error(status_code=400, desc=str(e)+","+str(e.message))
        return _func

    def auth_login(self, user_id, expires_days=1*365):
        self.user_key = self.create_signed_value("user_token", str(user_id))
        self.set_cookie("user_token", self.user_key, expires_days=expires_days)
        self._current_user_id = user_id

    def auth_logout(self):
        self.clear_cookie("user_token")
        self._current_user = None

    def prepare(self):
        pass

    def get_cookie(self, name, default=None):
        if name == 'user_token' and self.has_arg('session_key'):
            return self.arg('session_key')
        return super(BaseHandler, self).get_cookie(name, default)

    @property
    def current_user(self):
        if not hasattr(self, "_current_user"):
            user_id = self.current_user_id
            try:
                user = User.objects.get(pk=user_id)
            except Exception:
                user = None
            finally:
                setattr(self, '_current_user', user)

        return getattr(self, "_current_user", None)
    
    @property
    def current_user_id(self):
        if not hasattr(self, "_current_user_id"):
            user_id = self.get_current_user()
            if user_id:
                setattr(self, "_current_user_id", user_id)
        return getattr(self, "_current_user_id", None)

    def get_current_user(self):
        return self.get_secure_cookie("user_token", max_age_days=30)

    @property
    def is_login(self):
        return self.current_user_id != None

    @property
    def user_ip(self):
        if not hasattr(self, '_real_ip'):
            self._real_ip = self.request.headers.get('X-Real-Ip',
                                                     self.request.remote_ip)

            if not "." in self._real_ip:
                self._real_ip = "127.0.0.1"

        return self._real_ip

    def get_error_html(self, status_code, **kwargs):
        """ error html """
        if status_code == 500:
            status_code = 400
            self.set_status(400)

        ext = kwargs.get('exception')
        http_status_code = status_code

        if ext:
            http_status_code = ext.__dict__.get("http_status_code", status_code)

        desc = {
            400: '未知错误，请稍候尝试。',
            405: 'method not allowed',
            401: 'login first',
        }
        if ext:
            try:
                desc[http_status_code] = str(ext)
            except Exception as e:
                logging.error(e)

        result = {
            'status': 'failed',
            'code': kwargs.get('code', status_code),
            'desc': kwargs.get('desc', desc.get(http_status_code, '')),
        }
        return result

class CachedHandler(BaseHandler):
    u"""
        利用_result_buffer来缓存输出结果对象
        并将这些对象存到缓存中
        flush时，根据rt的值将对象序列化再输出给客户端
    """

    P_PATH = re.compile(r'^(/.+?)(\.(json|xml|text))?$')
    enable_cache = True

    def __init__(self, *args, **kwargs):
        self.get = self._deco_get(self.get)
        super(CachedHandler, self).__init__(*args, **kwargs)
        self._result_buffer = []
        self.get_cache_key = self._deco_get_cache_key(self.get_cache_key)
        self._cache_key = None
        self._default_cache_expire = settings.cache_expire_1H
        self._is_update_cache = None

    @property
    def is_update_cache(self):
        if self._is_update_cache is None:
            value = self.request.headers.get('Is-Update-Cache', '').upper()
            self._is_update_cache = value == 'YES'
        return self._is_update_cache

    def write(self, chunk):
        if chunk is not None:
            self._result_buffer.append(chunk)

    def flush(self, include_footers=False):
        self._flush_result_buffer()
        super(CachedHandler, self).flush(include_footers)

    def finish(self, chunk=None):
        if chunk is not None:
            self.write(chunk)
        self._flush_result_buffer()
        super(CachedHandler, self).finish()

    def _flush_result_buffer(self):
        for r in self._result_buffer:
            super(CachedHandler, self).write(r)
        self._result_buffer = []

    def _deco_get(self, fn):
        def _func(*args):
            args = self._fix_rt(args)
            if settings.DEBUG:
                fn(*args)
            else:
                # check cache
                ckey = self.get_cache_key()
                value = None if self.is_update_cache else PyPoolMemcache.get(ckey)
                if value is None:
                    fn(*args)
                    if self.get_status() in (200, 304) and self._result_buffer:
                        PyPoolMemcache.set(ckey, self._result_buffer,
                                       self.get_cache_expire())
                else:
                    self._result_buffer = value

        return _func


    def get_cache_expire(self):
        return self._default_cache_expire

    def get_cache_key(self):
        args_map = self.request.arguments.copy()
        # ignore pid uid guid
        args_map.pop('pid', None)
        args_map.pop('guid', None)
        args_map.pop('s', None)
        args_map.pop('t', None)
        args_map.pop('e', None)
        args_map.pop('_s_', None)
        args_map.pop('_t_', None)
        return args_map

    def _deco_get_cache_key(self, fn):
        def _func(*args, **kwargs):
            if not self._cache_key:
                path = self.request.path
                _mo = CachedHandler.P_PATH.match(path)
                if _mo:
                    path = _mo.group(1)
                _k = fn(*args, **kwargs)
                #sort by key
                sorted_keys = sorted(_k.items(), key=lambda x: x[0])
                params = []
                for i in sorted_keys:
                    params.append( "%s=%s" % (i[0], i[1]) )
                _k = '{}?{}'.format(path, "&".join(params))
                _k = hashlib.md5(_k).hexdigest()[8:24]
                self._cache_key = _k
            return self._cache_key
        return _func


class CachedPlusHandler(CachedHandler):
    """支持容错"""
    def _deco_get(self, fn):
        def _func(*args):
            args = self._fix_rt(args)
            if settings.DEBUG:
                fn(*args)
            else:
                def real_get():
                    fn(*args)
                    if self.get_status() == 200:
                        return self._result_buffer
                    else:
                        return None

                key = self.get_cache_key()
                expire_m = self.get_cache_expire()
                expire_s = None
                cached_result = get_plus_json(
                    key, real_get, expire_m,
                    expire_s, self.is_update_cache)

                if type(cached_result) == list:
                    if len(cached_result) >0 :
                        if "api.expired_at" in cached_result[0]:
                            cached_result[0].pop("api.expired_at")
                elif type(cached_result) == dict:
                    if "api.expired_at" in cached_result:
                            cached_result.pop("api.expired_at")

                self._result_buffer = cached_result or self._result_buffer

        return _func


class Arguments(object):
    """The request arguments handler"""

    def __init__(self, req_handler):
        self._req_handler = req_handler
        self._args_define_list = []
        self._args_map = {}
        self._parsed = False

    def define(self, arg_name, cover_func=None, default=None):
        assert isinstance(arg_name, str)
        self._args_define_list.append((arg_name, cover_func, default))
        self._parsed = False

    def to_dict(self):
        return self._args_map.copy()

    def _do_parse(self):
        for arg_name, cover_func, default in self._args_define_list:
            arg_value = self._req_handler.get_argument(arg_name, None)
            if arg_value is None:
                arg_value = default
            elif cover_func is not None:
                arg_value = cover_func(arg_value)
            self._args_map[arg_name] = arg_value

    def __getattr__(self, name):
        if not self._parsed:
            self._do_parse()
            self._parsed = True
        return self._args_map.get(name, None)

    def __setattr(self, name, value):
        raise RuntimeError('__setattr__ not allowed')


def varnish_cache(timeout=60):
    
    def func(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            r = method(self, *args, **kwargs)
            if self.get_status() == 200:
                
                if type(timeout) == int:
                    r = "max-age=%s" % timeout
                else:
                    r = timeout #no cache
                self.set_header("Cache-Control", r)
            return r
