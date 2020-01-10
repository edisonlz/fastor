#coding=utf-8
from datetime import timedelta, datetime
from django.db import models
from wi_cache import function_cache

class BaseUser(models.Model):
    """
    用户
    """

    SexChoices = (
        (1, '男'),
        (2, '女'),
    )
   
    RegisterFromChoices = (
        (1, 'android'),
        (2, 'ios'),
        (3, 'web'),
        (4, 'H5'),
    )

    RegisterFromDic = {
        "android": 1,
        "ios": 2,
        "web": 3,
        "xcx":12,
        "gzh":10,
    }
    


    user_id = models.CharField(max_length=32, verbose_name=u'用户ID', default='',primary_key=True)
    username = models.CharField( max_length=11, verbose_name=u'用户名', default='')
    nickname = models.CharField(max_length=20, verbose_name=u'昵称', default='')
    password = models.CharField(max_length=100, verbose_name=u'密码', default='')
    image_url = models.CharField( max_length=255, verbose_name=u'用户头像', default='')
    sex = models.IntegerField( verbose_name=u'性别', default='1', choices=SexChoices)
    email = models.CharField( max_length=50, verbose_name=u'邮箱', default='' )
    status = models.IntegerField( verbose_name=u'状态', default='0' )  # 0-关闭，1-开启
    register_from = models.IntegerField(verbose_name=u'注册设备', default='0', choices=RegisterFromChoices)
    last_login_time =  models.DateTimeField(auto_now_add=True, verbose_name=u'最后登录时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    

    class Meta:
        app_label = "iclass"
        db_table = "user"
        verbose_name = u"客户"


    @property
    def sex_str(self):
        this_map = {1: "男", 2: "女"}
        return this_map.get(self.sex, "无")

    @property
    def status_str(self):
        this_map = {0: "关闭", 1: "开启"}
        return this_map.get(self.status, "无")

    @property
    def register_from_str(self):
        return self.RegisterFromDic.get(self.register_from, "无")


    @classmethod
    @function_cache(cache_keys="user_id", prefix="func#get_user", expire_time=60*5)
    def get_user(cls, user_id):
        user = cls.objects.filter(user_id=user_id).first()
        return user 



    def to_json(self,need_level=False):
        dic = { 
                "user_id": self.user_id,
                "username": self.username,
                "nickname": self.nickname,
                "image_url": self.image_url,
        }
        return dic


 
