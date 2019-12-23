# -*- coding: UTF-8 -*-
import os,sys
import datetime
import time
from redis_client import RedisClient
import types
import logging
#加载配置
import setting
from setting import logger
try:
    from functools import wraps, update_wrapper
except ImportError:
    from django.utils.functional import wraps, update_wrapper  # Python 2.3, 2.4 fallback.

##########################Util Lib#############################
def queryset_to_dict(qs, key='pk'):
    """
	Given a queryset will transform it into a dictionary based on ``key``.
    param:
        qs:queryset
        key:string default is 'pk'
    return:
        dict
	"""
    return dict((getattr(u, key), u) for u in qs)

def distinct(l):
    """
	Given an iterable will return a list of all distinct values.
    param:
        l:an iterable
    return:
        the list
	"""
    return list(set(l))

def attach_OneToOne(objects, model, field):
    """
	Shortcut method which handles a pythonic LEFT OUTER JOIN.
	``attach_foreignkey(posts, Post.thread)``
    param:
        objects:object of list
        model: object
        field:string
	"""
    try:
        qs = model.objects.filter(pk__in=distinct(getattr(o, "pk") for o in objects))
        queryset = queryset_to_dict(qs)
        for o in objects:
            setattr(o, '_%s_cache' % (field), queryset.get(getattr(o, "pk")))
            #print getattr(o, '_%s_cache' % (field))
            #print o.userinfo
    except Exception,e:
        print e

def attach_foreignkey(objects, field, qs=None):
    """
	Shortcut method which handles a pythonic LEFT OUTER JOIN.
	``attach_foreignkey(posts, Post.thread)``
    param:
        objects:object of list
        field:string
        qs:query set  default is None
	"""
    try:
        t1 = time.time()
        field = field.field
        if qs is None:
            qs = field.rel.to.objects.all()
        qs = qs.filter(pk__in=distinct(getattr(o, field.column) for o in objects))
        #if select_related:
        #    qs = qs.select_related(*select_related)
        queryset = queryset_to_dict(qs)
        if queryset:
            for o in objects:
                setattr(o, '_%s_cache' % (field.name), queryset.get(getattr(o, field.column)))
        #print "attach_foreignkey use %s s " % (time.time() - t1)
    except Exception,e:
        print e

##########################Util Lib#############################


def find_include(ref_klass,pks,kwargs):
    """
    search the related object from current object
    param;
        ref_klass:related classs
        pks:primary key
        **kwargs:
            order_by_score: True or False
            include_select_related_model:True or False
            include:True or False
            select_related:True or False
    """
    if not pks:
        return []
    order_by_score = kwargs.get("order_by_score",False)
    include_select_related_model = kwargs.get("include_select_related_model")
    #默认是开启select_related()
    model = kwargs.get("include")
    if model:
        #1.fitler objects
        #print "model_name %s:" % model.__name__
        #print ref_klass.__name__,ref_klass.objects
        #mobjs = ref_klass.objects.filter(id__in=pks).order_by('-pk')
        n = datetime.datetime.now()
        if order_by_score:
            ids = ",".join(pks)
            if ref_klass.__name__.lower() != "user":
                sql = "SELECT * FROM %s where id in (%s) and status in(0,1) order by FIELD(id, %s)" % (ref_klass._meta.db_table,ids,ids)
            else:
                sql = "SELECT * FROM %s where id in (%s) order by FIELD(id, %s)" % (ref_klass._meta.db_table,ids,ids)
            mobjs = ref_klass.objects.raw(sql)
        else:
            mobjs = ref_klass.objects.filter(id__in=pks)
        logging.debug(" %s include use: %s" %  (ref_klass,datetime.datetime.now() - n))
        n = datetime.datetime.now()
        #2.fitler relate objects
        relate_ids = set()
        for obj in mobjs:
            v = getattr(obj,"%s_id" % model.__name__.lower())
            if v:
                relate_ids.add(v)
        #print "relate_ids %s:" % relate_ids
        #3.0 得到relate ID
        if relate_ids:
            robjs = model.objects.filter(id__in=tuple(relate_ids))
            #print "relate_ids len %s:" % len(robjs)
            rdic = {}
            for r in robjs:
                rdic[r.id] = r
            if include_select_related_model:
                #print "deal userinfo"
                attach_OneToOne(robjs,include_select_related_model,include_select_related_model.__name__.lower())
            
            #3.set relate objects
            for obj in mobjs:
                setattr(obj,model.__name__.lower(),rdic.get(getattr(obj,"%s_id" % model.__name__.lower())))
        logging.debug(" %s relate add use: %s" %  (ref_klass,datetime.datetime.now() - n))
        #4.返回关联对象
        return mobjs
    elif kwargs.get("select_related",False):
        return ref_klass.objects.select_related(depth=1).filter(id__in=pks)
    else:
        if order_by_score:
            ids = ",".join(pks)
            if ref_klass.__name__.lower() != "user":
                sql = "SELECT * FROM %s where id in (%s) and status in (0,1) order by FIELD(id, %s)" % (ref_klass._meta.db_table,ids,ids)
            else:
                sql = "SELECT * FROM %s where id in (%s) order by FIELD(id, %s)" % (ref_klass._meta.db_table,ids,ids)
            data = []
            for d in ref_klass.objects.raw(sql):
                data.append(d)
            return data
        else:
            data = ref_klass.objects.filter(id__in=pks)
            return data


