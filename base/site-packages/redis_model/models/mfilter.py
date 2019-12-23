#encoding = utf-8

"""
Handles the queries.
"""
import os,sys
import types
from redis_client import RedisClient
#加载配置
import setting
from setting import logger
from datetime import datetime

# Model Set
class ModelSet(object):
    
    def __init__(self, model_class):
        """
        initialize the model class  and get the redis's db
        param:
            model_class: model
        """
        self.model_class = model_class
        self._db = RedisClient.getInstance().redis

    def multi(self,pks,select):
        """
        handle the List  now this is support the id list
        param:
            pks: id list
            select:object related object
        return:
            objects of list
        """
        #print "pks" , pks
        pipe = self.db.pipeline(False)
        #1.批量获取用户数据
        #1.1 解析参数
        
        for pk in pks:
            if select:
                selectlist = select.split(",")
                selectlist.append("id")
                pipe.hmget(self.model_class.dump_fields_key(pk),selectlist)
            else:
                pipe.hgetall(self.model_class.dump_fields_key(pk))

        #1.2执行，批量获取
        objs = pipe.execute()
        #print "objs",objs
        if not objs:
            return []
        
        if select:
            results = objs
            objs = []
            for r in results:
                fields = {}
                if r:
                    for i in xrange(len(r)):
                        fields[selectlist[i]] = r[i]
                    objs.append(fields)

        #2.将原始数据解析为对象
        obj_list = []
        for h in objs:
            obj_list.append(self.model_class(**h))
            
        #3.返回对象列表
        return obj_list
    
    def filters(self,**kwargs):
        """
        Find the fields  when Index = True
        """
        n  = datetime.now()
        cls = self.model_class
        
        #初始化参考参数
        select = ()
        field = value =  None
        for k,v in kwargs.iteritems():
            if str(k).lower() != "select":
                field = str(k)
                value = v
            else:
                select = v
        #print "find " + "* " *20
        #print "field:",field,"value:",value
        
        ##解析 Find 字段
        if field.lower() != "id":
            #初始化find Index 指标
            #Index 保存结构： user:username:index ， yangqun , 1
            index_name = cls.index_name(field)
            index_field = value
            #print "index_name,index_field",index_name,index_field
            #获取primary key
            pk = self.db.hget(index_name,index_field)
        else:
            if(isinstance(value,list) or isinstance(value,tuple)):
                #在这里处理传入一组数据的情况
                pks = value
                data = self.multi(pks,select)
                logger.info("type: %s,filter: %s, use: %s" % (self.model_class.__name__,kwargs,datetime.now() - n))
                return data
            else:
                pk = value
                #Find 是否存在该用户
                hlen = self.db.hlen(cls.dump_fields_key(pk))
                if (hlen==0):
                    return None
        ##End Find 字段


        #到用户表中查找
        if not select:
            #如果没有提交select字段select *
            #print "find key %s" % cls.dump_fields_key(pk)
            fields = self.db.hgetall(cls.dump_fields_key(pk))
        else:
            #print "find key %s" % cls.dump_fields_key(pk)
            selectlist = select.split(",")
            selectlist.append("id")
            fields = {}
            #如果提交select字段select field1，field2，......
            data = self.db.hmget(cls.dump_fields_key(pk),selectlist)
            for i in xrange(len(selectlist)):
                fields[selectlist[i]] = data[i]
            
        #print "field " + "* " * 20
        #print fields
        
        if fields:
            data = cls(**fields)
            logger.info("type: %s,filter: %s, use: %s" % (self.model_class.__name__,kwargs,datetime.now() - n))
            return data
        else:
            return  None
    #别名
    filter = filters

    @property
    def db(self):
        """
        return:
            database
        """
        return self._db
