# -*- coding: utf-8 -*-
"""
    This module shows how to accept BeeCloud webhook push notifications.
    :created by xuanzhui on 2016/04/22.
    :copyright (c) 2015 BeeCloud.
    :license: MIT, see LICENSE for more details.
"""

# 这边只是演示如何接收beecloud webhook推送，实际项目中请遵循Flask项目规范，不要重复创建Flask app入口

# 接收webhook推送需要确保你的服务端地址能够在公网被访问

# 以下为了突出订阅支付，刻意写了两个接口，实际代码中可以按需求合并

from flask import Flask, request
from beecloud.entity import BCApp
import hashlib

app = Flask(__name__)

# 请与你支付和退款的app参数保持一致
bc_app = BCApp()
bc_app.app_id = 'c5d1cba1-5e3f-4ba0-941d-9b0a371fe719'
bc_app.app_secret = '39a7a518-9ac8-4a9e-87bc-7885f33cf18c'
bc_app.master_secret = 'e14ae2db-608c-4f8b-b863-c8c18953eef2'

'''
推送标准：
    HTTP 请求类型 : POST
    HTTP 数据格式 : JSON
    HTTP Content-type : application/json
'''


@app.route('/webhook/payment', methods=['POST'])
def app_payment_webhook():
    # 获取json数据
    json_data = request.get_json()

    # 第一步：验证数字签名
    # 从beecloud传回的sign
    bc_sign = json_data.get('signature')

    # 自己计算出sign -- app_id + transaction_id + transaction_type + channel_type + transaction_fee + master_secret 的MD5签名
    transaction_id = json_data.get('transaction_id')
    transaction_type = json_data.get('transaction_type')
    channel_type = json_data.get('channel_type')
    transaction_fee = json_data.get('transaction_fee')

    my_sign = hashlib.md5((bc_app.app_id + transaction_id + transaction_type + channel_type +
                           str(transaction_fee) + bc_app.master_secret).encode('UTF-8')).hexdigest()

    # 判断两个sign是否一致
    if bc_sign != my_sign:
        return ''

    # 如果一致第一个检验通过
    '''
    理论上说到这一步就可以
    return 'success'
    以下的业务逻辑请根据商户内部需求处理，
    不需要重发了就应该返回success
    '''

    '''
    注意：
    支付、退款和打款都会发送webhook，
    获取类型的方法
    transaction_type = json_data.get('transaction_type')
    以下以支付为例（对应type为'PAY'）
    '''

    # 第二步：过滤重复的Webhook
    '''
    同一条订单可能会发送多条支付成功的webhook消息，
    这有可能是由支付渠道本身触发的(比如渠道的重试)，
    也有可能是BeeCloud的Webhook重试。
    客户需要根据订单号进行判重，忽略已经处理过的订单号对应的Webhook。
    '''
    # 获取订单号，即上面的transaction_id
    '''
    以下为伪代码：
    #从自己系统的数据库中根据订单号取出订单数据，如发现已经支付成功，则忽略该订单
    bill_info = db_utils.get_bill_by_num(bill_num)
    if bill_info.pay_result == 'SUCCESS':
        return ''
    '''

    # 第三步：验证订单金额，即上面的transaction_fee，以分为单位
    '''
    以下为伪代码：
    # 如果金额不匹配，表明订单可能被篡改
    if bill_info.bill_fee != transaction_fee:
        return ''
    '''

    # 如果金额匹配第二个检验通过

    # 第四步：处理业务逻辑和返回
    # 更新你的订单状态
    # update_bill(...)

    # 用户返回 success 字符串给BeeCloud表示 - 正确接收并处理了本次Webhook
    # 其他所有返回都代表需要继续重传本次的Webhook请求
    return 'success'


@app.route('/webhook/subscription', methods=['POST'])
def app_subscription_webhook():
    # 获取json数据
    json_data = request.get_json()

    # 第一步：验证数字签名
    # 从beecloud传回的sign
    bc_sign = json_data.get('sign')

    # 自己计算出sign -- App ID + App Secret + timestamp 的 MD5 生成的签名 (32字符十六进制)
    timestamp = json_data.get('timestamp')

    my_sign = hashlib.md5((bc_app.app_id + bc_app.app_secret + str(timestamp)).encode('UTF-8')).hexdigest()

    # 判断两个sign是否一致
    if bc_sign != my_sign:
        return ''

    # 如果一致第一个检验通过
    '''
    理论上说到这一步就可以
    return 'success'
    以下的业务逻辑请根据商户内部需求处理，
    不需要重发了就应该返回success
    '''

    # 判断订阅或者订阅扣款有没有成功
    if not json_data.get('trade_success'):
        # 没有成功的情况获取失败原因，自行处理
        if json_data.get('message_detail'):
            err_msg = json_data.get('message_detail').get('err_msg')
        return 'success'

    # 第二步：过滤重复的Webhook，处理业务逻辑和返回

    # 获取的id可能是用户订阅的id，也可能是订阅扣款的id
    transaction_id = json_data.get('transaction_id')

    # 获取本次推送的消息类型
    transaction_type = json_data.get('transaction_type')
    sub_channel_type = json_data.get('sub_channel_type')

    if transaction_type == 'SUBSCRIPTION':
        # 表示用户订阅的结果推送
        '''
        从自己系统的数据库中取出保留的用户订阅记录id（在发起订阅的时候相关sdk会返回），
        和这边的transaction_id比较，如果transaction_id相同，看自己数据库中对应记录的状态，
        如果尚未生效，可以标记订阅状态为生效；如果状态已经是生效的，那么直接忽略
        '''
        # 这边有一个比较重要的信息card_id可以在获取第一次推送的时候留存，
        # 它是由{订阅用户银行名称、订阅用户银行卡号、订阅用户身份证姓名、订阅用户身份证号、订阅用户银行预留手机号}的组合确定，
        # 其他的信息建议在创建的时候就保存
        print(u'订阅成功')
        message_detail = json_data.get('message_detail')
        if message_detail:
            print(u'订阅账户标识id：' + message_detail.get('card_id'))
    elif transaction_type == 'PAY' and sub_channel_type == 'BC_SUBSCRIPTION':
        # 表示扣款的结果推送
        '''
        查看自己的系统中有没有transaction_id对应的订阅扣款订单，如果没有可以插入新的记录留存；
        如果已经包含相关的记录，那么直接忽略；
        详细的信息可以通过如下方式获取
        '''
        print(u'扣款订单号：' + str(json_data.get('transaction_id')))
        print(u'订阅扣款费用：' + str(json_data.get('transaction_fee')))
        message_detail = json_data.get('message_detail')
        if message_detail:
            print(u'订阅id：' + message_detail.get('subscription_id'))
            print(u'订阅计划id：' + message_detail.get('plan_id'))
            print(u'订阅用户在商户系统的id：' + message_detail.get('buyer_id'))
            print(u'订阅扣款账户id：' + message_detail.get('card_id'))
            print(u'订阅用户身份证号：' + message_detail.get('id_no'))
            print(u'订阅用户身份证姓名：' + message_detail.get('id_name'))
            print(u'订阅用户银行卡号：' + message_detail.get('card_no'))
            print(u'订阅用户银行名称：' + message_detail.get('bank_name'))
            print(u'订阅用户银行预留手机号：' + message_detail.get('mobile'))

    # 用户返回 success 字符串给BeeCloud表示 - 正确接收并处理了本次Webhook
    # 其他所有返回都代表需要继续重传本次的Webhook请求
    return 'success'


if __name__ == '__main__':
    app.debug = True
    # app.run(host='pythondemo.beecloud.cn', port=80)
    app.run()
