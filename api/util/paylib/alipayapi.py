# -*- coding: utf-8 -*-
import urllib
import hashlib
import urllib2
import logging
import os,sys
import base64
from datetime import datetime
import json
import logging
import urllib



class AliPayConfig(object):
    """
    支付宝 公共配置
    """
    APP_ID = '' #appid
    precreate_GATEWAY="https://openapi.alipay.com/gateway.do?"
    SIGN_TYPE = "RSA"
    INPUT_CHARSTE = "utf-8"
    KEY = '' #支付宝密钥
    SELLER_ID = ""#支付宝账号
    PARTNER = "" #合伙人id
    ALI_SERVICE_PATH = "https://mapi.alipay.com/gateway.do"
    NOTIFY_URL = "" #支付成功回调地址





class AliPayBase(object):
    """
    支付宝api 基类
    """
    def get_sign(self, para_str, sign_type="RSA2"):
        #对参数排序

        import OpenSSL
        ###############################################
        #            这里需要支付宝支付私钥文件           #
        ###############################################
        root = os.path.realpath(os.path.dirname(__file__))
        ali_private_path = os.path.join(root, "ali_private2048.txt")

        private_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, open(ali_private_path).read())
 
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8') #这三句：解决签名方法编码报错

        sign = base64.encodestring(OpenSSL.crypto.sign(private_key, para_str, 'sha256'))
        return sign

     


    def create_request_data(self):
        raise NotImplementedError


    def post_data(self):
        """
        标准post 可以自己实现 ,需要定义 self.create_request_data()
        """
        data = self.create_request_data()
        try:
            result = urllib2.urlopen(
                AliPayConfig.ALI_SERVICE_PATH,
                data=urllib.urlencode(data)).read()
        except Exception, e:
            logging.error("post data error %s %s" % (data['service'],e))

        return result

    def params_to_query(self,params):
        """
        生成需要签名的字符串
        :param params:
        :return:
        """
        """
        :param params:
        :return:
        """
        query = ""
        dict_items = {}
        for key, value in params.items():
            if isinstance(value, dict) == True:
                dict_items[key] = value
                params[key] = "%s"
        all_str = ''
        for key in sorted(params.keys()): #把参数按key值排序：这是支付宝下单请求的参数格式规定
            all_str = all_str + '%s=%s&' % (key, params[key])
        all_str = all_str.rstrip('&')
        biz_content_dict = dict_items['biz_content']
        content_str = ''
        for key in sorted(biz_content_dict.keys()):
            if isinstance(biz_content_dict[key], basestring) == True:
                content_str = content_str + '"%s":"%s",' % (key, biz_content_dict[key])
            else:
                content_str = content_str + '"%s":%s,' % (key, biz_content_dict[key])
        content_str = content_str.rstrip(',')
        content_str = '{' + content_str + '}'
        query = all_str % content_str
        return query





class AliPayDoWebPay(AliPayBase):
    """
    支付宝 下单接口封装
    doc https://docs.open.alipay.com/270/105900/
    """

    def __init__(self, orderid, goodsName, goodsPrice):

        
        self.notify_url = AliPayConfig.NOTIFY_URL
        self.precreate_GATEWAY = "https://openapi.alipay.com/gateway.do?"
        self.orderid = orderid
        self.goodsName = goodsName
        self.goodsPrice = goodsPrice

    

    #获取二维码url
    def getAlipayUrl(self):
        # 构建公共参数
        import requests

        params = {}
        params['method'] = 'alipay.trade.page.pay'
        params['version'] = '1.0'
        params['app_id'] = AliPayConfig.APP_ID
        params['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        params['charset'] =  'utf-8'
        params['notify_url'] = self.notify_url
        params['sign_type'] = 'RSA2'

        # 构建订单参数
        biz_content = {}
        biz_content['out_trade_no'] = self.orderid  # 订单号
        biz_content['qr_pay_mode'] = "2"
        biz_content['subject'] = self.goodsName  #商品名
        biz_content['product_code'] = 'FAST_INSTANT_TRADE_PAY'
        biz_content['total_amount'] = self.goodsPrice  # 价格
        params['biz_content'] = biz_content

        #由参数，生成签名，并且拼接得到下单参数字符串
        encode_params = self.make_payment_request(params)

        #下单
        url = self.precreate_GATEWAY + encode_params
        response = requests.get(url)

        #提取下单响应
        body = response.text
        #解析下单响应json字符串
        return body
        

    #1：生成下单请求参数字符串
    def make_payment_request(self,params_dict):
        """
        构造支付请求参数
        :param params_dict:
        :return:
        """
        query_str = self.params_to_query(params_dict)  # 拼接参数字符串
        sign = self.make_sign(query_str)  # 生成签名
        sign = urllib.quote(sign, safe='')  #解决中文参数编码问题
        res = "%s&sign=%s" % (query_str, sign)
        return res



    def make_sign(self,para_str):
        """
        生成签名
        :param message:
        :return:
        """
        import OpenSSL

        ###############################################
        #            这里需要支付宝支付私钥文件           #
        ###############################################
        root = os.path.realpath(os.path.dirname(__file__))
        ali_private_path = os.path.join(root, "ali_private2048.txt")

        private_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, open(ali_private_path).read())
 
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8') #这三句：解决签名方法编码报错

        sign = base64.encodestring(OpenSSL.crypto.sign(private_key, para_str, 'sha256'))
        return sign







