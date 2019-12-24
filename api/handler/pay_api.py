# -*- coding: utf-8 -*-
import os,sys
from api.view.base import BaseHandler , CachedPlusHandler
from api.document.doc_tools import *
from app.iclass.models import *
from django.conf import settings
import time, datetime
from xml.etree.ElementTree import XML
import time
import logging
import tornado
import json
import hashlib
from api.util.paylib.qr_code_generator import mk_qr
from api.util.paylib.wepayapi import *
from api.util.paylib.alipayapi import *
import traceback


##############################################################
#                 Web端检测支付成功轮训接口                    #
#############################################################


@handler_define
class QrcodeRoundPollStatusHandler(BaseHandler):
    

    @api_define("QrcodeRoundPollStatusHandler", r'/api/order/roll/status',
                [ 
                    Param('order_id', True, str, "", "201907221705372504535818", u'订单id'),
                ],
                description="二维码支付-检测支付成功，2s轮训")
    def get(self):
        application_id = self.arg_int('application_id', 1)
        order_id = self.arg('order_id')
        order = OrderInfo.objects.filter(order_id=order_id).first()

        pay = False
        if order.status == "2":
            pay = True

        ret = {
            "code": "200",
            "msg": "请求成功",
            "pay":pay,
        }

        return self.write(ret)


##############################################################
#                        APP端支付                           #
#############################################################


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

        order = OrderInfo.objects.filter(order_id=order_id).first()
        
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



@handler_define
class AliPayHandler(BaseHandler):

    @api_define("AliPayHandler", r'/api/live/ali/do/pay', [
        Param('order_id', True, int, "str", "201907291342455810652881", u'order_id'),
        Param('good_name', True, int, "str", "xx商品", u'商品名称'),
    ], description=u"阿里APP支付宝支付", protocal="http")
    def post(self):

        order_id = self.arg('order_id')
        good_name = self.arg('good_name')
        order = OrderInfo.objects.filter(order_id=order_id).first()

        pay = AliPayDoAppPay(
                orderid=order.order_id, 
                goodsName=good_name, 
                goodsPrice='%.2f' % (float(order.amount)),
            )
        params = pay.do_pay_params()

        #print params
        data = {'order_id': order_id}
        data["pay_params"] = params

        r = {
            'status': "success",
             "data": data, 
             "code":200,
             "ip":self.user_ip,
        }
        return self.write(r)


##############################################################
#                        Web端支持                            #
#############################################################




##############################################################
#                        微信支付接口                         #
#############################################################



@handler_define
class WeixinGetScanPayQrcodeHandler(BaseHandler):
    """
    微信扫码支付模式一获取支付二维码
    主要作为线下支付用途
    """



    @api_define("WeixinScanPayHandler", r'/api/wx/qrcode',
                [ 
                    Param('order_id', True, str, "", "201907221705372504535818", u'订单id'),
                ],
                description="微信二维码支付")
    def get(self):
        application_id = self.arg_int('application_id', 1)
        order_id = self.arg('order_id')
        good_name = "17Class产品" #这里需要设置成你们自有的产品名字
        order = OrderInfo.objects.filter(order_id=order_id).first()
       

        pay = WePayDoPay(
            out_trade_no=order.order_id,
            subject=good_name,
            total_fee= int(order.amount * 100),
            body=good_name,
            ip = self.user_ip,
            payment_type = "NATIVE",
            application_id=application_id
        )

        params = pay.do_pay_params()
        code_url = pay.code_url
        res = mk_qr(code_url, filename_pre_fix='order_')
        cdn_url = res.get('url', '')
        

        results = {
                   "code":200,
                   "params": pay.code_url, 
                   "url":cdn_url,
                  }
        return self.write(results)





