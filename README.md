# 欢迎使用Python 服务端开发框架 Fastor

**Fastor**是一款专为Python 打造的API与后端管理系统，通过精心的设计与技术实现，集成了大部分稳定开发组件，memcache ， redis，tornado，django，mysql 等。特点概述：
 
- **功能丰富** : 支持大部分服务器组件，支持API Doc；
- **得心应手** : 简单的实例，非常容易上手；
- **代码自动生成** : 根据定义的model模型，自动生成增删改查代码。
- **性能优先** :  API使用Tornado开发，性能极高。
- **稳定服务** :  django和tornado经过深度优化，例如:数据库连接自动重连，缓存过期防止雪崩策略等等。


-------------------

## 开始使用
## Fastor 分为2个系统

### 1）后端管理系统
![后台系统](https://picture-1253291048.cos.ap-shanghai.myqcloud.com/s.png)

### 2）API系统
![Api系统](https://picture-1253291048.cos.ap-shanghai.myqcloud.com/api.png)

-------------------

## 环境配置
##### 部署
- 下载或者clone fastor 代码
- 支持python2.7，目前不支持python3.0。

## 框架结构
##### APP 目录结构
- api: API 接口代码
- app: ORM Model与后端Views代码
- background: 分布式异步处理Async代码 & 定时任务
- base: 基类和一些帮助函数
- base/site-packages: 这里优先使用的是代码中的 site-packages 的python第三方类库

## 一 后端管理系统

##### 1）配置 base/settings.py
- 创建数据库fastor_db
- 配置数据库连接参数
- 配置redis连接参数
- 配置memached连接参数
- 其他配置等
``` python
示例
'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'fastor_db',  # Or path to database file if using sqlite3.
                'USER': 'root',  # Not used with sqlite3.
                'PASSWORD': '123456',  # Not used with sqlite3.
                'HOST': '127.0.0.1',  # Set to sempty string for localhost. Not used with sqlite3.
                'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
                'CHARSET': 'utf8',
                'OPTIONS': {
                    'init_command': 'SET storage_engine=INNODB; SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;set autocommit=1;',
                },
            },
```
#####  配置 app/settings.py
- 配置应用(app) 如第一次使用默认配置即可


##### 2）配置成功后，同步数据库并运行演示程序
``` python
cd app/
python manager.py syncdb #同步数据库并创建管理员
python runserver #启动服务
open http://127.0.0.1:8000/ ， 并使用刚创建的管理员账号密码登录
```


##### 3）创建自己的 models
 #####  1. 在目录 iclass/models/中创建model文件，例如 user.py
 #####  2. 在 iclass/models/__init__中导入 user 中的model对象
 #####  3. 示例
``` python


class BaseUser(models.Model):
    """
    用户
    """

    user_id = models.CharField(max_length=32, verbose_name=u'用户ID', default='',primary_key=True)
    username = models.CharField( max_length=11, verbose_name=u'用户名', default='')
    nickname = models.CharField(max_length=20, verbose_name=u'昵称', default='')
    password = models.CharField(max_length=100, verbose_name=u'密码', default='')
    image_url = models.CharField( max_length=255, verbose_name=u'用户头像', default='')
    sex = models.IntegerField( verbose_name=u'性别', default='1')
    email = models.CharField( max_length=50, verbose_name=u'邮箱', default='' )
    status = models.IntegerField( verbose_name=u'状态', default='0' )  # 0-关闭，1-开启
    register_from = models.IntegerField(verbose_name=u'注册设备', default='0', choices=RegisterFromChoices)
    last_login_time =  models.DateTimeField(auto_now_add=True, verbose_name=u'最后登录时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    
    class Meta:
        app_label = "iclass"
        db_table = "user"
        verbose_name = u"客户"

```

#####  4）.执行自动生成view/templates代码  python manage.py gencode iclass.models.base_user BaseUser
     - 这里将会在views和templates自动生成增删改查的代码
     - 在iclass/urls.py 编写url规则
     - view 导入views/__init__.py
     - 设置入口导航 iclass/templates/cms_index/left_side_menu.html
     

#####  5)  后台系统服务部署

    -  部署nginx ，nginx配置文件路径， app/conf/nginx.conf 
    -  执行 bash app/app.sh 执行进程的数量，端口号均在这里配置。


#####  6)  为了区分开发环境和线上环境支持本地my_settings.py，如果配置了my_settings.py,将覆盖原有配置，默认加到了.gitignore

    - 配置 app/my_settings.py

``` python
#示例配置
def load_settings(settings):
    settings.update({
      
        'DEBUG': True,
       
        'CACHES': {
            'default': {
                'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            }
        },
     
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'fastor_db',  # Or path to database file if using sqlite3.
                'USER': 'api',  # Not used with sqlite3.
                'PASSWORD': 'Win123456',  # Not used with sqlite3.
                'HOST': '58ec9db06f05c.sh.cdb.myqcloud.com',
                'PORT': '3612', 
                'CHARSET': 'utf8',
                'OPTIONS': {
                    'init_command': 'SET storage_engine=INNODB; SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;set autocommit=1;',
                },
            },

        },

        'AUTHENTICATION_BACKENDS': (
            "django.contrib.auth.backends.ModelBackend",
            "app.user.backends.LDAPBackend",
        ),

      
        "memcache_settings": {
            "func_cache": ["127.0.0.1:11211"],
        },

        'redis_settings': {
            "REDIS_BACKEND": {"servers": '127.0.0.1', "port": 6379, "db": 11},
            "MQUEUE_BACKEND": {"servers": '127.0.0.1', "port": 6379, "db": 12},
            "MASTER_REDIS": {"servers": '127.0.0.1', "port": 6379, "db": 9},
            "SLAVE_REDIS": {"servers": '127.0.0.1', "port": 6379, "db": 9},
        },

        "memcache_proxy_settings": {

        },

    })


```

## 二 API管理系统

##### 1）运行api管理系统

``` python
cd api/
python main.py --doc --debug --logging=debug

API系统默认用户名:admin， 密码:123456
密码可以在api/settings.py 中配置 ["api"]["password"] = "123456"
```

##### 2）创建api文件，在api/handler/user_api.py


``` python
示例代码user_api.py
@handler_define
class GetUserInfo(CachedPlusHandler):

    def get_cache_expire(self):
        return 60 * 1

    def get_cache_key(self):
        return {
            'user_id': self.arg('user_id', ''),
        }

    @api_define("GetUserInfo", r'/user/info/detail',
                [
                    Param('user_id', True, str, "", "201702071511512892383865", u'用户id'),
                ],
                description="""读取用户基本信息""",
                return_desc=""""""
                )
    def get(self):
        user_id = self.arg('user_id')

        user = BaseUser.objects.filter(user_id=user_id).first()
        if not user:
            response = {
                "code": 0,
                "status": "fail",
                "msg": "用户不存在",
            }
            return self.write(result)


        response = {
            "status": "success",
            "code": 200,
            "user":user.to_json()
        }
        return self.write(response)

```

##### 2）注册api，在api/document/doc_insall_handlers.py 注册新增api

``` python
示例代码

INSTALL_HANDLERS = [
    "api.handler.common",
    "api.handler.user_api",
]

INSTALL_HANDLERS_NAME = {
    "api.handler.common": "通用接口",
    "api.handler.user_api":"用户接口",
}

```

##### 3）重新运行API
``` python
python main.py --doc --debug --logging=debug

```

##### 4）API 缓存配置

``` python
from api.view.base import BaseHandler , CachedPlusHandler


#1.接口缓存
@handler_define
class GetUserInfo(CachedPlusHandler):

    #这个方法返回接口缓存时间带娃秒
    def get_cache_expire(self):
        return 60 * 1

    #这个方法返回缓存key值，一般返回请求参数即可
    def get_cache_key(self):
        return {
            'user_id': self.arg('user_id', ''),
        }

#2.方法缓存

from wi_cache import function_cache

#cache_keys.方法参数，如多个参数用逗号分隔。例如："user_id,course_id"
#prefix:缓存key前缀#expire_time：缓存时间单位秒

@classmethod
@function_cache(cache_keys="user_id", prefix="func#get_user", expire_time=60*5)
def get_user(cls, user_id):
    user = cls.objects.filter(user_id=user_id).first()
    return user 

```

#####  5）API 异步处理

``` python
#示例客户端代码


@handler_define
class AsyncDemo(BaseHandler):
    

    @api_define("AsyncDemo", r'/api/async/demo', [
        Param('user_id', True, str, "" , "123456" , u'用户ID'),
        Param('course_name', True, str, "","Ed老师的python课程" , u'课程名称'),
    ], description="[示例]处理异步事件", return_desc="""""")
    def get(self):
        
        user_id = self.arg("user_id")
        course_name = self.arg("course_name")

        data = {
            "user_id":user_id,
            "course_name":course_name,
        }

        dispatch_client = Client()
        dispatch_client.dispatch("demo.async.send", data)
        
   
        response = {
            "code": 200,
            "status": "success",
        }

        return self.write(response)

``` 



``` python
#示例服务端代码 background/demo.py

def do_sync_worker(data):
    print "**Recieve data: ", data
    logging.error(data)
   



if __name__ == "__main__":

    worker = Worker("demo.async.send",support_brpop=False)
    try:
        worker.register(do_sync_worker)
        worker.start()
    except KeyboardInterrupt:
        worker.stop()
        print "exited cleanly"
        sys.exit(1)
    except Exception as e:
        logging.error(e)

``` 


``` python
#示例服务端代码启动配置 background/supervisord.conf
#启动：supervisord -c  background/supervisord.conf
#重启：supervisorctl -c  background/supervisord.conf restart all

[program:demo]
process_name = demo-%(process_num)s
command=/data/python2.7/bin/python /data/python/fastor/background/demo.py
process_name=%(program_name)s_%(process_num)02d
stdout_logfile = /data/logs/demo.log
numprocs=2 #这里需要配置你并发处理任务的进程数量
autostart=true


``` 


#####  6)  API系统服务部署

    -  部署nginx ，nginx配置文件路径， api/conf/nginx/nginx.conf 
    -  执行 bash api/tornado.sh 执行进程的数量，端口号均在这里配置。


##### Fastor 这个单词并非拼错，faster + 人 = Fastor （人效更高）的意思
##### 作者： 向Ed老师曾经的战友们致敬！



