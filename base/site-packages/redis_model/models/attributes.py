# -*- coding: UTF-8 -*-

import os,sys
import datetime
import time
from redis_client import RedisClient
import types
import setting
from setting import logger

try:
    from functools import wraps, update_wrapper
except ImportError:
    from django.utils.functional import wraps, update_wrapper  # Python 2.3, 2.4 fallback.


#默认加载所有Field
__all__ = ["Attribute",'StringField','IntegerField','FloatField','DateTimeField', 'ListField', 'SetField','SortSetField']

class Attribute(object):
    
    
    def __init__(self):
        """
        initialize the bo is None ref is None description is ''
        """
        #Base Object
        self.bo = None
        self.ref = None
        self.descrpition = ""
        
##    def __deepcopy__(self, memo):
##        """
##        Deep copy of a QuerySet doesn't populate the cache
##        """
##        #print "in coopy"
##        obj_dict = copy.deepcopy(self.__dict__, memo)
##        obj = self.__class__()
##        obj.__dict__.update(obj_dict)
##        return obj
        
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
        if self.ref:
            from base import get_model_from_key
            return get_model_from_key(self.ref)


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
        val = self.typecast_for_read(val)
        setattr(instance,"_"+self.name,val)
    
    def typecast_for_read(self, value):
        """
        this method is not any operate
        get the value
        param:
            value:string
        return:
            value:string
        """
        return value
    
    def acceptable_types(self):
        """
        get the basestring  it is django
        return:
            basestring:string
        """
        return basestring
        
    def validate(self,instance):
        """
        validate the Effectiveness of date
        param:
            instance:object
        """
        if self.required:
            if not self:
                instance._errors.append("%s require" % self)


class StringField(Attribute):
    
    def __init__(self,index=False,required=False,name=None):
        """
        initialize the name,index and required
        param:
            index: True or False
            required: True or False
            name: object default is None
        """
        super(Attribute,self).__init__()
        self.name = name
        self.index = index
        self.required = required
    
    def typecast_for_read(self, value):
        """
        get the value
        param:
            value:string
        return:
            value:string
        """
        return value
    
    def typecast_for_storage(self, value):
        """
        get the value
        param:
            value:string
        return:
            value:string
        """
        return value
    
    
    def validate(self,instance):
        """
        validate the Effectiveness of data
        param:
            instance:object
        return:
            True or False
        """
        #判断添加索引，这里要确保一致性 
        if self.index:
            value = getattr(instance, self.name)
            index_name = instance.__class__.index_name(self.name)
            #2种情况，1为新用户注册，2为用户保存
            if instance.is_new():
                if instance.db.hexists(index_name,value):
                    instance._errors.append("field %s = %s exists" % (self.name,value))
                    return False
            else:
                if instance.db.hexists(index_name,value):
                    pid =instance.db.hget(index_name,value)
                    if str(instance.id) != str(pid):
                        instance._errors.append("field %s = %s exists" % (self.name,value))
                        return False
    
        #判断是否为必填字段
        if self.required:
            if not self:
                instance._errors.append("%s require" % self)

        return  True
    
    def __get__(self,instance,owner):
        """
        load lazy
        """
        #设计为lazy load
        try:
            return getattr(instance,'_'+self.name)
        except:
            
            if not instance.is_new():
                val = instance.db.hget(instance.dump_key(),self.name)
                if val is not None:
                    #转化为读出格式
                    val = self.typecast_for_read(val)
                self.__set__(instance, val)
                return val
            else:
                self.__set__(instance, None)
                return None


class IntegerField(StringField):
    
    def __init__(self,index = False,required = False,name = None):
        """
        initialize  call the StringField class __init__ method
        param:
            index:True or False
            required:True or False
            name:string  default is None
        """
        StringField.__init__(self,index,required,name)
        #self.name = name
        #self.index = index
        #self.required = required
        pass
    
    def typecast_for_read(self, value):
        """
        get the value
        param:
            value:number
        return:
            value:integer
        """
        return int(value)
    
    def typecast_for_storage(self, value):
        """
        get the value
        param:
            value:number
        return:
            value:integer
        """
        return int(value)
    
    def acceptable_types(self):
        """
        get the Integer type
        return:
            integer 
        """
        return int
        
    
    
class FloatField(StringField):
    
    def __init__(self,index = False,required = False,name = None):
        """
        initialize 
        param:
            index:True or False
            required:True or False
            name:string  default is None
        """
        super(StringField,self).__init__()
        self.name = name
        self.index = index
        self.required = required
        pass
    
    def typecast_for_read(self, value):
        """
        get the value
        param:
            value:number
        return:
            value:float
        """
        return float(value)

    def typecast_for_storage(self, value):
        """
        get the value
        param:
            value:number
        return:
            value:float
        """
        return float(value)
    
    def acceptable_types(self):
        """
        get the float type
        return:
            float
        """
        return float

    
    
