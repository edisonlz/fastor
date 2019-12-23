# -*- coding: UTF-8 -*-
import os, sys
import datetime
import time
from redis_model.redis_client import RedisClient
from redis_model.models.mongo_utils import *

class MAttribute(object):
    redis = RedisClient.getInstance().redis

    def __init__(self):
        """ intialize base object reference object description """
        self.bo = None
        self.ref = None
        self.descrpition = ""

    @property
    def ref_klass(self):
        """
          Reference the object
          return:
              the object of self's Reference
        """
        from mongoengine.document import Document, EmbeddedDocument

        if self.ref:
            _known_models = {}
            for klass in Document.__subclasses__():
                if hasattr(klass, "objects"):
                    _known_models[klass.__name__] = klass

                for sub in klass.__subclasses__():
                    if hasattr(sub, "objects"):
                        _known_models[sub.__name__] = sub

                    for _sub in sub.__subclasses__():
                        if hasattr(_sub, "objects"):
                            _known_models[_sub.__name__] = _sub

            return _known_models.get(self.ref, None)


    def set(self, instance, val):
        """
          set the object's name value
          param:
              instance:the name  type is string
              val: the value type is string
          """
        setattr(instance, self.name, val)

    def __set__(self, instance, val):
        """
          set the object's name value
          param:
              instance:the name  type is string
              val: the value type is string
          """
        setattr(instance, "_" + self.name, val)

    def acceptable_types(self):
        """
          get the basestring it is python
          return:
              string
          """
        return basestring

    def validate(self, instance):
        """
          validate the effective of data
          param:
              instance:object
          """
        if self.required:
            if not self:
                instance._errors.append("%s require" % self)

    @operGet
    def delete(self, key, **kwargs ):
        """ drop redis all tyep of data """
        pipe = self.redis.pipeline()
        pipe.delete(key)
        pipe.delete(self.get_field_key(key))
        pipe.execute()
        print "delete key", key, self.get_field_key(key)

    #pipe.delete(self.get_member_key(key, "save_high_score"))
    #print "delete key" , key  ,self.get_field_key(key)


    def get_field_key(self, key):
        return "%s_field" % key

    def get_member_key(self, member, field):
        return "%s_%s" % (member, field)


class MSortSetField(MAttribute):
    def __init__(self, ref=None, required=False, name=None, limit=0):
        """
          initialize name index reference object limit
          param:
              ref:reference object
              required:True or False
              name:string  default is None
              limit:integer  default is 20000 ,0 is no limit
          """
        super(MAttribute, self).__init__()
        self.name = name
        self.ref = ref
        self.required = required
        self.limit = limit
        self.delete_factor = 1.5

    @operSet
    def zadd(self, key, member, score, **kwargs):
        """
          add the member into the sorted set by score
          if the member is exist  then update it's score
          param:
              key:string
              member:string
              score:rank integer
              **kwargs:include obj and baseobj
                  obj:object
                  baseobj:base object
          return:
              True or False
          """
        try:
            save_high_score = kwargs.get("save_high_score", False)
            if save_high_score:
                sort_order = kwargs.get("sort_order", True)
                hkey = self.get_field_key(key)
                hmember = self.get_member_key(member, "save_high_score")

                if sort_order:
                    last_score = self.redis.hget(hkey, hmember) or 0
                else:
                    last_score = self.redis.hget(hkey, hmember) or sys.maxint

                last_score = int(last_score)
                if (sort_order and (score > last_score)) or (not sort_order and (score < last_score)):
                    self.redis.hset(hkey, hmember, score)
                else:
                    return False

            pipe = self.redis.pipeline()
            pipe.zadd(key, member, score)
            pipe.execute()

            if self.limit > 0:
                zcard = self.redis.zcard(key)
                if zcard > self.limit * self.delete_factor:
                    delete_to = zcard - self.limit
                    self.redis.zremrangebyrank(key, 0, delete_to)
            return True
        except Exception, e:
            print e
            pipe.reset()
            return False

    @operGet
    def zrank(self, key, member_id, **kwargs):
        """
          get the the index of member in sorted set
          in front is the lowest score
          return:
              integer
          """
        r = self.redis.zrank(key, member_id)
        if r != None:
            r += 1
        return r

    @operGet
    def  zrevrank( self, key, member_id, **kwargs):
        """
          get the the index of member in sorted set
          in front is the highest score
          return:
              integer
          """
        r = self.redis.zrevrank(key, member_id)
        if r != None:
            r = r + 1
        return r

    @operGet
    def zrange(self, key, start=0, end=10, withscores=False, **kwargs):
        """
          get the the member in sorted set  between start and end
          in front is the lowest score
          return:
              members of list
          """
        data = self.redis.zrange(key, start, end, withscores=withscores) or []

        if withscores:
            pks = []
            scores = {}
            for d in data:
                if d[0].find("_") > 0:
                    key = str(d[0]).split("_")[0]
                else:
                    key = d[0]
                pks.append(key)
                scores[key] = d[1]
        else:
            pks = data
            scores = {}

        if kwargs.get("only_ids", False):
            return pks
        else:
            return find_include(self.ref_klass, tuple(pks), scores, withscores)

    @operGet
    def zrevrange(self, key, start=0, end=10, **kwargs):
        """
          get the the index of member in sorted set
          in front is the lowest score  highest in the back
          return:
              members of list
          """
        withscores = kwargs.get("withscores", True)
        data = self.redis.zrevrange(key, start, end, withscores=withscores) or []

        scores = {}
        if withscores:
            pks = []
            for d in data:
                if d[0].find("_") > 0:
                    key = str(d[0]).split("_")[0]
                else:
                    key = d[0]
                pks.append(key)
                scores[key] = d[1]
        else:
            pks = data

        if kwargs.get("only_ids", False):
            return pks
        else:
            return find_include(self.ref_klass, tuple(pks), scores, withscores)

    @operGet
    def zscore(self, key, member, **kwargs):
        """
          get the score of member
          return:
              score
          """
        return self.redis.zscore(key, member.id)


    @operGet
    def zcard(self, key, **kwargs ):
        """
          get the base integer of sorted set
          return:
              count of list
          """
        return self.redis.zcard(key)


    @operSet
    def zrem(self, key, member_id, **kwargs):
        """
          delete the member in sorted set
          return:
              True or False
          """
        try:
            self.redis.zrem(key, member_id)
            return True
        except Exception, e:
            return False


    @operGet
    def zremrangebyrank(self, key, min_rank=0, max_rank=1, **kwargs):
        """
          maintain the size of list
          pop one object every time
          retrun:
              True or False
        """
        try:
            self.redis.zremrangebyrank(key, min_rank, max_rank)
            return True
        except Exception, e:
            return False


class MHashField(MAttribute):
    def __init__(self, ref=None, required=False, name=None):
        """
          initialize name index reference object limit
          param:
              ref:reference object
              required:True or False
              name:string  default is None
              limit:integer  default is 20000 ,0 is no limit
          """
        super(MAttribute, self).__init__()
        self.name = name
        self.ref = ref
        self.required = required


    @operSet
    def hset(self, key, field, **kwargs):
        """
        use User.hset(self, user1, 1)
        """
        self.redis.hset(key, field, kwargs["value"])
        return True


    @operGet
    def hget(self, key, field, **kwargs):
        """
        use User.hget(self, user1)
        """
        return self.redis.hget(key, str(getattr(field, "id")))


