#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.dom.minidom import Document, getDOMImplementation
import re
import escape


def json(obj):
    """ Represent instance of a class as JSON. """

    def serialize(obj):
        """ Recursively walk object's hierarchy. """
        if isinstance(obj, (bool, int, long, float, basestring)):
            return obj
        elif isinstance(obj, dict):
            obj = obj.copy()
            for key in obj:
                value = obj[key]
                obj[key] = '' if value is None else serialize(value)
            return obj
        elif isinstance(obj, list):
            return [serialize(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(serialize([item for item in obj]))
        elif hasattr(obj, '__dict__'):
            return serialize(obj.__dict__)
        else:
            return repr(obj) # Don't know how to handle, convert to string

    return escape.dump_json(serialize(obj))

def xml(obj):
    """ Represent instance of a class as XML """

    doc = Document()
    root = doc.createElement('document')
    doc.appendChild(root)

    def serialize(node, obj):
        """ Recursively walk object's hierarchy. """
        if isinstance(obj, (bool, int, long, float, basestring)):
            text = obj
            try:
                text = unicode(text).encode('utf-8')
            except UnicodeDecodeError:
                pass
            node.appendChild(doc.createTextNode(text))
        elif isinstance(obj, dict):
            obj = obj.copy()
            for key in obj:
                kk = key
                if re.search(r"^\d+$", kk):
                    #u xml name must 字母开头
                    kk = "key_{}".format(kk)
                k = doc.createElement(unicode(kk).encode('utf-8'))
                node.appendChild(k)
                serialize(k, obj[key])
        elif isinstance(obj, (list, tuple)):
            for item in obj:
                k = doc.createElement('item')
                node.appendChild(k)
                serialize(k, item)
        elif hasattr(obj, '__dict__'):
            serialize(node, obj.__dict__)
        else:
            node.appendChild(doc.createTextNode(repr(obj).encode('utf-8')))

    serialize(root, obj)
    #print doc.toxml()
    return doc.toxml()

def plist(obj):
    impl = getDOMImplementation()
    dt = impl.createDocumentType('plist', '-//Apple//DTD PLIST 1.0//EN', 'http://www.apple.com/DTDs/PropertyList-1.0.dtd')
    doc = impl.createDocument(None, 'plist', dt)
    #root = doc.createElement('plist')
    root = doc.documentElement
    root.setAttribute('version', '1.0')
    doc.appendChild(root)

    def serialize(node, obj):
        if isinstance(obj, (bool, int, long, float, basestring)):
            text = obj
            try:
                text = unicode(text).encode('utf-8')
            except UnicodeDecodeError:
                pass
            _item = doc.createElement('string')
            _item_value = doc.createTextNode(text)
            _item.appendChild(_item_value)
            node.appendChild(_item)
        elif isinstance(obj, dict):
            _p_item = doc.createElement('dict')
            for k, v in obj.items():
                _item = doc.createElement('key')
                _item_value = doc.createTextNode(unicode(k).encode('utf-8'))
                _item.appendChild(_item_value)
                _p_item.appendChild(_item)
                serialize(_p_item, v)
            node.appendChild(_p_item)
        elif isinstance(obj, (list, tuple)):
            k = doc.createElement('array')
            for item in obj:
                serialize(k, item)
            node.appendChild(k)
        elif hasattr(obj, '__dict__'):
            serialize(node, obj.__dict__)
        else:
            node.appendChild(doc.createTextNode(repr(obj).encode('utf-8')))

    serialize(root, obj)
    return doc.toxml('UTF-8')