class DateTimeField(StringField):

    def __init__(self,index = False,required = False,name = None):
        """
        initialize 
        param:
            index:True or False
            required:True or False
            name:string  default is None
        """
        #super(DateTimeField, self).__init__(**kwargs)
        #super(DateTimeField,self).__init__()
        StringField.__init__(self,index,required,name)
        #self.name = name
        #self.index = index
        #self.required = required
        #self.auto_now = auto_now
        #self.auto_now_add = auto_now_add


    def typecast_for_read(self, value):
        """
        get the value
        param:
            value:string
        return:
            datetime
        """
        try:
            if isinstance(value,datetime.datetime):
                return value
            else:
                return datetime.datetime.strptime(value,"%Y-%m-%d %H:%M:%S")
        except TypeError, ValueError:
            logger.error("%s error datetime type" % value)
            return None

    def typecast_for_storage(self, value):
        """
        get the value
        param:
            value:string
        return:
            datetime
        """
        if value is None:
            logger.error("%s is Null" % value)
            return None
        if not isinstance(value, datetime.datetime):
            err =  "%s should be datetime object, and not a %s" % (self.name, type(value))
            logger.error(err)
            raise TypeError(err)
        return "%s" % value.strftime("%Y-%m-%d %H:%M:%S")

    def value_type(self):
        """
        get the datetime type
        return:
            datetime
        """
        return datetime

    def acceptable_types(self):
        """
        get the datetime type
        return:
            datetime
        """
        return self.value_type()

########################################### Start Oper Decorater#######################################

def operKey(obj,field):
    """
    operate Key
    param:
        obj:the object 
        field:the string
    """
    return "%s:id:%s:%s" % (obj.__class__.__name__,obj.id, field)


def operSet(fn):
    """
    add operate
    return:
        True or False
    """
    def _new(self, *args, **kws):
        try:
            baseobj = args[0]
            obj = args[1]
            #检查有效性
            if not obj:
                logger.error("please input dest object")
                raise StandardError("please input dest object")
            
            if hasattr(obj,"_id") or hasattr(obj,"id"):
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
    get the operate
    """
    def _new(self, *args, **kws):
        try:
            obj = args[0]
            #print obj.id
            if hasattr(obj,"_id") or hasattr(obj,"id"):
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


class ListField(Attribute):
    
    def __init__(self,ref=None,required=False,name = None):
        """
        initialize
        param:
            ref:default is None
            required:True or False
            name:string
        """
        super(Attribute,self).__init__()
        self.ref = ref
        self.index = False
        self.required = required
        self.name = name

    
    """   添加List 方法  """
    @operSet
    def lpush(self,key,value,**kwargs):
        """
        push the data into list of redis at left of list
        param;
            key:string
            value:string
            **kwargs: a dict
        return:
            True or False
        """
        #LPUSH key value Append an element to the head of the List value at key
        #print "listfield lpush ",key,",",value
        try:
            pipe = RedisClient.getInstance().redis.pipeline()
            pipe.lpush(key,value)
            self.change_log("list:insert",kwargs["obj"].id,kwargs["baseobj"],pipe)
            pipe.execute()
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
    def lpop(self,key,select=None,**kwargs):
        """
        get the data into list of redis at left of list
        param;
            key:string
            value:string
            **kwargs: a dict
            select:the default is None the related object
        return:
            object
        """
        # LPOP key Return and remove (atomically) the first element of the List at key
        #print "lpop key",key
        pk =  RedisClient.getInstance().redis.lpop(key)
        self.change_log("list:delete",pk,kwargs["obj"])
        return  self.ref_klass.objects.filter(id=pk,select=select)

    @operGet
    def rpop(self,key,select=None,**kwargs):
        """
        get the data into list of redis at right of list
        param;
            key:string
            value:string
            **kwargs: a dict
            select:the default is None the related object
        return:
            object
        """
        # RPOP key Return and remove (atomically) the first element of the List at key
        #print "rpop key",key
        pk = RedisClient.getInstance().redis.rpop(key)
        self.change_log("list:delete",pk,kwargs["obj"])
        return  self.ref_klass.objects.filter(id=pk,select=select)
    
    @operGet
    def llen(self,key,**kwargs):
        """
        get the length of list
        param:
            key:string
            **kwargs:dict
        return:
            length of list
        """
        # LLEN key Return the length of the List value at key
        #print "len key",key
        return RedisClient.getInstance().redis.llen(key)
    
    @operGet
    def lrange(self,key,start=0,end=10,select=None,**kwargs):
        """
        get the date in the list
        param:
            key:string
            start:integer default is 0
            end:integer  default is 10
            select:default is None related object
            **kwargs:dict
        return:
            the data in list
        """
        # LRANGE key start end Return a range of elements from the List at key
        n = datetime.datetime.now()
        pks = RedisClient.getInstance().redis.lrange(key,start,end)
        logger.info("lrange key: %s,start: %s, end: %s ,select:%s,use : %s" % (key,start,end,select,datetime.datetime.now() - n))
        return self.ref_klass.objects.filter(id=tuple(pks),select=select)


##    @operGet
##    def ltrim(self,key,start=0,end=10):
##         这个不支持同步
##        # LTRIM key start end Trim the list at key to the specified range of elements
##        return RedisClient.getInstance().redis.ltrim(key,start,end)

    @operSet
    def lrem(self,key,id,count=0,**kwargs):
        """
        LREM key count value Remove the first-N, last-N, or all the elements matching value from the List at key
        param:
            key:string
            count:integer
            **kwargs:dict
        return:
            True or False
        """
        # LREM key count value Remove the first-N, last-N, or all the elements matching value from the List at key
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
        delete the list   use index
        param:
            key:string
            pipe:redis's pipe
            **kwargs:dict
        return:
            True or False
        """
        db = pipe | RedisClient.getInstance().redis
        return db.delete(key)
    
    
