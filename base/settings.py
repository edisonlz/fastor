# -*- coding: utf-8 -*-
import sys
import os.path

reload(sys)
sys.setdefaultencoding('utf-8')

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "site-packages"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "..", ".."))

from django.core.management import get_commands,load_command_class
from django.core.management import execute_from_command_line
from django.conf import settings as django_settings
from django.utils import importlib


def execute(*modules):
    load_django_settings(*modules)
    execute_from_command_line()


def load_django_settings(*modules):
    settings = {'MODULES': modules}
    kwargs = {}
    mods = []

    for module in modules:
        #try:
        mods.append(importlib.import_module('%s.settings' % module))
        #except ImportError, err:
        #raise ImportError("Could not import settings '%s' (Is it on sys.path?): %s" % (module, err))

    for module in modules:
        try:
            mods.append(importlib.import_module('%s.my_settings' % module))
        except ImportError:
            pass


    for mod in mods:
        if hasattr(mod, 'inti_params'):
            kwargs.update(getattr(mod, 'inti_params')())

    for mod in mods:
        if hasattr(mod, 'load_settings'):
            getattr(mod, 'load_settings')(settings, **kwargs)


    for mod in mods:
        if hasattr(mod, 'check_settings'):
            getattr(mod, 'check_settings')(settings)

    if not django_settings.configured:
        django_settings.configure(**settings)



def load_settings(settings, debug=False, **kwargs):
    ugettext = lambda s: s

    settings.update({
        

        'redis_settings': {
            "MQUEUE_BACKEND": {
                "servers": '127.0.0.1',
                "port": 6379,
                "db": 0,
                "password": "",
            },
        },
     
        'DEBUG': debug,
        'TEMPLATE_DEBUG': debug,
        'ALLOWED_HOSTS': ['*'],
        'HOST':"http://127.0.0.1:8000",

        'SAVE_IMAGE_PATH':"/tmp",
        "IMAGE_URL_HOST":"file:///private/tmp",

        #先设置为一天
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'fastor_db',  # Or path to database file if using sqlite3.
                'USER': 'root',  # Not used with sqlite3.
                'PASSWORD': '123456',  # Not used with sqlite3.
                'HOST': '127.0.0.1',  # Set to sempty string for localhost. Not used with sqlite3.
                'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
                'CHARSET': 'utf8',
                'OPTIONS': {
                    'init_command': 'SET storage_engine=INNODB; SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;set autocommit=1;',
                },
            },

            'slave': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'fastor_db',  # Or path to database file if using sqlite3.
                'USER': 'root',  # Not used with sqlite3.
                'PASSWORD': '123456',  # Not used with sqlite3.
                'HOST': '127.0.0.1',  # Set to sempty string for localhost. Not used with sqlite3.
                'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
                'CHARSET': 'utf8',
                'OPTIONS': {
                    'init_command': 'SET storage_engine=INNODB; SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;set autocommit=1;',
                },
            },

        },

        'DATABASE_ROUTERS': ['app.db_router.MainRouter'],
        'DATABASE_MAPPING': {},
        'DATABASE_READ_MAPPING': {},

    
        #'DISABLE_TRANSACTION_MANAGEMENT' : True,
        'LANGUAGES': [
                ('en', ugettext('English')),
                ('zh-cn', ugettext('Chinese')),
                                           ],

        'TRANSMETA_DEFAULT_LANGUAGE': 'zh-cn',
        'TIME_ZONE': 'Asia/Shanghai',
        'LANGUAGE_CODE': 'zh_cn',
        'SITE_ID': 1,
        'USE_I18N': True,
        'USE_L10N': True,
        'MEDIA_ROOT': '',
        'MEDIA_URL': '',
        'STATIC_ROOT': '',
        'STATIC_URL': '/static/',
        '': '/static/admin/',
        'STATICFIADMIN_MEDIA_PREFIXLES_FINDERS': [
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        ],
        'SECRET_KEY': '1234546',
        'TEMPLATE_LOADERS': (
                ('django.template.loaders.cached.Loader', (
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                )),
            ),

        'MIDDLEWARE_CLASSES': [
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.transaction.TransactionMiddleware',
            "app.middleware.profile_middleware.ProfileMiddleware",
            ],
        'AUTHENTICATION_BACKENDS': (
            "django.contrib.auth.backends.ModelBackend",
            ),
        'TEMPLATE_CONTEXT_PROCESSORS': (
            "django.core.context_processors.debug",
            "django.core.context_processors.i18n",
            "django.core.context_processors.media",
            "django.core.context_processors.request",
            'django.core.context_processors.static',
            "django.contrib.auth.context_processors.auth",),

        'ROOT_URLCONF': 'base.urls',
        'INSTALLED_APPS': [
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django.contrib.admin',
            'django.contrib.admindocs',
            ],
        'DATE_FORMAT': 'Y-m-d',
        'DATETIME_FORMAT': 'Y-m-d H:i',
        'TIME_FORMAT': 'H:i',


        "memcache_settings": {
            "func_cache": ["127.0.0.1:11211"],
        },

        'cache_expire_2H': 60 * 60 * 2,
        'cache_expire_1H': 60 * 60,
        'cache_expire_15M': 60 * 15,
        'cache_expire_30M': 60 * 30,
        'cache_expire_1M': 60,



    }, )