class DAttribute(object):
    
    
    def __init__(self):
        """
        intialize base object reference object decsription
        """
        #Base Object
        self.bo = None
        self.ref = None
        self.descrpition = ""
        
    def change_log(self,oper,obj_id,baseobj,pipe=None,score=None):
        """
        save the relation of Reference
        list|sortset:insert:user_posts:user_id:post_id
        list|sortset:delete:user_posts:user_id:post_id
        param:
            oper: the operation  type is string
            obj_id: id of object  type is integer
            baseobj: base object
            pipe: redis pipe  default is None
            score: use rank
        """
        #是否启用数据同步
        if not setting.DATA_SYNC:
            return
        
        #初始化服务
        dp  = pipe or RedisClient.getInstance().redis
        #保存chang_log
        #String = 操作符： 主类型_引用类型s  : 主类型ID: 此类型ID
        basetype = str(baseobj.__class__.__name__).lower()
        ref = self.ref.lower()
        if  basetype == ref:
            ref = self.name.lower()
        if oper.startswith("sortset"):
            val = "%(oper)s:_:%(model_type)s_%(relate_type)ss:_:%(id)s:_:%(rid)s:_:%(score)s" % {"oper":oper,"model_type": basetype,"relate_type": ref,"id":baseobj.id,"rid" : obj_id ,"score":score}
        else:
            val = "%(oper)s:_:%(model_type)s_%(relate_type)ss:_:%(id)s:_:%(rid)s" % {"oper":oper,"model_type": basetype,"relate_type": ref,"id":baseobj.id,"rid" : obj_id}
        logger.info("sync: " + val)
        #保存数据dao Redis List Queue
        dp.lpush("change_log",val)
    
    
    @property
    def ref_klass(self):
        """
        Reference the object
        return:
            the object of self's Reference
        """
        from django.db import models
        if self.ref:
            _known_models = {}
            for klass in models.Model.__subclasses__():
                if hasattr(klass,"objects"):
                    _known_models[klass.__name__] = klass
                
                for sub in klass.__subclasses__():
                    if hasattr(sub,"objects"):
                        _known_models[sub.__name__] = sub
                        
                    for ssub in sub .__subclasses__():
                        if hasattr(ssub,"objects"):
                            _known_models[ssub.__name__] = ssub
            
            return _known_models.get(self.ref, None)

    """
    属性对象
    """
    def set(self,instance,val):
        """
        set the object's name value
        param:
            instance:the name  type is string
            val: the value type is string
        """
        setattr(instance,self.name,val)
    
    def __set__(self,instance,val):
        """
        set the object's name value
        param:
            instance:the name  type is string
            val: the value type is string
        """
        setattr(instance,"_"+self.name,val)
    
    def acceptable_types(self):
        """
        get the basestring it is python
        return:
            string
        """
        return basestring
        
    def validate(self,instance):
        """
        validate the effective of data
        param:
            instance:object
        """
        if self.required:
            if not self:
                instance._errors.append("%s require" % self)