@handler_define
class WePayNoticeHandler(BaseHandler):

    
    @api_define("WeChat Callback Url", r'/api/live/wepay/notice', [
    ], description=u"微信支付成功通知接口",)
    def post(self):
        body = self.request.body

        #body = "<xml><appid><![CDATA[wxeac3211dfd4fca9e]]></appid>\x0A<bank_type><![CDATA[CFT]]></bank_type>\x0A<cash_fee><![CDATA[100]]></cash_fee>\x0A<fee_type><![CDATA[CNY]]></fee_type>\x0A<is_subscribe><![CDATA[N]]></is_subscribe>\x0A<mch_id><![CDATA[1541433441]]></mch_id>\x0A<nonce_str><![CDATA[cy5jrmnpxgkst8i3]]></nonce_str>\x0A<openid><![CDATA[ocPo_1IdNvc5OdEjCBh8dGY330vE]]></openid>\x0A<out_trade_no><![CDATA[201907251646076124496637]]></out_trade_no>\x0A<result_code><![CDATA[SUCCESS]]></result_code>\x0A<return_code><![CDATA[SUCCESS]]></return_code>\x0A<sign><![CDATA[34786315644C4739785D3C29060828A3]]></sign>\x0A<time_end><![CDATA[20190725164623]]></time_end>\x0A<total_fee>100</total_fee>\x0A<trade_type><![CDATA[NATIVE]]></trade_type>\x0A<transaction_id><![CDATA[4200000384201907255202260035]]></transaction_id>\x0A</xml>"
        if not body:
            self.write('''
                    <xml>
                      <return_code><![CDATA[FAIL]]></return_code>
                      <return_msg><![CDATA[FAIL]]></return_msg>
                    </xml>
                    ''')

        logging.error(body)
        xml = XML(body)


        wp = WePayDoPay(out_trade_no='',
                subject='',
                total_fee='',
                body='',
                ip = self.user_ip)

        success = wp.verify_notice_sign(xml)
        logging.error("sign: %s" % success)

        if not success:
            self.write('''
                    <xml>
                      <return_code><![CDATA[FAIL]]></return_code>
                      <return_msg><![CDATA[Sign error]]></return_msg>
                    </xml>
                    ''')

        #####
        #这里是你支付成功的代码逻辑
        #####

        #这里是解析支付数据代码
        data = self.create_order(xml)
        OrderInfo.success()

        self.write('''
                <xml>
                  <return_code><![CDATA[SUCCESS]]></return_code>
                  <return_msg><![CDATA[OK]]></return_msg>
                </xml>
                ''')
        

    @classmethod
    def create_order(cls,xml):
        root = xml
        logging.error(xml)
        wcn = {}
        wcn["app_id"] = root.find('appid').text
        wcn["transaction_id"] = root.find('out_trade_no').text
        wcn["channel_transaction_id"] = root.find('transaction_id').text
        bank_type = root.find('bank_type')

        if bank_type is not None:
            wcn["channel_type"] = bank_type.text

        cash_fee = root.find('cash_fee')
        if cash_fee is not None:
            wcn["transaction_fee"] =float( root.find('cash_fee').text )

        fee_type = root.find('fee_type')
        if fee_type is not None:
            wcn["fee_type"] = fee_type.text

        is_subscribe = root.find('is_subscribe')
        if is_subscribe is not None:
            wcn["is_subscribe"] = is_subscribe.text

        wcn["mch_id"] = root.find('mch_id').text
        wcn["nonce_str"] = root.find('nonce_str').text

        device_info = root.find('device_info')
        if device_info is not None:
            wcn["device_info"] = device_info.text
        
        result_code = root.find('result_code')
        if result_code is not None:
            wcn["result_code"] = result_code.text

        openid = root.find('openid')
        if openid is not None:
            wcn["openid"] = openid.text

        return_code = root.find('return_code')
        if return_code is not None:
            wcn["return_code"] = return_code.text

        wcn["sign"] = root.find('sign').text

        time_end = root.find('time_end')
        if time_end is not None:
            wcn["time_end"] =  time_end.text

        trade_type = root.find('trade_type')
        if trade_type is not None:
            wcn["sub_channel_type"] =  trade_type.text

        err_code_des = root.find('err_code_des')
        if err_code_des is not None:
            wcn["err_code_des"] =  err_code_des.text

        attach = root.find('attach')
        if attach is not None:
            wcn["attach"] =  root.find('attach').text

        coupon_fee = root.find('coupon_fee')
        if coupon_fee is not None:
            wcn["coupon_fee"] = coupon_fee.text

     
        wcn["transaction_type"]  = 'PAY'
        wcn["channel_type"]  = 'WX'

        return wcn




##############################################################
#                       支付宝支付接口                         #
#############################################################


