#coding=utf-8

from django.conf import settings
import random

class MainRouter(object):

    def db_for_read(self, model, **hints):
        db_setting = settings.DATABASE_READ_MAPPING.get(model._meta.app_label)

        if db_setting:
            return db_setting

        return 'default'

    def db_for_write(self, model, **hints):
        db_setting = settings.DATABASE_MAPPING.get(model._meta.app_label)
        if db_setting:
            return db_setting

        return 'default'

    def allow_relation(self, obj1, obj2, **hints):

        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        return False

    def allow_syncdb(self, db, model):

        db_setting = settings.DATABASE_MAPPING.get(model._meta.app_label)
        if db_setting:
            return False
        else: 
            return True
        