########################################### Start Oper Decorater#######################################

def operKey(obj,field):
    """
    operate Key
    param:
        obj:object
        field:string
    return:
        string
    """
    return "%s:id:%s:%s" % (obj.__class__.__name__,obj.id, field)


def operSet(fn):
    """
    this Decoration method
    add operation
    """
    def _new(self, *args, **kws):
        try:
            baseobj = args[0]
            obj = args[1]
            #检查有效性
            if not obj:
                logger.error("please input dest object")
                raise StandardError("please input dest object")
            
            if hasattr(obj,"id") or hasattr(obj,"_id"):
                #key = "user:id:1:posts"
                key = operKey(baseobj,self.name) #"%s:id:%s:%s" % (baseobj.__class__.__name__,baseobj.id, self.name)
                kws["obj"] = obj
                kws["baseobj"] = baseobj
                fn(self,key,obj.id, **kws)
            else:
                logger.error("please object is new not have object.id")
                raise StandardError("please object is new not have object.id")
        except Exception,e:
            logger.error(e)
            return False
        return True
    #包装函数
    return wraps(fn)(_new)


def operGet(fn):
    """
    this is Decoration method
    get opearte  
    """
    def _new(self, *args, **kws):
        try:
            obj = args[0]
            #print obj.id
            if hasattr(obj,"id") or hasattr(obj,"_id"):
                #如果有ID只保存ID
                #key = "user:id:1:posts"
                key = operKey(obj,self.name)  #"%s:id:%s:%s" % (obj.__class__.__name__,obj.id, self.name)
                args = args[1:]
                kws["obj"] = obj
                return fn(self,key, *args, **kws)
            else:
                logger.error("please object is new not have object.id")
                raise StandardError("please object is new not have object.id")
        except Exception,e:
            logger.error(e)
            return None
    
    #包装函数
    return wraps(fn)(_new)

########################################### End Oper Decorater#######################################