class SetField(Attribute):
    def __init__(self,ref=None,required=False,name=None):
        """
        initialize 
        param:
            ref:object default None
            required:True or False
            name:string default is None
        """
        super(Attribute,self).__init__()
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
        # SADD key member Add the specified member to the Set value at key
        try:
            pipe = RedisClient.getInstance().redis.pipeline()
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
    def spop(self,key,select=None,**kwargs):
        """
        SPOP key Remove and return (pop) a random element from the Set value at key
        param:
            key:string
            **kwargs:include obj 
                obj:the object
            select:related object
        return:
            object
        """
        pk = RedisClient.getInstance().redis.spop(key)
        self.change_log("set:delete",pk,kwargs["obj"])
        return self.ref_klass.objects.filter(id=pk,select=select)
    
    
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
        try:
            pipe = RedisClient.getInstance().redis.pipeline()
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
            count
        """
        return RedisClient.getInstance().redis.scard(key)
    
    @operGet
    def sismember(self,key,member_id,**kwargs):
        """
        SISMEMBER key member Test if the specified value is a member of the Set at key
        param:
            key:string
            member_id:string
            **kwargs:dict
        return:
            objects of list
        """
        return RedisClient.getInstance().redis.sismember(key,member_id)
    
    @operGet
    def smembers(self,key,select=None,**kwargs):
        """
        SMEMBERS key Return all the members of the Set value at key 
        param:
            key:string
            select:object  default is None
            **kwargs:dict
        return:
            objects of list
        """
        n = datetime.datetime.now() 
        pks = RedisClient.getInstance().redis.smembers(key)
        logger.info("smembers key: %s,select: %s,use: %s" % (key,select,datetime.datetime.now() - n))
        return self.ref_klass.objects.filter(id = tuple(pks),select=select)
    
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
        db = pipe | RedisClient.getInstance().redis
        return db.delete(key)



class SortSetField(Attribute):
    def __init__(self,ref=None,required=False,index = False,name=None):
        """
        initialize
        param:
            ref:obejct
            required:True or False
            index:True or False
            name:string  default is None
        """
        super(Attribute,self).__init__()
        self.name = name
        self.index = index
        self.ref = ref
        self.required = required
        
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
            pipe = RedisClient.getInstance().redis.pipeline()
            pipe.zadd(key ,member ,score)
            self.change_log("sortset:insert",kwargs["obj"].id,kwargs["baseobj"],pipe,score)
            pipe.execute()
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
        return RedisClient.getInstance().redis.zrank( key , member_id)
    
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
        return RedisClient.getInstance().redis.zrevrank( key ,member_id)
    
    @operGet
    def  zrange(self, key , start=0, end=10,select=None,**kwargs):
        """
        get the the member in sorted set  between start and end
        in front is the lowest score
        param:
            key:string
            start:integer
            end:integer
            select:object  default is None
            **kwargs:dict
        return:
            members of list
        """
        pks = RedisClient.getInstance().redis.zrange( key ,start, end)
        return self.ref_klass.objects.filter(id=tuple(pks),select=select)
    
    @operGet
    def  zrevrange(self, key ,start=0, end=10,select = None,**kwargs):
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
        pks = RedisClient.getInstance().redis.zrevrange( key ,start, end)
        return self.ref_klass.objects.filter(id=tuple(pks),select=select)
    
    @operGet
    def  zrangebyscore(self, key ,min, max,select = None,**kwargs):
        """
        get the the member in sorted set  between min and max
        param:
            key:string
            min:integer
            max:integer
            select:object  default is None
            **kwargs:dict
        return:
            members of list
        """
        pks = RedisClient.getInstance().redis.zrangebyscore( key ,min, max)
        return self.ref_klass.objects.filter(id=tuple(pks),select=select)
    
    @operGet
    def  zscore(self, key ,member_id,**kwargs):
        """
        get the score of member
        param:
            key:string
            member_id:integer
            **kwargs:dict
        return:
            score
        """
        return RedisClient.getInstance().redis.zscore( key ,member_id)
    
    
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
        return RedisClient.getInstance().redis.zcard( key )
    
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
            pipe = RedisClient.getInstance().redis.pipeline()
            pipe.zrem( key,member_id)
            self.change_log("sortset:delete",member,kwargs["baseobj"])
            pipe.execute()
            return True
        except Exception,e:
            pipe.reset()
            logger.error(e)
            return False
        #return RedisClient.getInstance().redis.zrem( key,member_id)


