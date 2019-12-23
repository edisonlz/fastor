# coding=utf-8
import tornado.web
import simplejson
import tornado
from api.document.doc_globe import api_manager

from doc_insall_handlers import INSTALL_HANDLERS_NAME
#
# class ThirdPartLoginPage(tornado.web.RequestHandler):
#
# def get(self):
# self.render('templates/docs/websocket.html',**{})

class TestUpload(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write('''
    <html>
    <head><title>Upload File</title></head>
    <body>
    <form action='/upload/img' enctype="multipart/form-data" method='post'>
    <input type='file' name='file'/><br/>
    <input type='text' name='user_id'/><br/>

    <input type='submit' value='submit'/>
    </form>
    </body>
    </html>
    ''')


def request_login(method):
    def wrapper(self, *args, **kwargs):
        api_doc = self.cookies.get("api_doc")
        if api_doc and api_doc.value == "allow":
            return method(self, *args, **kwargs)
        else:
            self.redirect('/signin')
    return wrapper


class ApiDocHandler(tornado.web.RequestHandler):
    @request_login
    def get(self):
        global api_manager
        api_type = self.get_argument('api_type', '1')
        all_apis = api_manager.get_apis(name=self.get_argument('name', None), module=self.get_argument('module', None),
                                        handler=self.get_argument('handler', None),
                                        api_type=api_type)
        apis = {}
        for api in all_apis:
            if not apis.has_key(api.module):
                apis[api.module] = []

            apis[api.module].append(api)


        App = type('App', (object,), {'name': "api", })
        app = App()

        self.set_header('Content-Type', 'text/html; charset=utf-8')
        self.render('templates/docs/api_docs.html',
                    **{'tornado': tornado, 'apis': apis, 'api_base': self.settings.get("api_base", ''), \
                       'test_app_key': "", 'test_app': app, "module_names":INSTALL_HANDLERS_NAME,
                       'test_user_name': self.settings.get("test_user_name", ''), "api_type": api_type})



class ApiMapHandler(tornado.web.RequestHandler):
    def get(self):
        all_apis = api_manager.get_apis(name=self.get_argument('name', None), module=self.get_argument('module', None),
                                        handler=self.get_argument('handler', None))
        apis = {}
        for api in all_apis:
            if not apis.has_key(api.module):
                apis[api.module] = []
            apis[api.module].append(api)

        self.set_header('Content-Type', 'text/html; charset=utf-8')
        self.render('templates/docs/api_map.html', **{'apis': apis, 'api_base': self.settings.get("api_base", ''), })


class ApiLoggingDataHandler(tornado.web.RequestHandler):
    def get(self):
        from api.document.doc_tools import logging_data

        global logging_data
        data = logging_data[::-1]
        min_len = 15
        if len(data) < min_len:
            for i in xrange(min_len - len(data)):
                data.append("<p class='text-success'>...</p>")

        result = simplejson.dumps(data)
        self.write(result)


# class ApiClearCacheHandler(tornado.web.RequestHandler):
#
# def get(self):
# import pylibmc
#
#         mc = pylibmc.Client(['10.105.28.41:11211',], binary=True,
#                                 behaviors={"tcp_nodelay": True, "ketama": True})
#         mc.flush_all()
#         mc = pylibmc.Client(['10.105.28.41:22120',], binary=True,
#                                 behaviors={"tcp_nodelay": True, "ketama": True})
#         mc.flush_all()
#         self.write({"status":"ok"})

# class ApiAppKeyHandler(tornado.web.RequestHandler):
#     def get(self):
#         app_keys = {}
#         self.write(simplejson.dumps(app_keys))


class ApiExampleHandler(tornado.web.RequestHandler):
    def get(self):
        id = self.get_argument('id')
        parts = id.split('.')
        data = {}
        try:
            for p in parts:
                data = (type(data) is dict) and data[p] or getattr(data, p)
        except Exception, e:
            data = ''
        if hasattr(data, 'val'):
            v = data.val()
        else:
            v = data
        if type(v) in (list, tuple, dict):
            if v:
                self.write(simplejson.dumps(v, indent=True))
            else:
                self.write('null')
        else:
            self.write(v)


class BenmarkUrl(tornado.web.RequestHandler):
    def get(self):

        api_type = self.get_argument('api_type', '1')
        all_apis = api_manager.get_apis(name=self.get_argument('name', None), module=self.get_argument('module', None),
                                        handler=self.get_argument('handler', None),
                                        api_type=api_type)
        apis = {}
        for api in all_apis:
            if not apis.has_key(api.module):
                apis[api.module] = []
            params = []
            api_uri = api.uri
            for p in api.params:
                if p.name in (":id", ":uid", ":xid", ":keyword"):
                    api_uri = api_uri.replace(p.name, str(p.example or p.default))
                    continue
                if p.required or p.name == "_cookie":
                    if p.default:
                        params.append("%s=%s" % (p.name, p.default))
                    elif str(p.example):
                        params.append("%s=%s" % (p.name, p.example))

            test_url = api_uri + "?" + '&'.join(params)
            setattr(api, "test_url", test_url)
            apis[api.module].append(api)

        self.set_header('Content-Type', 'text/html; charset=utf-8')
        self.render('templates/docs/api_test_docs.html', **{'tornado': tornado, 'apis': apis})


class SigninHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/docs/api_login.html', **{'tornado': tornado, 'alert': 0})

    def post(self):
        from django.conf import settings

        username = self.get_argument('username', "")
        password = self.get_argument('password', "")

        if username == 'admin' and password == settings.api.get("password"):
            self.set_cookie("api_doc", "allow")
            self.redirect('/doc')
        else:
            self.set_header('Content-Type', 'text/html; charset=utf-8')
            self.render('templates/docs/api_login.html', **{'tornado': tornado, 'alert': 1})


class SignoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("api_doc")
        self.redirect('/signin')