class DListField(DAttribute):
    
    def __init__(self,ref=None,required=False,name = None):
        """
        initialize 
        param:
            ref:object  default is None
            required:True or false  default is False
            name:string
        """
        super(DAttribute,self).__init__()
        self.ref = ref
        self.index = False
        self.required = required
        self.name = name

    
    """   添加List 方法  """
    @operSet
    def lpush(self,key,value,**kwargs):
        """
        LPUSH key value Append an element to the head of the List value at key
        param;
            key:string
            value:string
            **kwargs: a dict
                obj:object
                baseobj:base object
        return:
            True or False
        """
        #print "listfield lpush ",key,",",value
        try:
            if setting.Debug:
                n = datetime.datetime.now()
            pipe = RedisClient.getInstance().redis.pipeline()
            pipe.lpush(key,value)
            self.change_log("list:insert",kwargs["obj"].id,kwargs["baseobj"],pipe)
            pipe.execute()
            if setting.Debug:
                logger.info(" lpush key: %s,use : %s" % (key,datetime.datetime.now() - n))
            return True
        except Exception,e:
            pipe.reset()
            logger.error(e)
            return False


    @operSet
    def rpush(self,key,value,**kwargs):
        """
        push the data into list of redis at right of list
        param;
            key:string
            value:string
            **kwargs: a dict
                obj:object
                baseobj:base object
        return:
            True or False
        """
        #Save
        #print "listfield rpush ",key,",",value
        try:
            pipe = RedisClient.getInstance().redis.pipeline()
            pipe.rpush(key,value)
            self.change_log("list:insert",kwargs["obj"].id,kwargs["baseobj"],pipe)
            pipe.execute()
            return True
        except Exception,e:
            pipe.reset()
            logger.error(e)
            return False

    @operGet
    def lpop(self,key,**kwargs):
        """
        LPOP key Return and remove (atomically) the first element of the List at key
        param;
            key:string
            **kwargs: a dict
                obj:object
        return:
            object
        """
        # LPOP key Return and remove (atomically) the first element of the List at key
        #print "lpop key",key
        pk =  RedisClient.getInstance().redis.lpop(key)
        self.change_log("list:delete",pk,kwargs["obj"])
        objs = self.ref_klass.objects.filter(id=pk)
        if objs:
            return objs[0]
        return None

    @operGet
    def rpop(self,key,**kwargs):
        """
        RPOP key Return and remove (atomically) the first element of the List at key
        param;
            key:string
            **kwargs: a dict
                obj:object
        return:
            object
        """
        #print "rpop key",key
        pk = RedisClient.getInstance().redis.rpop(key)
        self.change_log("list:delete",pk,kwargs["obj"])
        objs = self.ref_klass.objects.filter(id=pk)
        if objs:
            return objs[0]
        return None
    
    @operGet
    def llen(self,key,**kwargs):
        """
        LLEN key Return the length of the List value at key
        param;
            key:string
            **kwargs: a dict
        return:
            integer of length
        """
        #print "len key",key
        return RedisClient.getInstance().redis.llen(key)
    
    @operGet
    def lrange(self,key,start=0,end=10,**kwargs):
        """
        LRANGE key start end Return a range of elements from the List at key
        param:
            key:string
            start:integer default is 0
            end:integer  default is 10
            **kwargs:dict
        return:
            the data in list
        """
        if setting.Debug:
            n = datetime.datetime.now()
        pks = RedisClient.getInstance().redis.lrange(key,start,end)
        if setting.Debug:
            logger.info("lrange key: %s,start: %s, end: %s ,use : %s" % (key,start,end,datetime.datetime.now() - n))
        
        #返回相关对象集合
        return  find_include(self.ref_klass,pks,kwargs)
        #return self.ref_klass.objects.filter(pk__in = pks)

##    @operGet
##    def ltrim(self,key,start=0,end=10):
##         这个不支持同步
##        # LTRIM key start end Trim the list at key to the specified range of elements
##        return RedisClient.getInstance().redis.ltrim(key,start,end)

    @operSet
    def lrem(self,key,id,count=1,**kwargs):
        """
        LREM key count value Remove the first-N, last-N, or all the elements matching value from the List at key
        param:
            key:string
            count:integer default is 1
            id:integer
            **kwargs:dict
                baseobj:base object
        return:
            True or False
        """
        #print "rem key",key
        #print "rem value",id
        try:
            pipe = RedisClient.getInstance().redis.pipeline()
            pipe.lrem(key,id,count)
            self.change_log("list:delete",id,kwargs["baseobj"])
            pipe.execute()
            return True
        except Exception,e:
            pipe.reset()
            logger.error(e)
            return False
    
    @operGet
    def delete(self,key,pipe,**kwargs):
        """
        delete the list use index
        param:
            key: string
            pipe: redis pipe
        return:
            True or false
        """
        db = pipe | RedisClient.getInstance().redis
        return db.delete(key)
    
    
