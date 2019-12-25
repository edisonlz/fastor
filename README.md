# 欢迎使用Python 服务端开发框架 Fastor

**Fastor**是一款专为Python 打造的API与后端管理系统，通过精心的设计与技术实现，集成了大部分稳定开发组件，memcache ， redis，tornado，django，mysql 等。特点概述：
 
- **功能丰富** : 支持大部分服务器组件，支持API Doc。
- **得心应手** : 简单的实例，非常容易上手。
- **代码自动生成** : 根据定义的model模型，自动生成增删改查代码。
- **性能优先** :  API使用Tornado开发，性能极高。
- **稳定服务** :  django和tornado经过深度优化，例如:数据库连接自动重连，缓存过期防止雪崩策略等等。
- **支付功能** : 支持微信，支付宝支付功能。
- **API安全** : 在nginx层使用lua插件，对api签名并校验。


Fastor  = faster + 人 ， 意为（人效更高）

-------------------

## 开始使用
## Fastor 分为后端管理系统和API系统

### 1）后端管理系统
![后台系统](https://picture-1253291048.cos.ap-shanghai.myqcloud.com/s.jpeg)

### 2）API系统
![Api系统](https://picture-1253291048.cos.ap-shanghai.myqcloud.com/api.png)

### 3）系统架构图
![系统架构图d&](https://picture-1253291048.cos.ap-shanghai.myqcloud.com/dddd.png)

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

``` python
 """
    自动生成view.templates 说明：

    图像上传: field_name 中包括 image 字符串的会自动检测为图像控件
    时间: field_type 等于 DatetimeField 会自动生成时间控件
    poistion 字段：如果包含position 字段，1，数据不分页 2.可以生成拖动保存位置
    choices: 如果 module 里面包括choices，自动生成select控件
    """
``` 

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

##### 7) 关于上传图片地址的配置
``` python

base/settings.py

#上传到本地地址
'SAVE_IMAGE_PATH':"/tmp",
#这个本地地址chrome访问无权限，如果存储在本地，可以启动nginx作为代理服务器访问本地图片
"IMAGE_URL_HOST":"file:///private/tmp",

#参考配置
server {
    listen 80;
    server_name image.fastor.com;
    charset utf-8;

    location / {
        alias /data/images/;
        expires 15m;
    }
}

"IMAGE_URL_HOST":"http://image.fastor.com",


备注：建议上传到腾讯云或者阿里云的对象存储中。

```

##### 8) DBrouter配置
``` python

base/settings.py

#默认配置
'DATABASE_ROUTERS': ['app.db_router.MainRouter'],
#语法： { 'app_label': '数据库连接' }
'DATABASE_MAPPING': {},
'DATABASE_READ_MAPPING': {},

#读写分离配置
'DATABASE_MAPPING': {"iclass":"default"},
DATABASE_READ_MAPPING': {"iclass":"slave"},
```


##### 9) UMeditor配置
``` python

配置地址：app/statics/umeditor/umeditor.conf

#默认配置，如有需要可自行配置
        ,imageUrl:"/editor/upload_img"   //图片上传地址
        ,imageFieldName: "files[]"       //图片数据的key,若此处修改，需要在后台对应文件修改对应参数

```

##### 10) 右侧菜单选中规则
``` python

右侧菜单：app/iclass/templates/cms_index/left_side_menu.html
data-menu-id="100"

#view 对应的增删改查 template 中的 menu-sel 须和 data-menu-id值相等
<input type="hidden" id="menu-sel" value="100">


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


``` python
#https://pypi.org/project/hash_ring/

#默认memcached分布式算法使用求余数，
#如果是大型应用，可以将memcached 修改为一致性hash算法
#备注：不建议使用memcached代理服务，对性能有损耗，出问题不好查找
#修改算法路径 /fastor/base/site-packages/wi_cache/__init__.py #148行
# 将 func_cache =  memcache.Client(memcache_settings["func_cache"])
# 替换为 func_cache = MemcacheRing(memcache_settings["func_cache"])

#示例代码
from hash_ring import MemcacheRing
mc = MemcacheRing(['127.0.0.1:11222','127.0.0.1:11111'])
mc.set('hello', 'world')
print mc.get('hello')


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
#重启demo服务：supervisorctl -c  background/supervisord.conf restart demo:*


[program:demo]
process_name = demo-%(process_num)s
command=/data/python2.7/bin/python /data/python/fastor/background/demo.py
process_name=%(program_name)s_%(process_num)02d
stdout_logfile = /data/logs/demo.log
numprocs=2 #这里需要配置你并发处理任务的进程数量
autostart=true


``` 



#####  6）API 增加了微信支付宝支付接口
- 文档详见doc/pay文档
- 需要根据当前业务，实现业务逻辑
- 代码依赖第三发库，PIL,OpenSSL,qrcode 需要部署安装

``` python
#代码示例

@handler_define
class WeixinAppPayHandler(BaseHandler):
   

    @api_define("WeixinAppPayHandler", r'/api/wx/app/pay',
                [ 
                    Param('order_id', True, str, "", "201907261548295499512023", u'订单id'),
                    Param('good_name', True, str, "", "xxx", u'good_name'),
                ],
                description="微信APP支付")
    def get(self):
        application_id = self.arg_int('application_id', 1)
        order_id = self.arg('order_id')
        good_name = self.arg('good_name','')

        order = OrderInfo.objects.filter(order_id=order_id).first() #订单逻辑需要根据当前业务实现
        
        pay = WePayDoPay(
            out_trade_no=order.order_id,
            subject=good_name,
            total_fee= int(order.amount * 100),
            body=good_name,
            ip = self.user_ip,
            payment_type = "NATIVE",
            application_id=application_id
        )

        params = pay.get_pay_params()
        

        results = {
                   "params": params, 
                   "code":200,
                   'status': "success",
                   "msg":"成功",
        }

        return self.write(results)

```

#####  8)  API系统高级方法

``` python
#获取参数，必传
order_id = self.arg('order_id')
#获取参数，带默认值，非必传
order_id = self.arg('order_id','')
#获取int型参数
user_type = self.arg_int('user_type')
#获取bool型参数
is_admin = self.arg_bool('is_admin')
#(用户)客户端ip地址
user_ip = self.user_ip
``` 




#####  9)  API系统服务部署

    -  部署nginx ，nginx配置文件路径， api/conf/nginx/nginx.conf 
    -  执行 bash api/tornado.sh 执行进程的数量，端口号均在这里配置。


``` crontab
日志切割
#Delete old more than 7 days log files
0 0 * * * /data/python/fastor/api/bin/logrotate-nginx.sh > /dev/null 2>&1
5 0 * * * /data/python/fastor/api/bin/logrotate.sh > /dev/null 2>&1
22 2 * * * find /data/logs/ -mtime +7 -type f -name "*log*" -exec rm -rf {} \;
``` 


#####  10)  API安全数字签名，此功能适合高手

``` python

1）API接口安全规则
Method ： GET | POST
增加参数:
_s_: signature 签名
_t_: 当前时间戳，校队系统时间在初始化接口返回,接口参数有效期30分钟
_t_ = timestamp = timestamp + (客户端当前时间 - 客户端从初始化获得timestamp的时间)
这样做到原因是需要客户端校对服务器时间，因为客户端时间有可能不准确。

签名方式:
token_string = req_method + ":" + path + ":" + sorted(query) + ":" + timestamp + ":" + secret
其中：sorted(query) 是按照key的自然顺序排列,然后以key=value的形式累加
例如: GET /test?b=2&a=1
token_string = GET + ":" + /test + ":" + a=1b=2 + ":" + 1457665234 + ":" + secret_xxxxxx
signature = ngx.md5(token_string)

*method为post的情况下，需要将请求发到body中，不支持url参数post*

接口返回状态码为 410 请重新更新服务器时间。
接口返回 403 为签名错误，访问被禁止。

``` 

``` python

2）Nginx 部署，详见 deploy.secure.api.sh
- 这里建议使用 nginx-1.0.4 版本，稳定/性能高。
- deploy.secure.api.sh部署起来过于繁琐，需要花费一定的时间和经历。
- 部署完毕后建议制作镜像。
- 如果下载不到历史版本，可以从百度云盘下载，链接: https://pan.baidu.com/s/19-5fSBn5wM-xwGLZL-K34Q 提取码: jhbt 
``` 


``` python
3）nginx配置示例
  #lua配置地址：api/conf/nginx/lua
  #签名密钥配置：api/conf/nginx/lua/check_pid_signature.lua
              local secret = "82406d2ff6c40894a26a3ad34eafff2f" #32位字符串


    location / {

        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Headers X-Requested-With;
        add_header Access-Control-Allow-Methsods GET,POST,OPTIONS;

        #引入效验文件，如上传图片，初始化接口可不加载该配置
        access_by_lua_file conf/lua/check_pid_signature.lua;

        proxy_pass          http://make_app_api;
        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

``` 

#### 未来版本支持
- tensorflow 基础版本基于大数据的用户分类
- 图像识别  opencv 拍照识别答题卡


##### 作者： 向Ed老师曾经的战友们致敬！



