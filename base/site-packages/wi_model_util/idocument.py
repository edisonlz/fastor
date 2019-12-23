#encoding = utf-8
import StringIO
import datetime, time
import os, sys
from mongoengine import Document

def queryset_2_dict(qs, key='id'):
    """ Given a queryset will transform it into a dictionary based on ``key`` """
    dic = {}
    for q in qs:
        value = q._data.get(key)
    if value:
        k = value.__dict__.get("_DBRef__id")
        if k:
            #print k ,q
            k = str(k)
            dic.setdefault(k, [])
            dic[k].append(q)
    return dic


def distinct(l):
    """ Given an iterable will return a list of all distinct values """
    return list(set(l))


def attach_one_to_many(objects, doc, field="comments", ref_id="feed", order="feed_id,-create_time"):
    """
     Shortcut method which handles a pythonic LEFT OUTER JOIN.
     ``attach_foreignkey(posts, Post.thread)``
     """
    if objects:
        docs = doc.objects.filter(feed__in=objects).order_by(order)
        queryset = queryset_2_dict(docs, ref_id)
        data = []
        for o in objects:
            #print o ,"-", field , "-" , queryset.get(getattr(o, "id"),[])
            setattr(o, field, queryset.get(str(getattr(o, "id")), []))
            data.append(o)
    return data


def queryset_to_dict(qs, key):
    """
     Given a queryset will transform it into a dictionary based on ``key``.
     """
    dic = {}
    if qs:
        for q in qs:
            dic[str(q.id)] = q
    return dic


def attach_ref_user(objects, doc, ref="user"):
    """
     Shortcut method which handles a pythonic LEFT OUTER JOIN.
     ``attach_foreignkey(posts, Post.thread)``
     """
    if objects:
        keys = []
        _objects = []
        for q in objects:
            value = q._data.get(ref)
            k = value.__dict__.get("_DBRef__id")
            if k:
                setattr(q, "__user_id", str(k))
                keys.append(str(k))
            _objects.append(q)

        qs = doc.objects.filter(id__in=distinct(keys))
        queryset = queryset_to_dict(qs, ref)
        for o in _objects:
            setattr(o, ref, queryset.get(getattr(o, "__user_id")))
        return _objects


def attach_ref(doc, objects, ref):
    """ attach_foreignkey(Post.thread , posts) """
    if objects:
        keys = []
        _objects = []
        for q in objects:
            value = q._data.get(ref)
            k = value.__dict__.get("_DBRef__id")
            if k:
                setattr(q, "__%s_id" % ref, str(k))
                keys.append(str(k))
            _objects.append(q)

        qs = doc.objects.filter(id__in=distinct(keys))
        queryset = queryset_to_dict(qs, ref)
        for o in _objects:
            setattr(o, ref, queryset.get(getattr(o, "__%s_id" % ref)))
        return _objects


def attach_raw_ref(doc, objects, ref):
    """ attach_foreignkey(Post.thread , posts) """
    if objects:
        keys = []
        _objects = []
        for q in objects:
            value = q._data.get(ref)
            if value:
                keys.append(str(value))
            _objects.append(q)

        qs = doc.objects.filter(id__in=distinct(keys))
        queryset = queryset_to_dict(qs, ref)
        for o in _objects:
            setattr(o, ref, queryset.get(getattr(o, ref)))
        return _objects


def get_ref(doc, objects, ref):
    if objects:
        keys = []
        for q in objects:
            value = q._data.get(ref)
            k = value.__dict__.get("_DBRef__id")
            if k:
                keys.append(str(k))

        qs = doc.objects.filter(id__in=distinct(keys))
        return qs


def get_raw_ref(doc, objects, ref, order_by=None):
    if objects:
        keys = []
        for q in objects:
            value = getattr(q, ref)
            if value:
                keys.append(value)
        if keys:
            if order_by:
                qs = doc.objects.filter(id__in=distinct(keys)).order_by(order_by)
            else:
                qs = doc.objects.filter(id__in=distinct(keys))

            return qs