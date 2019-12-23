# -*- coding: utf-8 -*-
import re
from functools import wraps
from api.document.doc_globe import api_manager
from api.document.doc_base import *
from api.view.base import CachedHandler,CachedPlusHandler
import importlib

def api_define(name, uri, params=[], result=None, filters=[], description='', add_user=False, api_type=1, wiki='', protocal="http",return_desc=""):

    def wrap(method):
        if not hasattr(method, 'apis'):
            setattr(method, 'apis', [])

        params.append(Param('doc', True, str, "1", "1", u'doc for debug'))
        params.append(Param('_os_', False, str, "Android", ["Android", "iPhone OS"], u'os这个字段出自header，这里for test'))
        params.append(Param('ver', False, str, "1.0", "1.0", u'版本'))
        params.append(Param('from', False, str, "ios", "ios", u'平台(android|ios|web)'))

        getattr(method, 'apis').append(
            ApiDefined(name, method.__name__.upper(), uri, params, result, module=method.__module__, filters=filters,
                       description=description, api_type=api_type, wiki=wiki,protocal=protocal,return_desc=return_desc))
        return method

    return wrap


def handler_define(cls):
    for m in [getattr(cls, i) for i in dir(cls) if callable(getattr(cls, i)) and hasattr(getattr(cls, i), 'apis')]:
        method_filters = getattr(m, 'api_filters', None)

        for api in m.apis:
            api['cached'] = issubclass(cls, CachedHandler) or issubclass(cls, CachedPlusHandler)
            api['handler'] = cls
            if method_filters:
                for f in method_filters:
                    f(api)
            if api['filters']:
                for f in api['filters']:
                    f(api)

            from api.document.doc_globe import api_manager
            global api_manager
            
            api_manager.addapi(api)
    return cls


def suburls(prefix=ur'/', suburl=[]):
    _urls = []
    for u, h in suburl:
        _urls.append((prefix + u, h))
    return _urls

log_formatter = logging.Formatter(fmt="[%(levelname)s:%(asctime)s:%(filename)s:%(lineno)d] %(message)s")

logging_data = []
max_logging_size = 300
url_extractor = re.compile(r"(GET|POST) ([^\s]+) ")

def hook_logging(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        rv = f(*args, **kwargs)
        try:
            if rv:
                global logging_data
                if len(logging_data) >= max_logging_size:
                    logging_data = logging[(max_logging_size/2):]

                def url_repl(matchobj):
                    try:
                        uri = matchobj.group(2)
                        repl = "%s <a href='%s' title='%s' target='blank'>%s</a>" % (matchobj.group(1),uri,uri,uri)
                        return repl
                    except IndexError:
                        pass

                css_dict = {
                    logging.DEBUG: "text-info",
                    logging.INFO: "text-success",
                    logging.WARNING: "text-warning",
                    logging.ERROR: "text-error",
                    logging.CRITICAL: "text-error",
                }

                _log = log_formatter.format(rv)
                _log = url_extractor.sub(url_repl, _log)
                _log = ("<p class='%s'>" % css_dict.get(rv.levelno, "muted")) + _log + "</p>"
                logging_data.append(_log)

        except Exception,e:
            pass
        return rv

    return wrap


def profile_patch(execute):
    def _(self, transforms, *args, **kwargs):
        #if options.is_debug and options.is_profile:
        if hasattr(self, "is_profile") and self.is_profile:
            self.profiler = profile.Profile()
            io = StringIO.StringIO()
            result = self.profiler.runcall(execute, self, transforms, *args, **kwargs)
            self.profiler.create_stats()
            stats = pstats.Stats(self.profiler, stream=io)
            stats.strip_dirs().sort_stats('cum')
            stats.print_stats(60)
            r = '<pre>%s</pre>' % io.getvalue()
            logging.debug(r)
            return result
        else:
            return execute(self, transforms, *args, **kwargs)
    return _


def load_api_doc(path, debug=False):

    from api.document import doc_view
    from api.document.doc_insall_handlers import INSTALL_HANDLERS

    for module in INSTALL_HANDLERS:
        importlib.import_module(module)

    global api_manager
    apiurls = api_manager.get_urls()
    apiurls = [(r'{0}\.?(json|xml|text)?'.format(i), j) for (i, j) in apiurls]
    apiurls = suburls(ur'(?:/openapi-wireless)?', apiurls)

    #rest set
    resturls = []
    for uri in apiurls:
        ruri = uri[0]
        name = uri[1].__module__
        api_handler = name.split(".")[1]
        ruri = ruri.replace(":id", "([^/]+?)")
        ruri = ruri.replace(":xid", "(X[^/]+?|\d+?)")
        ruri = ruri.replace(":uid", "(U.+?)")
        ruri = ruri.replace(":keyword", "([^/]+?)$")
        resturls.append((ruri, uri[1],))

    apiurls = resturls
    app_settings = {}

    if debug:
        apiurls = apiurls + [
           # (r"/test/websocket$", doc_view.ThirdPartLoginPage),
           (r'/upload$',doc_view.TestUpload),
           (r'/signin$',doc_view.SigninHandler),
           (r'/signout$',doc_view.SignoutHandler),
            (r"/doc$", doc_view.ApiDocHandler),
            (r"/doc/example$", doc_view.ApiExampleHandler),
          #  (r"/debug/clear_cache$", doc_view.ApiClearCacheHandler),
            (r"/doc/logging/data", doc_view.ApiLoggingDataHandler),
            (r"/map$", doc_view.ApiMapHandler),
            (r'/test_url$', doc_view.BenmarkUrl),
        ]

        app_settings = {
            "template_path": os.path.join(path, "document"),
            "static_path": os.path.join(path, "document", "templates", "docs"),
            "static_url_prefix": '/doc/static/',
        }

#         #hook logging
        from logging import root
        root.makeRecord = hook_logging(root.makeRecord)
#        logging.info = hook_logging(logging.info)
#        logging.error = hook_logging(logging.error)
#        logging.warning = hook_logging(logging.warning)
#        logging.fatal = hook_logging(logging.fatal)

        from tornado import web
        old_execute = web.RequestHandler._execute
        web.RequestHandler._execute = profile_patch(old_execute)
    return apiurls, app_settings