class DSetField(DAttribute):
    #常量定义
    redis = RedisClient.getInstance().redis
    
    def __init__(self,ref=None,required=False,name=None):
        """
        initialize reference object name index and required
        param:
            ref:reference object
            required:True or False
            name:string
        """
        super(DAttribute,self).__init__()
        self.ref = ref
        self.name = name
        self.index = False
        self.required = required
        
    @operSet
    def sadd(self,key,member,**kwargs):
        """
        SADD key member Add the specified member to the Set value at key
        param:
            key:string
            member:string
            **kwargs:include obj and baseobj
                obj:the object
                baseobj: base object
        return:
            True or False
        """
        try:
            if setting.Debug:
                n = datetime.datetime.now()
            pipe = DSetField.redis.pipeline()
            pipe.sadd(key,member)
            self.change_log("set:insert",kwargs["obj"].id,kwargs["baseobj"],pipe)
            pipe.execute()
            return True
        except Exception,e:
            pipe.reset()
            logger.error(e)
            return False
        #RedisClient.getInstance().redis.sadd(key,member)
    
    
    @operGet
    def spop(self,key,**kwargs):
        """
        SPOP key Remove and return (pop) a random element from the Set value at key
        param:
            key:string
            **kwargs:include obj 
                obj:the object
        return:
            object
        """
        # SPOP key Remove and return (pop) a random element from the Set value at key
        pk = DSetField.redis.spop(key)
        self.change_log("set:delete",pk,kwargs["obj"])
        
        #print '#'*10
        #print pk
        #print self.ref_klass
        #print '#'*10
        objs = self.ref_klass.objects.filter(pk=pk)
        if objs:
            return objs[0]
        return None

    
    
    @operSet
    def srem(self,key,member,**kwargs):
        """
        SREM key member Remove the specified member from the Set value at key
        param:
            key:string
            member:string
            **kwargs:include baseobj
                baseobj: base object
        return:
            True or False
        """
        #SREM key member Remove the specified member from the Set value at key
        try:
            pipe = DSetField.redis.pipeline()
            pipe.srem(key,member)
            self.change_log("list:delete",member,kwargs["baseobj"])
            pipe.execute()
            return True
        except Exception,e:
            pipe.reset()
            logger.error(e)
            return False
        #RedisClient.getInstance().redis.srem(key,member)

    @operGet
    def scard(self,key,**kwargs):
        """
        SCARD key Return the number of elements (the cardinality) of the Set at key
        param:
            key:string
            **kwargs:dict
        return: 
            count of set by key
        """
        return DSetField.redis.scard(key)
    
    @operGet
    def sismember(self,key,member_id,**kwargs):
        # SISMEMBER key member Test if the specified value is a member of the Set at key
        return DSetField.redis.sismember(key,member_id)
    
    @operGet
    def smembers(self,key,**kwargs):
        """
        SMEMBERS key Return all the members of the Set value at key 
        param:
            key:string
            **kwargs:dict
        return:
            objects of list
        """
        # SMEMBERS key Return all the members of the Set value at key 
        if setting.Debug:
            n = datetime.datetime.now()
        pks = DSetField.redis.smembers(key)
        if kwargs.get("only_ids",False):
            return pks
        return self.ref_klass.objects.filter(pk__in = pks)

    
    @operGet
    def delete(self,key,pipe,**kwargs):
        """
        delete the value of key
        param;
            key:string
            pipe:redis
            **kwargs:dict
        return:
            True or False
        """
        db = pipe | DSetField.redis
        return db.delete(key)



