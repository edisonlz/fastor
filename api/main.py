#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
#import library
sys.path.insert(0, os.path.join(PROJECT_ROOT, '..', 'base', "site-packages"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.insert(0, os.path.join(PROJECT_ROOT, '..'))

from base.settings import load_django_settings
from settings import load_tonardo_settings

load_django_settings('fastor.base', 'fastor.app', 'fastor.api')

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import logging
import settings
from api.document.doc_tools import load_api_doc


def init_options():
    tornado.options.define('port', default=11000, type=int)
    tornado.options.define('worker', default=2, type=int)
    tornado.options.define('debug', default=False, type=bool)
    tornado.options.define('doc', default=True, type=bool)
    tornado.options.define('timeout', default=2, type=int)
    tornado.options.parse_command_line()

    return tornado.options.options


def main():
    _options = init_options()

    # 设置全局socket超时时间
    import socket

    socket.setdefaulttimeout(_options.timeout)
    settings.is_debug = _options.debug
    settings.is_doc = _options.doc

    # FIXME: 找不到templates目录
    apiurls, app_settings = load_api_doc(PROJECT_ROOT, _options.doc)
    url_list = apiurls
    load_tonardo_settings(app_settings)

    
    application = tornado.web.Application(url_list, debug=_options.debug, **app_settings)

    _httpserver = tornado.httpserver.HTTPServer(application, no_keep_alive=True)
    _httpserver.bind(_options.port)


    _httpserver.start(1 if _options.debug else _options.worker)
    logging.info("httpserver thread {} worker,domain http://{}:{},debug={},logging={}".format(str(_options.worker),
                                                                                              str(socket.gethostname()),
                                                                                              str(_options.port),
                                                                                              str(_options.debug),
                                                                                              str(_options.logging)))
    logging.info(
        "http://" + str(socket.gethostname()) + ":" + str(_options.port) + '/urls?pid=127f7a5e3a366bd0&kind=1' + " ")
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()