class AliPayDoAppPay(AliPayBase):
    """
    支付宝 下单接口封装
    doc https://docs.open.alipay.com/270/105900/
    """

    def __init__(self, orderid, goodsName, goodsPrice):

       
        self.notify_url = AliPayConfig.NOTIFY_URL     
        self.precreate_GATEWAY = "https://openapi.alipay.com/gateway.do?"
        self.orderid = orderid
        self.goodsName = goodsName
        self.goodsPrice = goodsPrice

    

    #获取二维码url
    def do_pay_params(self):
        # 构建公共参数
        import requests

        params = {}
        params['method'] = 'alipay.trade.app.pay'
        params['version'] = '1.0'
        params['app_id'] = AliPayConfig.APP_ID
        params['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        params['charset'] =  'utf-8'
        params['notify_url'] = self.notify_url
        params['sign_type'] = 'RSA2'
        params['format'] = 'json'
        

        # 构建订单参数
        biz_content = {}
        biz_content["timeout_express"] = "30m"
        biz_content['out_trade_no'] = self.orderid  # 订单号
        biz_content['subject'] = self.goodsName  #商品名
        biz_content['body'] = self.goodsName  #商品名
        biz_content['product_code'] = 'QUICK_MSECURITY_PAY'
        biz_content['total_amount'] = self.goodsPrice  # 价格
        params['biz_content'] = biz_content

        encode_params = self.make_payment_request(params)

        return encode_params

     
        

    #1：生成下单请求参数字符串
    def make_payment_request(self,params_dict):
        """
        构造支付请求参数
        :param params_dict:
        :return:
        """
        import copy
        query_str = self.params_to_query(copy.deepcopy(params_dict),)  # 拼接参数字符串
        sign = self.make_sign(query_str)  # 生成签名
        
        query_str = self.params_to_query(copy.deepcopy(params_dict),quote=True)
        res = "%s&sign=%s" % (query_str, urllib.quote(str(sign)))

        return res



    def params_to_query(self,params,quote=False):
        """
        生成需要签名的字符串
        :param params:
        :return:
        """
        """
        :param params:
        :return:
        """
        query = ""
        dict_items = {}
        for key, value in params.items():
            if isinstance(value, dict) == True:
                dict_items[key] = value
                params[key] = "%s"

        all_str = ''
        for key in sorted(params.keys()): #把参数按key值排序：这是支付宝下单请求的参数格式规定
            if quote:
                if key not in dict_items:
                    all_str = all_str + '%s=%s&' % (key, urllib.quote(params[key]))
                else:
                    all_str = all_str + '%s=%s&' % (key, params[key])

            else:
                all_str = all_str + '%s=%s&' % (key, params[key])

        all_str = all_str.rstrip('&')
        biz_content_dict = dict_items['biz_content']
        content_str = ''
        for key in sorted(biz_content_dict.keys()):
            if isinstance(biz_content_dict[key], basestring) == True:
                content_str = content_str + '"%s":"%s",' % (key, biz_content_dict[key])
            else:
                content_str = content_str + '"%s":%s,' % (key, biz_content_dict[key])

        content_str = content_str.rstrip(',')
        content_str = '{' + content_str + '}'
        if quote:
            query = all_str.replace("%s",urllib.quote(str(content_str)))
        else:
            query = all_str % content_str

        return query


    def make_sign(self,para_str):
        """
        生成签名
        :param message:
        :return:
        """
        import OpenSSL

        root = os.path.realpath(os.path.dirname(__file__))
        ali_private_path = os.path.join(root, "ali_private2048.txt")
        # print ali_private_path

        #把私钥存到一个文件里，加载出来【尝试过用rsa模块的方法加载私钥字符串，会报格式错误。查看源码得知，需要从文件流加载】
        private_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, open(ali_private_path).read())
 
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8') #这三句：解决签名方法编码报错

        sign = base64.encodestring(OpenSSL.crypto.sign(private_key, para_str, 'sha256'))
        return sign






class AliPayVerifyNotice(AliPayBase):
    """
    支付宝通知结果验证
    """
    def __init__(self, notice_params):
        self.service = 'notify_verify'
        self.notice_params = notice_params


    def verify_sign(self):

        query_str = self.params_to_query(notice_params)
        server_sign = self.get_sign(query_str)
        client_sign = self.notice_params.get("sign")

        return server_sign == client_sign





