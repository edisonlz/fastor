#coding=utf-8
import os

def load_settings(settings, debug=False, **kwargs):    
   settings["api"] = {
        "password": "123456",
    }


def check_settings(settings):
    pass


def load_tonardo_settings(tonardo_settings={}):
    tonardo_settings.update({
            'cookie_secret': 'c31e1ae472e605dbcd02c11563a3792f',

    })


