#encoding=utf-8

#import settings
import time
import logging
import memcache
import random

try:
    import cjson as json
except Exception, e:
    logging.error(e)
    import json

    json.encode = json.dumps
    json.decode = json.loads

class McJsonPickleWrapper(object):
    def __init__(self, file, protocol=None):
        self.file = file
        self.protocol = protocol

    def dump(self, value):
        data = json.encode(value)
        self.file.write(data)

    def load(self):
        data = self.file.read()
        return json.decode(data)


class MemcacheProxy(object):
    """Memcache Proxy"""

    def __init__(self, servers):
        #searilaize
        pickler = McJsonPickleWrapper
        unpickler = McJsonPickleWrapper

        self._servers = []
        self._down_servers = []

        for server in servers:
            mc = memcache.Client([server, ], pickler=pickler, unpickler=unpickler)
            self._servers.append(mc)


    @property
    def mc(self):
        return random.choice(self._servers)


    def mc_backup(self, down_server):
        servers = []

        try:
            if down_server not in self._down_servers:
                self._down_servers.append(down_server)

            for s in self._servers:
                if s not in self._down_servers:
                    servers.append(s)
        except Exception, e:
            logging.error(e)
            servers = self._servers
            pass

        return random.choice(servers)


    def add(self, *args, **kwargs):
        mc = None
        try:
            mc = self.mc
            return mc.add(*args, **kwargs)
        except Exception, e:
            logging.error(e)
            return self.mc_backup(mc).add(*args, **kwargs)


    def get(self, *args, **kwargs):
        mc = None
        try:
            mc = self.mc
            return mc.get(*args, **kwargs)
        except Exception, e:
            logging.error(e)
            try:
                return self.mc_backup(mc).get(*args, **kwargs)
            except Exception, e:
                logging.error(e)
                return None


    def get_multi(self, *args, **kwargs): # real signature unknown
        """ Get multiple keys at once. """
        mc = None
        try:
            mc = self.mc
            return mc.get_multi(*args, **kwargs)
        except Exception, e:
            logging.error(e)
            try:
                return self.mc_backup(mc).get_multi(*args, **kwargs)
            except Exception, e:
                logging.error(e)
                return None



    def set(self, *args, **kwargs):
        mc = None
        try:
            mc = self.mc
            return mc.set(*args, **kwargs)
        except Exception, e:
            logging.error(e)
            return self.mc_backup(mc).set(*args, **kwargs)


    def set_multi(self, *args, **kwargs): # real signature unknown
        """ Set multiple keys at once. """
        mc = None
        try:
            mc = self.mc
            return mc.set_multi(*args, **kwargs)
        except Exception, e:
            logging.error(e)
            return self.mc_backup(mc).set_multi(*args, **kwargs)


    def delete(self, *args, **kwargs):
        mc = None
        try:
            mc = self.mc
            return mc.delete(*args, **kwargs)
        except Exception, e:
            logging.error(e)
            return self.mc_backup(mc).delete(*args, **kwargs)


    def delete_multi(self, *args, **kwargs): # real signature unknown
        """ Delete multiple keys at once. """
        mc = None
        try:
            mc = self.mc
            return mc.delete_multi(*args, **kwargs)
        except Exception, e:
            logging.error(e)
            return self.mc_backup(mc).delete_multi(*args, **kwargs)


    def incr(self, *args, **kwargs): # real signature unknown
        """ incr  keys at once. """
        mc = None
        try:
            mc = self.mc
            return mc.incr(*args, **kwargs)
        except Exception, e:
            logging.error(e)
            return self.mc_backup(mc).incr(*args, **kwargs)


    def decr(self, *args, **kwargs): # real signature unknown
        """ decr  keys at once. """
        mc = None
        try:
            mc = self.mc
            return mc.decr(*args, **kwargs)
        except Exception, e:
            logging.error(e)
            return self.mc_backup(mc).decr(*args, **kwargs)


    def append(self, *args, **kwargs): # real signature unknown
        """ append  keys at once. """
        mc = None
        try:
            mc = self.mc
            return mc.append(*args, **kwargs)
        except Exception, e:
            logging.error(e)
            return self.mc_backup(mc).append(*args, **kwargs)

    def prepend(self, *args, **kwargs): # real signature unknown
        """ replace  keys at once. """
        mc = None
        try:
            mc = self.mc
            return mc.prepend(*args, **kwargs)
        except Exception, e:
            logging.error(e)
            return self.mc_backup(mc).prepend(*args, **kwargs)


    def replace(self, *args, **kwargs): # real signature unknown
        """ replace  keys at once. """
        mc = None
        try:
            mc = self.mc
            return mc.replace(*args, **kwargs)
        except Exception, e:
            logging.error(e)
            return self.mc_backup(mc).replace(*args, **kwargs)


    def cas(self, *args, **kwargs): # real signature unknown
        """ cas. """
        mc = None
        try:
            mc = self.mc
            return mc.cas(*args, **kwargs)
        except Exception, e:
            logging.error(e)
            return self.mc_backup(mc).cas(*args, **kwargs)

        