@handler_define
class AliWebPayHandler(tornado.web.RequestHandler):

    #@login_required
    @api_define("AliWebPayHandler", r'/html/ali/pay', [
        Param('order_id', True, int, "str", "201907291342455810652881", u'order_id'),
        Param('good_name', True, int, "str", "xx商品", u'商品名称'),
    ], description=u"阿里支付宝网站支付", protocal="http")
    def get(self,x):
        #
        # 这里是阿里网站支付文档
        # https://docs.open.alipay.com/270/105898/
        #
        order_id = self.get_argument('order_id')
        good_name = self.get_argument('good_name')
        
        order = OrderInfo.objects.filter(order_id=order_id).first()

        pay = AliPayDoWebPay(
               order.order_id, good_name, order.amount
        )

        body = pay.getAlipayUrl()
        return self.finish(body)




@handler_define
class AliPayNoticeHandler(BaseHandler):

    
    @api_define("Play Url", r'/api/live/alipay/notice', [
    ], description=u"支付宝支付成功回调通知接口",)
    def post(self):

        #这里是回调文档
        #https://docs.open.alipay.com/270/105902/

        #这里是返回参数
        #"gmt_create=2019-08-16+16%3A49%3A15
        #&charset=utf-8&
        #seller_email=class17111%40163.com&
        #subject=%E9%AB%98%E7%AB%AF%E8%AF%BE%E7%A8%8B
        #&sign=hInbUcoY8I%2FN5tq3AV8BVOq%2B6GorG8K8wPKFUczOUa0rheKYHUpjEQ1vM7aCRMUmxx1fBpDmBVPJ7Oq79UzyU1PG8hfdgzWRVdHmPLS7CzNBz5jx4FSmCUrrUSgNksiyNT2XiZwoJiUlb7qqeSeMCXcseYN4Inxincyczofs5MBaVX3VmpoP3Uxf4ZUQrAVGN1N2jPoBIQRA6SY8G%2B1Yr1Ff6n9MBliqWOBf1LC72lmv3or%2FZhWXXNLlEkMNNXowjWQP6ZZ1cSlDucK4TvQD9G1H6ImcNZUb70OWFuLmUtIdDlhmhqTxNLEcaKerr%2BqRAcsk614tXCfuBkfy%2B37ofQ%3D%3D&
        #body=%E9%AB%98%E7%AB%AF%E8%AF%BE%E7%A8%8B&
        #buyer_id=2088602148566473&
        #invoice_amount=0.01&
        #notify_id=2019081600222164916066470592278958&
        #fund_bill_list=%5B%7B%22
        #amount%22%3A%220.01%22%2C%22
        #fundChannel%22%3A%22
        #ALIPAYACCOUNT%22%7D%5D&
        #notify_type=trade_status_sync&
        #trade_status=TRADE_SUCCESS&
        #receipt_amount=0.01&
        #app_id=2019061965635427&
        #buyer_pay_amount=0.01&
        #sign_type=RSA2&seller_id=2088531403624516&
        #gmt_payment=2019-08-16+16%3A49%3A15&
        #notify_time=2019-08-16+16%3A49%3A16&version=1.0&
        #out_trade_no=201908161649015009575081&
        #total_amount=0.01&
        #trade_no=2019081622001466470526352576&
        #auth_app_id=2019061965635427&
        #buyer_logon_id=nul***%40qq.com&
        #point_amount=0.00


        app_id = self.arg('app_id')
        #数据库里的订单
        out_trade_no = self.arg('out_trade_no')
        #支付宝交易id
        trade_no = self.arg('trade_no')
        #买家号id
        buyer_id = self.arg('buyer_id')
        #卖家支付宝用户号   
        seller_id = self.arg('seller_id')
        #交易状态
        trade_status = self.arg('trade_status')
        #订单金额   
        total_amount = self.arg_float('total_amount')

        #支付渠道说明
        fund_bill_list = self.arg('fund_bill_list')

        if trade_status != "TRADE_SUCCESS":
            return self.write("FAILED")

        wcn = {}
        wcn["app_id"] = app_id
        wcn["transaction_id"] = out_trade_no
        wcn["channel_transaction_id"] = trade_no
        wcn["transaction_fee"] = total_amount * 100
        wcn["fee_type"] = ""
        wcn["seller_id"] = seller_id
        wcn["buyer_id"] = buyer_id
        wcn["transaction_type"]  = 'PAY'
        wcn["channel_type"]  = 'ALI'


        #这里将订单设置为已经回调成功
        OrderInfo.success(wcn)

        return self.write("success")









