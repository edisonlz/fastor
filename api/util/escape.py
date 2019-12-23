#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import simplejson as __json
except ImportError:
    import json as __json


def to_str(value):
    """unicode->str"""
    if isinstance(value, (str, type(None))):
        return value
    assert isinstance(value, unicode)
    return value.encode("utf-8")


def to_unicode(value):
    """str->unicode"""
    if isinstance(value, (unicode, type(None))):
        return value
    assert isinstance(value, str)
    return value.decode("utf-8")


def load_json(value):
    """json->obj"""
    return __json.loads(value)


def dump_json(value):
    """obj->json"""
    return __json.dumps(value, separators=(',', ':'))