class DSortSetField(DAttribute):
    
    #常量定义
    redis = RedisClient.getInstance().redis
    
    def __init__(self,ref=None,required=False,index = False,name=None,limit=500):
        """
        initialize name index reference object limit
        param:
            ref:reference object
            required:True or False
            index:True or False
            name:string  default is None
            limit:integer  default is 1000
        """
        super(DAttribute,self).__init__()
        self.name = name
        self.index = index
        self.ref = ref
        self.required = required
        #限制最大幅度，设置为0为不限制
        self.limit = limit
        
    @operSet
    def  zadd(self,key ,member ,score,**kwargs):
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
            if setting.Debug:
                n = datetime.datetime.now()
            pipe = DSortSetField.redis.pipeline()
            pipe.zadd(key ,member ,score)
            self.change_log("sortset:insert",kwargs["obj"].id,kwargs["baseobj"],pipe,score)
            pipe.execute()
                
            #Start 删除超过LIMIT的
            if self.limit > 0:
                zcard = DSortSetField.redis.zcard(key)
                #print "zcard",zcard
                if zcard > self.limit:
                    #print "* " * 20
                    #print "Start 删除超过LIMIT的"
                    #print "rem %s " % key
                    delete_to = zcard - self.limit
                    DSortSetField.redis.zremrangebyrank(key,0,delete_to)
            #End
            
            return True
        except Exception,e:
            pipe.reset()
            logger.error(e)
            return False
        #return RedisClient.getInstance().redis.zadd(key ,member ,score)
    
    
    @operGet
    def  zrank(self, key ,member_id,**kwargs):
        """
        get the the index of member in sorted set
        in front is the lowest score
        param:
            key:string
            member_id:integer
            **kwargs:dict
        return:
            integer
        """
        return DSortSetField.redis.zrank( key , member_id)
    
    @operGet
    def  zrevrank( self,key , member_id,**kwargs):
        """
        get the the index of member in sorted set
        in front is the highest score
        param:
            key:string
            member_id:integer
            **kwargs:dict
        return:
            integer
        """
        return DSortSetField.redis.zrevrank( key ,member_id)
    
    
    @operGet
    def  zrange(self, key , start=0, end=10,**kwargs):
        """
        get the the member in sorted set  between start and end
        in front is the lowest score
        param:
            key:string
            start:integer
            end:integer
            **kwargs:dict
        return:
            members of list
        """
        pks = DSortSetField.redis.zrange( key ,start, end) or []
        if kwargs.get("only_ids",False):
            return pks
        else:
            return  find_include(self.ref_klass,pks,kwargs)
       

    
    @operGet
    def  zrevrange(self, key ,start=0, end=10,**kwargs):
        """
        get the the index of member in sorted set
        in front is the lowest score  highest in the back
        param:
            key:string
            member_id:integer
            **kwargs:dict
        return:
            integer
        """
        if setting.Debug:
            n = datetime.datetime.now()
            
        withscores = kwargs.get("withscores",False)
        #t = time.time()
        data = DSortSetField.redis.zrevrange( key ,start, end,withscores = withscores) or []
        #print "zrevrange use:" ,time.time() - t
        #读取的时候带 score
        if withscores:
            pks = []
            scores = {}
            for d in data:
                pks.append(d[0])
                scores[d[0]] = d[1]
        else:
            pks = data
        #print "withscores use:" ,time.time() - t
        if kwargs.get("only_ids",False):
            return pks
        else:
            mobjs = find_include(self.ref_klass,tuple(pks),kwargs)
            #print "find_include use:" ,time.time() - t
            #这里将得分设置为对象的属性
            if withscores and mobjs:
                m_raws = []
                for obj in mobjs:
                    setattr(obj,"rd_score",scores[str(obj.pk)])
                    m_raws.append(obj)
                mobjs = m_raws
            return mobjs
    
    @operGet
    def  zrangebyscore(self, key ,min, max,**kwargs):
        """
        get the the member in sorted set  between min and max
        param:
            key:string
            min:integer
            max:integer
            **kwargs:dict
        return:
            members of list
        """
        pks = DSortSetField.redis.zrangebyscore( key ,min, max) or []
        return self.ref_klass.objects.filter(pk__in = pks)
    
    @operGet
    def  zscore(self, key ,member,**kwargs):
        """
        get the score of member
        param:
            key:string
            member_id:integer
            **kwargs:dict
        return:
            score
        """
        return DSortSetField.redis.zscore( key ,member.id)
    
    
    @operGet
    def  zcard(self, key,**kwargs ):
        """
        get the base integer of sorted set
        param:
            key:string
            **kwarg:dict
        return:
            count of list
        """
        return DSortSetField.redis.zcard( key )
    
    
    @operSet
    def  zrem(self, key,member_id,**kwargs):
        """
        delete the member in sorted set
        param:
            key:string
            member_id:integer
            **kwargs:dict
        return:
            True or False
        """
        try:
            DSortSetField.redis.zrem( key,member_id)
            return True
        except Exception,e:
            logger.error(e)
            return False
    
    
    @operGet
    def zremrangebyrank(self,key,min_rank=0,max_rank=1,**kwargs):
        """
        maintain the size of list
        pop one object every time
        param:
            key:string
            min_rank:integer  default is 0
            max_rank:integer default is 1
            **kwargs:dict
        retrun:
            True or False
        """
        try:
            DSortSetField.redis.zremrangebyrank(key,min_rank,max_rank)
            return True
        except Exception,e:
            logger.error(e)
            return False

