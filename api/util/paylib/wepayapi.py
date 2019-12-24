# -*- coding: utf-8 -*-
import hashlib
import urllib2
import random
import string
import time
import copy
import xml.etree.ElementTree as ET
import logging


class WePayConfig(object):

    MCHID = "" #商户号
    APPID = "" #APPID
    KEY = "" #微信API密钥
    NOTIFY_URL = "" #支付成功回调地址



class WePayBase(object):
    """
    微信支付基类
    """


    def dict_to_xml(self, param_map):
        """array转xml"""
        xml = ["<xml>"]
        for k, v in param_map.iteritems():
            if v.isdigit():
                xml.append("<{0}>{1}</{0}>".format(k, v))
            else:
                xml.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))
        xml.append("</xml>")
        return "".join(xml)


    def xml_to_dict(self, xml):
        data = {}
        root = ET.fromstring(xml)
        for child in root:
            value = child.text
            data[child.tag] = value
        return data


    def get_sign(self, param_map):
        """生成签名"""
        sort_param = sorted(
            [(key, unicode(value).encode('utf-8')) for key, value in param_map.iteritems()],
            key=lambda x: x[0]
        )
        content = '&'.join(['='.join(x) for x in sort_param])
        key =  WePayConfig.KEY

        sign_content = "{0}&key={1}".format(content, key)
        #print sign_content
        smd5 = hashlib.md5()
        #print sign_content
        smd5.update(sign_content)
        return smd5.hexdigest().upper()

    def random_str(self):
        content = string.lowercase + string.digits
        return ''.join(random.sample(content, 16))


class WePayDoPay(WePayBase):
    """
    微信下单接口
    """
    def __init__(self,  out_trade_no, total_fee, body='buy', subject='buy', payment_type="APP",ip="",openid='',application_id=1):
        
        self.url = "https://api.mch.weixin.qq.com/pay/unifiedorder"


        self.notify_url = WePayConfig.NOTIFY_URL
        self.out_trade_no = str(out_trade_no)
        self.subject = subject
        self.trade_type = payment_type
        self.total_fee = str(total_fee)
        self.body = body
        self.ip = ip
        self.prepay_id = ''
        self.xml = ''
        self.code_url = ''
        self.nonce_str = self.random_str()
        self.openid = openid


    def post_xml(self, second=30):
        data = urllib2.urlopen(
            self.url, self.create_xml(),
            timeout=second).read()

        return data



    def create_xml(self):
        """生成接口参数xml"""

        web_wx_appid = WePayConfig.APPID
        web_wx_mchid = WePayConfig.MCHID

        param_map = {
            'appid': web_wx_appid,
            'mch_id': web_wx_mchid,
            'spbill_create_ip': self.ip,
            'nonce_str': self.nonce_str,
            'out_trade_no': self.out_trade_no,
            'body': self.body,
            'total_fee': self.total_fee,
            'notify_url': self.notify_url,
            'trade_type': self.trade_type
        }

        if self.openid:
            param_map['openid'] = self.openid


        param_map['sign'] = self.get_sign(param_map)
        self.xml = self.dict_to_xml(param_map)
        
        return self.xml


    def qr_code_xml(self,prepay_id):
        web_wx_appid = WePayConfig.APPID
        web_wx_mchid = WePayConfig.MCHID

        param_map = {
            "return_code":"SUCCESS",
            'appid': web_wx_appid,
            'mch_id': web_wx_mchid,
            'nonce_str': self.nonce_str,
            "prepay_id":prepay_id,
            "result_code":"SUCCESS",
        }

        param_map['sign'] = self.get_sign(param_map)
        xml = self.dict_to_xml(param_map)
        return xml



    def _get_prepay_id(self):
        """获取prepay_id"""

        result = self.xml_to_dict(self.post_xml())
        #print " * " * 20
        #print result
        result_code = result.get('result_code')
        err_code = result.get('err_code')
        if result_code != "SUCCESS":
            e = Exception()
            e.desc = result.get("return_msg","")
            e.message = result.get("return_msg","")
            logging.error(result)
            raise e

        self.prepay_id = result.get('prepay_id')
        self.nonce_str = result.get("nonce_str")
        self.code_url = result.get("code_url")
        return self.prepay_id



    def get_pay_params(self):
        web_wx_appid = WePayConfig.APPID
        web_wx_mchid = WePayConfig.MCHID

        prepay_id = self._get_prepay_id()
        param_map = {
            'prepayid': prepay_id,
            'appid': web_wx_appid,
            'partnerid': web_wx_mchid,
            'package': 'Sign=WXPay',
            'noncestr': self.nonce_str,
            'timestamp': str(int(time.time()))
        }

        sort_param = sorted(
            [(key, value)for key, value in param_map.iteritems()],
            key=lambda x: x[0]
        )

        sign = self.get_sign(param_map)


        param_map['prepay_id'] = prepay_id
        param_map['sign'] = sign

        return param_map


    def do_pay_params(self):
        web_wx_appid = WePayConfig.APPID
        web_wx_mchid = WePayConfig.MCHID

        prepay_id = self._get_prepay_id()
        param_map = {
            'prepayid': prepay_id,
            'appid': web_wx_appid,
            'partnerid': web_wx_mchid,
            'package': 'Sign=WXPay',
            'noncestr': self.nonce_str,
            'timestamp': str(int(time.time()))
        }

        sort_param = sorted(
            [(key, value)for key, value in param_map.iteritems()],
            key=lambda x: x[0]
        )

        sign = self.get_sign(param_map)

        pay_params = '&'.join(['='.join(x) for x in sort_param])
        pay_params +="&sign=" + sign


        data = {
            "prepay_id": prepay_id,
            'pay_params': pay_params
        }
        return data

    def verify_notice_sign(self,xml):
        """
        校验签名
        """
        root = xml
        param_map = {}
        sign = ""
        for child in root:
            if child.tag !="sign":
                param_map[child.tag] = child.text
            else:
                sign = child.text

        we_sign = self.get_sign(param_map)

        if sign == we_sign:
            return True
        else:
            return False




class WePayNotice(WePayBase):
    """响应型接口基类"""
    SUCCESS, FAIL = "SUCCESS", "FAIL"

    def __init__(self, xml_data):
        self.xml_data = xml_data
        self.recieve_param = self._format_params(
            xml_data=xml_data)

    def _format_params(self, xml_data):
        """将微信的请求xml转换成dict，以方便数据处理"""
        return self.xml_to_dict(xml=xml_data)

    def validate(self):
        """校验签名"""
        tmp = copy.deepcopy(self.recieve_param)
        del tmp['sign']
        sign = self.get_sign(tmp) #本地签名

        return self.recieve_param['sign'] == sign

    def return_data(self, data):
        """设置返回微信的xml数据"""
        return self.dict_to_xml(data)






