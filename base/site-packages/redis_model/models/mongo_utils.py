# -*- coding: UTF-8 -*-
import os, sys
import datetime, time
from redis_model.redis_client import RedisClient

try:
    from functools import wraps, update_wrapper
except ImportError:
    from django.utils.functional import wraps, update_wrapper  # Python 2.3, 2.4 fallback.

def queryset_to_dict(qs, key='id'):
    """ Given a queryset will transform it into a dictionary based on ``key``. """
    return dict((str(getattr(u, key)), u) for u in qs)


def find_include(ref_klass, pks, scores, withscore):
    """ search the related object from current object """
    if not pks:
        return []

    rd = ref_klass.objects.filter(id__in=pks)
    print ref_klass, pks

    qs = queryset_to_dict(rd)
    results = []
    for pk in pks:
        obj = qs[pk]
        if withscore and obj:
            setattr(obj, "rd_score", scores[str(obj.id)])
        if obj:
            results.append(obj)
    return results


def operKey(obj, field):
    """ generate operate Key """
    return "%s:id:%s:%s" % (obj.__class__.__name__, obj.id, field)


def operSet(fn):
    """ this Decoration method for add operation """

    def _new(self, *args, **kws):
        try:
            baseobj = args[0]
            obj = args[1]
            if not obj:
                raise StandardError("please input dest object")

            if hasattr(obj, "id") or hasattr(obj, "_id"):
                key = operKey(baseobj, self.name)
                kws["obj"] = obj
                kws["baseobj"] = baseobj
                member_id = obj.id
                if hasattr(obj, "_multi_score_id_"):
                    member_id = str(getattr(obj, "_multi_score_id_"))
                return fn(self, key, member_id, **kws)
            else:
                raise StandardError("please object is new not have object.id")
        except Exception, e:
            return False

    return wraps(fn)(_new)


def operGet(fn):
    """ this is Decoration method get opearte """

    def _new(self, *args, **kws):
        try:
            obj = args[0]
            #print obj.id
            if hasattr(obj, "id") or hasattr(obj, "_id"):
                key = operKey(obj, self.name)
                args = args[1:]
                kws["obj"] = obj
                return fn(self, key, *args, **kws)
            else:
                raise StandardError("please object is new not have object.id")
        except Exception, e:
            print e

    return wraps(fn)(_new)

