## BeeCloud Python SDK (Open Source)

[![Build Status](https://travis-ci.org/beecloud/beecloud-python.svg)](https://travis-ci.org/beecloud/beecloud-python) ![license](https://img.shields.io/badge/license-MIT-brightgreen.svg) ![version](https://img.shields.io/badge/version-v3.6.0-blue.svg)

## 简介

本项目的官方GitHub地址是 [https://github.com/beecloud/beecloud-python](https://github.com/beecloud/beecloud-python)

SDK支持以下支付渠道: 
 
 * 微信
 * 支付宝
 * 银联
 * PayPal
 * 百度钱包   
 * 京东
 * 易宝、快钱等

并且包含退款、打款、订阅支付和相应的查询功能，适用于python2.7、python3.4、python3.5、python3.6。


## 安装 Python SDK
从pip快速安装  
`pip install beecloud`  
更新  
`pip install beecloud --upgrade`  
或者下载源码进入sdk安装  
`python setup.py install`  


## 依赖
sdk依赖于开源库[requests](http://docs.python-requests.org/en/latest/)，安装sdk时会自动安装，如果意外安装失败，可以手动安装

```
pip install requests
```

demo依赖于开源web框架[Flask](http://flask.pocoo.org/)，需手动安装

```
pip install Flask
```

## 准备
参考[快速开始](https://beecloud.cn/apply/)，完成开发准备工作。

## 流程

下图为整个支付的流程:
![pic](http://7xavqo.com1.z0.glb.clouddn.com/img-beecloud%20sdk.png)


步骤①：**（从网页服务器端）发送订单信息**  
步骤②：**收到BeeCloud返回的渠道支付地址（比如支付宝的收银台）**  
>*特别注意：
微信扫码返回的内容不是和支付宝一样的一个有二维码的页面，而是直接给出了微信的二维码的内容，需要用户自己将微信二维码输出成二维码的图片展示出来*

步骤③：**将支付地址展示给用户进行支付**  
步骤④：**用户支付完成后通过一开始发送的订单信息中的return_url来返回商户页面**
>*特别注意：
微信没有自己的页面，二维码展示在商户自己的页面上，所以没有return url的概念，需要商户自行使用一些方法去完成这个支付完成后的跳转（比如后台轮询查支付结果）*

此时商户的网页需要做相应界面展示的更新（比如告诉用户"支付成功"或"支付失败")。**不允许**使用同步回调的结果来作为最终的支付结果，因为同步回调有极大的可能性出现丢失的情况（即用户支付完没有执行return url，直接关掉了网站等等），最终支付结果应以下面的异步回调为准。

步骤⑤：**（在商户后端服务端）处理异步回调结果（[Webhook](https://beecloud.cn/doc/?index=webhook)）**
 
付款完成之后，根据客户在BeeCloud后台的设置，BeeCloud会向客户服务端发送一个Webhook请求，里面包括了数字签名，订单号，订单金额等一系列信息。客户需要在服务端依据规则要验证**数字签名是否正确，购买的产品与订单金额是否匹配，这两个验证缺一不可**。验证结束后即可开始走支付完成后的逻辑。

## 使用方法
* 具体使用请参考项目中的`demo`代码；
* 关于字符串的说明，对于`python2`如果需要传入的参数包含中文字符，请传入`unicode`，对于网络请求成功的情况，`BCResult`中返回结果的字符串也是`unicode`形式；对于`python3`，不需要考虑这样的细节；
* 以下的示例和`demo`中出现的关键字`u`（`unicode`）是为了兼容处理，在`python3`环境下不需要作这样的处理；
* 关于请求参数，公用字段（`app_id`，`timestamp`，`app_sign`）会自动处理，不要手动设置，其他字段和`REST API`一致（例如`REST API`中支付部分，对于`WX_JSAPI`支付方式，`openid`是必填的，假设请求参数名为`req_params`，那么应该添加这样的设置 `req_params.openid = 'openid_str'`），请参考[官网](https://beecloud.cn/doc/?index=rest-api)说明，境外支付请参考[Github beecloud-rest-api](https://github.com/beecloud/beecloud-rest-api/)，以下不做额外介绍
* 返回结果是`beecloud.entity.BCResult`实例，包含以下公共字段，其他字段因不同API而异（例如`REST API`中支付部分，支付完成后会返回支付表记录唯一标识`id`，假设返回参数名为`result`，可以通过`result.id`获取结果），同理，请参照上一条列出的文档

参数名 | 说明
---- | -----
result_code | 返回码，0为正常
result_msg | 返回信息， OK为正常
err_detail | 具体错误信息

### 1.初始化

#### ①. `BCApp`对应于`BeeCloud`控制台中的应用，初始化：  

```
from beecloud.entity import BCApp
bc_app = BCApp()
bc_app.app_id = 'your app id'
# app secret被用于支付和查询
bc_app.app_secret = 'your app secret'
# master secret被用于打款和退款
bc_app.master_secret = 'your app master secret'
```

如果相关渠道尚未申请完成，想要体验sdk支付流程，可以开启测试模式

```
from beecloud.entity import BCApp
bc_app = BCApp()
# 不要在上线模式中设置该选项，否则会遇到BC验签错误相关提示
app.is_test_mode = True
bc_app.app_id = 'your app id'
bc_app.test_secret = 'your app test secret'
```

#### ②. 对于支付、打款和退款，需要初始化BCPay：

```python
from beecloud.pay import BCPay
bc_pay = BCPay()
bc_pay.register_app(bc_app)
```

#### ③. 对于查询需要初始化BCQuery：

```python
from beecloud.query import BCQuery
bc_query = BCQuery()
bc_query.register_app(bc_app)
```

### 2.支付
可以参考`demo.py`中`app_bill`

#### 原型：
通过`BCPay`的实例，以`pay`方法，结合`BCPayReqParams`参数，发起支付请求；  
对于线下收款，通过`offline_pay`方法发起请求，用户的支付结果通过`BCQuery`的`query_offline_bill_status`方法查询

#### 调用：

```python
req_params = BCPayReqParams()
req_params.channel = 'UN_WEB'
req_params.title = u'支付测试'
# 分为单位
req_params.total_fee = 1
req_params.bill_no = 'billno123'
# 可选参数
req_params.optional = {'lang': 'python', u'中文key': u'中文value'}
# 支付完成后的跳转页面
req_params.return_url = 'https://beecloud.cn/'
result = bc_pay.pay(req_params)
# 如果result.result_code为0表示请求成功
# 然后对相关的返回参数做处理，比如ALI_WEB会返回重定向url
```


### 3.退款
可以参考`demo.py`中`app_refund`；<br/>
退款接口包含预退款功能，当need_approval字段的值为true时，该接口开启预退款功能，预退款仅创建退款记录，并不真正发起退款，需后续调用审核接口

#### 原型：
通过`BCPay`的实例，以`refund`方法，结合`BCRefundReqParams`参数，发起退款请求

#### 调用：

```python
refund_params = BCRefundReqParams()
# 退款channel为选填参数
refund_params.channel = 'WX'
refund_params.refund_no = 'refundno123'
refund_params.bill_no = 'billno123'
# 分为单位
refund_params.refund_fee = 1
# need_approval为True时表示预退款，需要后期调用 预退款批量审核 API
# refund_params.need_approval = True
result = bc_pay.refund(refund_params)
# 如果result.result_code为0表示请求成功
# 对于支付宝退款，需要重定向至result.url
```


### 4.预退款批量审核
可以参考`demo.py`中`app_audit_pre_refunds`

#### 原型：
通过`BCPay`的实例，以`audit_pre_refunds`方法，结合`BCPreRefundAuditParams`参数，发起预退款批量审核

#### 调用：

```python
req_params = BCPreRefundAuditParams()
req_params.channel = 'WX'
req_params.ids = ['pre_refund_id1', 'pre_refund_id2']
req_params.agree = True
result = bc_pay.audit_pre_refunds(req_params)
# result.result_map为批量同意单笔结果集合
# 对于支付宝，需要重定向至result.url
```


### 5.打款
可以参考`demo.py`中`app_transfer`

#### 原型：
打款分**单笔打款**、**比可企业打款**、**批量打款**；  

 * **单笔打款**包含`WX_REDPACK`（微信红包）、`WX_TRANSFER`（微信企业打款）和`ALI_TRANSFER`（支付宝企业打款），通过`BCPay`的实例，以`transfer`方法，结合`BCTransferReqParams`参数发起打款；  

 * **比可企业打款**通过`BCPay`的实例，以`bc_transfer`方法，结合`BCCardTransferParams`参数发起打款；该打款渠道支持的银行列表，可以通过`BCQuery`中的`query_bc_transfer_supported_banks`方法进行查询；
  
 * **批量打款**目前只支持`ALI`（支付宝批量打款），通过`BCPay`的实例，以`batch_transfer`方法，结合`BCBatchTransferParams`参数发起打款；

#### 调用：
***单笔打款***  
以微信红包为例

```python
transfer_params = BCTransferReqParams()
transfer_params.channel = 'WX_REDPACK'
transfer_params.desc = u'打款说明'
# 微信为10位数字
transfer_params.transfer_no = '0123456789'
# 微信红包1.00-200元，此处以分为单位
transfer_params.total_fee = 100
transfer_params.channel_user_id = 'receiver_wechat_open_id'
# 微信红包初始化BCTransferRedPack
redpack = BCTransferRedPack()
redpack.send_name = 'BeeCloud'
redpack.wishing = u'BeeCloud祝福开发者工作顺利'
redpack.act_name = u'BeeCloud开发者测试中'
transfer_params.redpack_info = redpack
result = bc_pay.transfer(transfer_params)
# result.result_code等于0表示打款成功
# 对于支付宝需要重定向到result.url
```
  
***比可企业打款***

```python
transfer_params = BCCardTransferParams()
# 单位为分
transfer_params.total_fee = 1
transfer_params.bill_no = order_num_on_datetime()
# 最长支持16个汉字
transfer_params.title = u'python比可企业打款测试'
# 银行缩写编码
transfer_params.bank_code = 'BOC'
# 银行联行行号
transfer_params.bank_associated_code = '1043050000'
# 银行全名
transfer_params.bank_fullname = u'中国银行'
# DE代表借记卡，CR代表信用卡
transfer_params.card_type = 'DE'
# 帐户类型，P代表私户，C代表公户
transfer_params.account_type = 'C'
# 收款方的银行卡号
transfer_params.account_no = '5300000'
# 收款方的姓名或者单位名
transfer_params.account_name = u'苏州比可网络科技有限公司'
# 银行绑定的手机号，当需要手机收到银行入账信息时，该值必填，前提是该手机在银行有短信通知业务，否则收不到银行信息
transfer_params.mobile = '1850000'
# 附加数据，选填
transfer_params.optional = {'key1': u'选填的value'}

result = bc_pay.bc_transfer(transfer_params)
# result.result_code等于0表示打款请求成功，但是需要在webhook判定最终打款结果
```
  
***批量打款***

```python
transfer_params = BCBatchTransferParams()
# 11-32位数字字母组合
transfer_params.batch_no = 'abcdefg1234567'
transfer_params.account_name = u'苏州比可网络科技有限公司'
# 每一笔打款细项为BCBatchTransferItem实例
item1 = BCBatchTransferItem()
item1.transfer_id = order_num_on_datetime() + 'a'
item1.receiver_account = '1234567'
item1.receiver_name = u'某人1'
# 以分为单位
item1.transfer_fee = 1
item1.transfer_note = u'python支付宝批量打款item1'

item2 = BCBatchTransferItem()
# 继续像item1一样添加相关设置

transfer_params.transfer_data = [item1, item2]

result = bc_pay.batch_transfer(transfer_params)
# result.result_code等于0时需要重定向到result.url
```


### 6.查询支付订单
可以参考`demo.py`中`app_query_bills`

#### 原型：
通过`BCQuery`的实例，以`query_bills`方法，结合`BCQueryReqParams`参数查询

#### 调用：
```python
query_params = BCQueryReqParams()
# 如果查询全部订单channel不设置即可
query_params.channel = 'WX'
# 限制只返回支付成功的订单
query_params.spay_result = True
result = bc_query.query_bills(query_params)
# 如果查询成功result.bills为beecloud.entity.BCBill的实例列表
```


### 7.查询退款订单
可以参考`demo.py`中`app_query_refunds`

#### 原型：
通过`BCQuery`的实例，以`query_refunds`方法，结合`BCQueryReqParams`参数查询

#### 调用：
```python
query_params = BCQueryReqParams()
# 如果查询全部订单channel不设置即可
query_params.channel = 'WX'
result = bc_query.query_refunds(query_params)
# 如果查询成功result.refunds为beecloud.entity.BCRefund的实例列表
```


### 8.查询支付订单数目
可以参考`demo.py`中`app_query_bills_count`

#### 原型：
通过`BCQuery`的实例，以`query_bills_count`方法，结合`BCQueryReqParams`参数查询

#### 调用：
```python
query_params = BCQueryReqParams()
# 如果查询全部订单channel不设置即可
query_params.channel = 'WX'
query_params.spay_result = True
result = bc_query.query_bills_count(query_params)
# 如果查询成功result.count表示满足条件的数目
```


### 9.查询退款订单数目
可以参考`demo.py`中`app_query_refunds_count`

#### 原型：
通过`BCQuery`的实例，以`query_refunds_count`方法，结合`BCQueryReqParams`参数查询

#### 调用：
```python
query_params = BCQueryReqParams()
# 如果查询全部订单channel不设置即可
query_params.channel = 'WX'
result = bc_query.query_refunds_count(query_params)
# 如果查询成功result.count表示满足条件的数目
```


### 10.根据ID查询支付订单
可以参考`demo.py`中`app_bill_by_id`

#### 原型：
通过`BCQuery`的实例，以`query_bill_by_id`方法，结合支付订单唯一标识id查询

#### 调用：
```python
result = bc_query.query_bill_by_id(bill_id)
# 如果查询成功result.pay为beecloud.entity.BCBill的实例
```


### 11.根据ID查询退款订单
可以参考`demo.py`中`app_refund_by_id`

#### 原型：
通过`BCQuery`的实例，以`app_refund_by_id`方法，结合退款订单唯一标识id查询

#### 调用：
```python
result = bc_query.query_refund_by_id(refund_id)
# 如果查询成功result.refund为beecloud.entity.BCRefund的实例
```


### 12.退款状态更新
可以参考`demo.py`中`app_query_refund_status`；  
退款状态更新接口提供查询退款状态以更新退款状态的功能，用于对退款后不发送回调的渠道（WX、YEE、KUAIQIAN、BD）退款后的状态更新

#### 原型：
通过`BCQuery`的实例，以`query_refund_status`方法，结合渠道类型channel和退款单号refund_no查询

#### 调用：
```python
result = bc_query.query_refund_status(channel, refund_no)
# 如果查询成功result.refund_status为查询到的退款状态
```

  
### 13.订阅支付
先查看[订阅系统说明文档](https://github.com/beecloud/beecloud-rest-api/blob/master/subscription/%E8%AE%A2%E9%98%85%E7%B3%BB%E7%BB%9F%E8%AF%B4%E6%98%8E%E6%96%87%E6%A1%A3.md)了解基础概念  

* **查询计划列表**
  
可以参考`demo.py`中`subscription_plans`  
  
**原型**
  
通过`BCQuery`的实例，以`query_plans`方法，结合`BCQueryCriteria`参数查询，结果包含`BCPlan`的列表；如果设置了`BCQueryCriteria count_only`为`True`，那么结果只包含满足条件的个数`total_count`  
  
**调用**
  
```python
result = bc_query.query_plans()
# 如果查询成功，result.plans为查询到的计划列表
```
  
* **订阅支付支持的银行列表**
  
可以参考`demo.py`中`subscription_supported_banks`  
  
**原型**
  
通过`BCQuery`的实例，结合`query_subscription_payment_supported_banks`方法发起请求
  
**调用**
  
```python
result = bc_query.query_subscription_payment_supported_banks()
# 如果查询成功，result.common_banks包含支持的常用银行列表，result.banks包含全部支持的银行列表
```
  
* **发送验证码**
  
可以参考`demo.py`中`sms`  
  
**原型**
  
通过`BCPay`的实例，结合`send_sms_passcode`方法发起请求，参数接受验证码的手机号，返回结果包含`sms_id`，同时发送`sms_code`到用户手机  
  
**调用**
  
```python
result = bc_pay.send_sms_passcode(mobile)
# 如果请求成功，result.sms_id为本次验证码id
```
  
* **发起订阅**
  
可以参考`demo.py`中`subscribe`  
  
**原型**
  
通过`BCPay`的实例，以`subscribe`方法，结合`BCSubscription`参数、`sms_id`和`sms_code`发起，结果包含`BCSubscription`对象，如果该对象`valid`为`True`表明本次订阅已经即时生效，否则你还需要等待webhook推送最终审核结果；  
`sms_id`和`sms_code`的获取查看获取验证码方法的说明
  
**调用**
  
```python
param = BCSubscription()
param.buyer_id = 'your_system_buyer_id'
param.plan_id = 'plan_id'
param.bank_name = 'choose_from_subscription_payment_supported_banks'
param.card_no = 'bank_card_number'
param.id_name = 'name_on_id_card'
param.id_no = 'id_card_number'
# 和银行卡绑定的手机号
param.mobile = 'mobile_number'
result = bc_pay.subscribe(param, 'sms_id_get_by_send_sms_passcode', 'sms_code_from_user_phone')
# 如果请求成功，result.subscription为创建的订阅对象
```
  
* **取消订阅**
  
可以参考`demo.py`中`cancel_subscription`  
  
**原型**
  
通过`BCPay`的实例，结合`cancel_subscription`方法发起请求，参数为被取消的订阅id  
  
**调用**
  
```python
result = bc_pay.cancel_subscription(sid)
# 如果操作成功，result.id为本次取消的订阅id
```
  
* **查询订阅列表**
  
可以参考`demo.py`中`subscriptions`  
  
**原型**
  
通过`BCQuery`的实例，以`query_subscriptions`方法，结合`BCQueryCriteria`参数查询，结果包含`BCSubscription`的列表；如果设置了`BCQueryCriteria count_only`为`True`，那么结果只包含满足条件的个数`total_count`  
  
**调用**
  
```python
# 自定义你的查询条件
# param = BCQueryCriteria()
# param.limit = 8
# param.buyer_id = 'xz'
result = bc_query.query_subscriptions()
# 如果查询成功，result.subscriptions为查询到的计划列表
```
  
### 14.鉴权
调用`beecloud.utils`中`verify_card_factors`方法，依次传入参数`BCApp`实例、姓名、身份证号、银行卡号、银行预留手机号做四要素鉴权，手机号不传入则三要素鉴权，银行卡号也不传入则二要素鉴权  
  
```python
result = verify_card_factors(bc_app,
                             'name',
                             'id card number',
                             'bank card number',
                             'phone number')
```
result中result_code为0表示鉴权成功。

### 15.商家用户系统
商家可以选择上传用户ID，然后在控制台查看用户行为分析  
调用`beecloud.user`模块中相关方法  

* **注册单个用户**  

调用`add_merchant_user`方法，依次传入参数`BCApp`实例和用户在商家唯一标识符ID，返回result\_code为0表示成功  

```python
add_merchant_user(bc_app, 'merchant_python_user1')
```
  
* **批量导入用户**  

调用`batch_add_merchant_users`方法，依次传入参数`BCApp`实例，商家账户和用户ID列表，返回result\_code为0表示成功  

```python
batch_add_merchant_users(bc_app, 'merchant@email.cn', ['merchant_python_user2', 'merchant_python_user3'])
```

* **用户批量查询**  

调用`query_merchant_users`方法，  
选填参数`merchant`如果传入则查询该商家下所有注册过的用户，否则查询注册时与app关联的用户；  
选填参数`start_time`如果传入返回此时间戳之后创建的用户；  
选填参数`end_time`如果传入返回此时间戳之前创建的用户  

```python
res = query_merchant_users(bc_app, start_time=1499788800000)
if not res.result_code:
    for user in res.users:
        print(user.buyer_id)
```

* **历史数据补全**  

调用`attach_buyer_history_bills`方法，将历史订单和购买用户关联   
参数`bill_info`整体为字典类型，用户ID作为key，该用户的订单号列表作为value，  
如果修改失败，返回`failed_bills`，结构和`bill_info`一样  

```python
bill_info = {'merchant_python_user1': ['test1499839192'],
             'merchant_python_user2': ['test1499839169', 'test1499839127']}
res = attach_buyer_history_bills(bc_app, bill_info)
```

* **关于新下单的说明**  

务必在下单时传入`buyer_id`，表示当前订单的购买用户  

```python
req_params = BCPayReqParams()
req_params.buyer_id = 'merchant_python_user1'
...
```
  
### 16.营销卡券系统
商家可以通过优惠券系统开展营销活动  
调用`beecloud.sales`模块中相关方法  

* **根据ID查询优惠券模板**  

调用`query_coupon_template`方法，依次传入参数`BCApp`实例和优惠券模板ID，返回result\_code为0表示成功，返回的`coupon_template`字段见`beecloud.entity.BCCouponTemplate`

```python
result = query_coupon_template(bc_app, 'coupon-template-id')

if result.result_code == 0:
    template = result.coupon_template
```
  
* **根据条件查询优惠券模板**  

调用`query_coupon_templates`方法，依次传入参数`BCApp`实例和`BCQueryCriteria`实例，返回result\_code为0表示成功，返回的`coupon_templates`为`BCCouponTemplate`列表  

```python
query_criteria = BCQueryCriteria()
query_criteria.name = 'template-name'

result = query_coupon_templates(bc_app, query_criteria)

if result.result_code == 0:
    templates = result.coupon_templates

    if templates and len(templates) > 0:
        template = templates[0]
        print(template.name)
```

* **发放优惠券**  

调用`create_coupon`方法，依次传入参数`BCApp`实例、优惠券模板ID和用户ID，返回result\_code为0表示成功，返回的`coupon`字段见`beecloud.entity.BCCoupon`  

```python
result = create_coupon(bc_app, 'template-id', 'user-id')
if result.result_code == 0:
    coupon = result.coupon

    if coupon:
        print(coupon.id)

        template = coupon.template
        print(template.name)
```

* **根据ID查询优惠券**  

调用`query_coupon`方法，依次传入参数`BCApp`实例和优惠券ID，返回result\_code为0表示成功，返回的`coupon`字段见`BCCoupon`  

```python
result = query_coupon(bc_app, 'coupon-id')
if result.result_code == 0:
    coupon = result.coupon

    if coupon:
        print(coupon.user_id)

        template = coupon.template
        print(template.name)
```
  
* **根据条件查询优惠券**  

调用`query_coupons`方法，依次传入参数`BCApp`实例和`BCQueryCriteria`实例，返回result\_code为0表示成功，返回的`coupons`为`BCCoupon`列表  

```python
query_criteria = BCQueryCriteria()
query_criteria.template_id = 'template-id'

result = query_coupons(bc_app, query_criteria)

if result.result_code == 0:
    coupons = result.coupons

    if coupons and len(coupons) > 0:
        coupon = coupons[0]

        print(coupon.user_id)

        template = coupon.template
        print(template.name)
```
  
* **关于新下单的说明**  

在下单时传入`coupon_id`，表示当前订单使用的优惠券  

```python
req_params = BCPayReqParams()
req_params.coupon_id = 'coupon-id'
...
```


## Demo
项目中的`demo`工程  
1. 请先安装sdk和[Flask](http://flask.pocoo.org/)，请参考`安装`和`依赖`  
2. 运行：cmd进入`demo`文件夹后，运行
```shell
python demo.py
```


## 测试
项目中的`tests`工程为单元测试
>依赖[mock](https://pypi.python.org/pypi/mock)
`pip install mock`


## 常见问题
参见[帮助中心](http://help.beecloud.cn/hc/) 
