# coding=utf-8
import os, sys
import random

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "site-packages"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "..", ".."))

BASE_DIR =  os.path.join(PROJECT_ROOT,'..','base', "site-packages" ,"django_admin_bootstrapped")

def load_settings(settings, debug=False, **kwargs):
    settings.update(
        {
            'TEMPLATE_LOADERS': (
                (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ),
            ),

            'DEBUG': debug,
            'TEMPLATE_DEBUG': debug,
            'TEST': False,
            'APK_UPLOAD_PATH': "/tmp/data/download",
            'PROJECT_ROOT': PROJECT_ROOT,
            'ANONYMOUS_USER_ID': -1,

            'TEMPLATE_DIRS': (
                os.path.join(PROJECT_ROOT, "templates"),
                os.path.join(PROJECT_ROOT, "iclass/templates"),
                os.path.join(PROJECT_ROOT, "user/templates"),
                os.path.join(BASE_DIR, "templates"),
            ),
            'ROOT_URLCONF': 'app.urls',
            'STATICFILES_FINDERS': [
                'django.contrib.staticfiles.finders.FileSystemFinder',
                'django.contrib.staticfiles.finders.AppDirectoriesFinder',
            ],
            'STATICFILES_DIRS': (
                os.path.join(PROJECT_ROOT, 'statics'),
            ),
            'TEMPLATE_CONTEXT_PROCESSORS': (
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.request",
                'django.core.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                "django.contrib.auth.context_processors.auth",),

            'MIDDLEWARE_CLASSES': [
                'django.middleware.common.CommonMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
                'django.middleware.transaction.TransactionMiddleware',
                'app.middleware.profile_middleware.ProfileMiddleware',
            ],

            'AUTH_USER_MODEL': 'user.User',

            'INSTALLED_APPS': [
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                'django.contrib.admin',
                'django.contrib.admindocs',
                #'django_extensions',
                'app.user',
                'app.iclass',
                # 'south',
            ],
            "LOGIN_URL": "/signin",
            "LOGIN_REDIRECT_URL": "/",
           
    }
    )
    ugettext = lambda s: s


def check_settings(settings):
    pass

