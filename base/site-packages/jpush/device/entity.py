#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys

if 2 != sys.version_info[0]:
    unicode = str

def add(*types):
    """Select a (list of) to be added objects(s)

    >>> add("registrationid1", "registrationid2")
    {'add': ['registrationid1', 'registrationid2']}
    >>> add("tag1", "tag2")                         
    {'add': ['tag1', 'tag2']}
    >>> add("alias1", "alias2")   
    {'add': ['alias1', 'alias2']}
    """
    vadd = [v for v in types]
    return {"add": vadd}

def remove(*types):
    """Select a (list of) to be removed objects(s)

    >>> remove("registrationid1", "registrationid2")   
    {'remove': ['registrationid1', 'registrationid2']}
    >>> remove("tag1", "tag2")                              
    {'remove': ['tag1', 'tag2']}
    >>> remove("alias1", "alias2")                        
    {'remove': ['alias1', 'alias2']}
    """
    vremove = [v for v in types]
    return {"remove": vremove}

def device_tag(*types):
    """Get a tag object

    >>> device_tag("")
    {'tags': ''}
    >>> device_tag("tag1")
    {'tags': 'tag1'}
    >>> device_tag(add("tag1", "tag2"), remove("tag3", "tag4"))
    {'tags': {'add': ['tag1', 'tag2'], 'remove': ['tag3', 'tag4']}}
    """
    tag = {}
    if 1 == len(types) and isinstance(types[0], (str, unicode)):
        tag["tags"] = types[0]
        return tag
    tag["tags"] = {}
    for t in types:
        for key in t:
            if key not in ('add', 'remove'):
                raise ValueError("Invalid tag '%s'" % t)
            tag["tags"][key] = t[key]
    return tag


def device_mobile(device_mobile):
    mobile={}
    mobile["mobile"]=device_mobile
    return mobile


def device_alias(*types):
    """Get an alias object

    >>> device_alias("")
    {'alias': ''}
    >>> device_alias("alias1")
    {'alias': 'alias1'}
    >>> device_alias(add("alias1", "alias2"), remove("alias3", "alias4"))
    {'alias': {'add': ['alias1', 'alias2'], 'remove': ['alias3', 'alias4']}}
    """
    alias = {}
    if 1 == len(types) and isinstance(types[0], (str, unicode)):
        alias["alias"] = types[0]
        return alias 
    alias["alias"] = {}
    for t in types:
        for key in t:
            if key not in ('add', 'remove'):
                raise ValueError("Invalid alias '%s'" % t)
            alias["alias"][key] = t[key]
    return alias


def device_regid(*types):
    """Get a registration_id object

    >>> device_regid("")
    {'registration_ids': ''}
    >>> device_regid("registration_id1")
    {'registration_ids': 'registration_id1'}
    >>> device_regid(add("registration_id1", "registration_id2"), remove("registration_id3", "registration_id4"))
    {'registration_ids': {'add': ['registration_id1', 'registration_id2'], 'remove': ['registration_id3', 'registration_id4']}}
    """
    registration_id = {}
    if 1 == len(types) and isinstance(types[0], (str, unicode)):
        registration_id["registration_ids"] = types[0]
        return registration_id
    registration_id["registration_ids"] = {}
    for t in types:
        for key in t:
            if key not in ('add', 'remove'):
                raise ValueError("Invalid registration_id '%s'" % t)
            registration_id["registration_ids"][key] = t[key]
    return registration_id

if "__main__" == __name__:
    print (add("1", "2"))
    print (device_tag(add("a", "b"), remove('1', '2')))
