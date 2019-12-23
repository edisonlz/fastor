# -*- coding: utf-8 -*-
"""
    beecloud.utils
    ~~~~~~~~~
    This module contains common utils.
    :created by xuanzhui on 2015/12/24.
    :copyright (c) 2015 BeeCloud.
    :license: MIT, see LICENSE for more details.
"""

from beecloud.entity import BCResult, BCReqType, _TmpObject
from beecloud import BEECLOUD_API_HOST, BEECLOUD_RESTFUL_VERSION, NETWORK_ERROR_CODE, NETWORK_ERROR_NAME, \
    NOT_SUPPORTED_CODE, NOT_SUPPORTED_NAME
import random
import datetime
import requests
import requests.exceptions
import sys
import hashlib
import time
import json

if sys.version_info[0] == 3:   # if 3
    import urllib.parse
    long = int
else:
    import urllib

URL_REQ_SUCC = 1
URL_REQ_FAIL = 0


def get_rest_root_url():
    return BEECLOUD_API_HOST + BEECLOUD_RESTFUL_VERSION


def obj_to_dict(obj):
    if not obj:
        return None

    return {k: v for (k, v) in obj.__dict__.items() if v is not None}


def order_num_on_datetime():
    # py2 %f 后三位在win经常为0
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3:]


def _http_req_with_params(url, obj, method='POST', timeout=None):
    if type(obj) is not dict:
        req_param = obj_to_dict(obj)
    else:
        req_param = obj

    try:
        if method == 'POST':
            http_resp = requests.post(url, json=req_param, timeout=timeout)
        elif method == 'PUT':
            http_resp = requests.put(url, json=req_param, timeout=timeout)
        else:
            raise ValueError('method [{:s}] is not supported'.format(method))
    except requests.exceptions.ConnectionError:
        return _deal_with_conn_error()

    if http_resp.status_code == 200 or (400 <= http_resp.status_code < 500):
        http_resp.encoding = 'UTF-8'
        try:
            result_json = http_resp.json()
        except ValueError:
            return _deal_with_invalid_resp(http_resp)
        else:
            return URL_REQ_SUCC, result_json
    else:
        return _deal_with_invalid_resp(http_resp)


def http_post(url, obj, timeout=None):
    """
    http post request
    :param url: post url
    :param obj: post param
    :param timeout: refer to desc of BCApp timeout
    :return: tuple, [0] indicate the result code: 0 means failure, 1 means success; [1] is beecloud.entity.BCResult
    """
    return _http_req_with_params(url, obj, timeout=timeout)


def http_put(url, obj, timeout=None):
    """
    http put request
    :param url: put url
    :param obj: put param
    :param timeout: refer to desc of BCApp timeout
    :return: tuple, [0] indicate the result code: 0 means failure, 1 means success; [1] is beecloud.entity.BCResult
    """
    return _http_req_with_params(url, obj, method='PUT', timeout=timeout)


def obj_to_quote_str(param_obj):
    str_tmp = json.dumps(obj_to_dict(param_obj))
    if sys.version_info[0] == 3:
        return urllib.parse.quote_plus(str_tmp)
    else:
        return urllib.quote_plus(str_tmp)


def parse_dict_to_obj(dict_data, class_name):
    obj = class_name()

    if dict_data:
        for k, v in dict_data.items():
            obj.__dict__[k] = v

    return obj


# result would be key1=val1&key2=val2, value would utf8 encode
def compatible_urlencode(pair_data):
    dict_data = pair_data
    if type(pair_data) is not dict:
        dict_data = obj_to_dict(pair_data)

    if sys.version_info[0] == 3:
        return urllib.parse.urlencode(dict_data)
    else:
        return urllib.urlencode(dict_data)


def http_get(url, timeout=None, params=None):
    """
    http get request
    :param url: url with params concatenated(params should not set in this case) or not
    :param timeout: refer to desc of BCApp timeout
    :param params: dict type, attach at the end of url, ? will be auto added
    :return: tuple, [0] indicate the result code: 0 means failure, 1 means success; [1] is beecloud.entity.BCResult
    """
    try:
        http_resp = requests.get(url, params=params, timeout=timeout)
    except requests.exceptions.ConnectionError:
        return _deal_with_conn_error()

    if http_resp.status_code == 200 or (400 <= http_resp.status_code < 500):
        http_resp.encoding = 'UTF-8'
        try:
            result_json = http_resp.json()
        except ValueError:
            return _deal_with_invalid_resp(http_resp)
        else:
            return URL_REQ_SUCC, result_json
    else:
        return _deal_with_invalid_resp(http_resp)


def http_del(url, timeout=None):
    """
    http delete request
    :param url: url with params concatenated
    :param timeout: refer to desc of BCApp timeout
    :return: tuple, [0] indicate the result code: 0 means failure, 1 means success; [1] is beecloud.entity.BCResult
    """
    try:
        http_resp = requests.delete(url, timeout=timeout)
    except requests.exceptions.ConnectionError:
        return _deal_with_conn_error()

    if http_resp.status_code == 200 or (400 <= http_resp.status_code < 500):
        http_resp.encoding = 'UTF-8'
        try:
            result_json = http_resp.json()
        except ValueError:
            return _deal_with_invalid_resp(http_resp)
        else:
            return URL_REQ_SUCC, result_json
    else:
        return _deal_with_invalid_resp(http_resp)


def _deal_with_conn_error():
    resp = BCResult()
    resp.result_code = NETWORK_ERROR_CODE
    resp.result_msg = NETWORK_ERROR_NAME
    resp.err_detail = 'ConnectionError: normally caused by timeout'
    return URL_REQ_FAIL, resp


def _deal_with_invalid_resp(http_resp):
    resp = BCResult()
    resp.result_code = NETWORK_ERROR_CODE
    resp.result_msg = http_resp.status_code
    resp.err_detail = http_resp.reason
    return URL_REQ_FAIL, resp


def set_common_attr(resp_dict, bc_result):
    bc_result.result_code = resp_dict.get('result_code')
    bc_result.result_msg = resp_dict.get('result_msg')
    bc_result.err_detail = resp_dict.get('err_detail')


def report_not_supported_err(method_name):
    err_result = BCResult()
    err_result.result_code = NOT_SUPPORTED_CODE
    err_result.result_msg = NOT_SUPPORTED_NAME
    err_result.err_detail = u'[{:s}] does NOT support test mode currently!'.format(method_name)
    return err_result


def local_timestamp_since_epoch(dt):
    """
    :param dt: datetime which should be set with system local timezone
    :return: milliseconds from epoch 1970-01-01 00:00:00 UTC
    """
    epoch = datetime.datetime.utcfromtimestamp(0)
    # e.g. Beijing timezone is 8 hours faster than UTC
    delta = dt - epoch - (datetime.datetime.now() - datetime.datetime.utcnow())
    return long((delta.days * 86400 + delta.seconds) * 1000 + delta.microseconds / 1000)


def attach_app_sign(req_param, req_type, bc_app):
    # BC APP的唯一标识
    if not bc_app.app_id:
        raise ValueError('app id is not set')

    setattr(req_param, 'app_id', bc_app.app_id)

    # 签名生成时间
    # 时间戳, 毫秒数
    timestamp = long(time.time()*1000)
    setattr(req_param, 'timestamp', timestamp)

    # 加密签名
    # 算法: md5(app_id+timestamp+secret), 32位16进制格式, 不区分大小写
    if bc_app.is_test_mode:
        if not bc_app.test_secret:
            raise ValueError('test secret is not set')
        else:
            app_sign = hashlib.md5((bc_app.app_id + str(timestamp) +
                                    bc_app.test_secret).encode('UTF-8')).hexdigest()
    else:
        if req_type in (BCReqType.REFUND, BCReqType.TRANSFER):
            if not bc_app.master_secret:
                raise ValueError('master secret is not set')
            else:
                app_sign = hashlib.md5((bc_app.app_id + str(timestamp) +
                                        bc_app.master_secret).encode('UTF-8')).hexdigest()
        else:
            if not bc_app.app_secret:
                raise ValueError('app secret is not set')
            else:
                app_sign = hashlib.md5((bc_app.app_id + str(timestamp) +
                                        bc_app.app_secret).encode('UTF-8')).hexdigest()

    setattr(req_param, 'app_sign', app_sign)


# ======== BeeCloud restful object CURD start ========

def rest_add_object(bc_app, url, obj, json_obj_name, obj_type):
    """
    :param bc_app: used to attach app sign
    :param url: used to post request
    :param obj: like beecloud.entity.BCPlan
    :param json_obj_name: object json name returned when successful, like 'plan'
    :param obj_type: like beecloud.entity.BCPlan
    :return: beecloud.entity.BCResult
    """
    attach_app_sign(obj, BCReqType.PAY, bc_app)
    tmp_resp = http_post(url, obj, bc_app.timeout)

    # if err encountered, [0] equals 0
    if not tmp_resp[0]:
        return tmp_resp[1]

    # [1] contains result dict
    resp_dict = tmp_resp[1]

    bc_result = BCResult()
    set_common_attr(resp_dict, bc_result)
    if not bc_result.result_code:
        setattr(bc_result, json_obj_name, parse_dict_to_obj(resp_dict.get(json_obj_name), obj_type))

    return bc_result


def rest_update_object(bc_app, url, obj_id, **kwargs):
    """
    :param bc_app: used to attach app sign
    :param url: used to post request
    :param obj_id: object id
    :param kwargs: optional key/value pairs arguments
    :return: beecloud.entity.BCResult
    """
    tmp_obj = _TmpObject()
    if kwargs:
        for k, v in kwargs.items():
            if v:
                setattr(tmp_obj, k, v)

    attach_app_sign(tmp_obj, BCReqType.PAY, bc_app)
    tmp_resp = http_put(url + '/' + obj_id, tmp_obj, bc_app.timeout)

    # if err encountered, [0] equals 0
    if not tmp_resp[0]:
        return tmp_resp[1]

    # [1] contains result dict
    resp_dict = tmp_resp[1]

    bc_result = BCResult()
    set_common_attr(resp_dict, bc_result)

    if not bc_result.result_code:
        bc_result.id = resp_dict.get('id')

    return bc_result


def rest_delete_object(bc_app, url, obj_id, **kwargs):
    """
    :param bc_app: used to attach app sign
    :param url: used to post request
    :param obj_id: object id
    :param kwargs: optional key/value pairs arguments
    :return: beecloud.entity.BCResult
    """
    tmp_obj = _TmpObject()
    if kwargs:
        for k, v in kwargs.items():
            if v:
                setattr(tmp_obj, k, v)

    attach_app_sign(tmp_obj, BCReqType.PAY, bc_app)
    req_url = url + '/' + obj_id + '?' + compatible_urlencode(tmp_obj)
    tmp_resp = http_del(req_url, bc_app.timeout)

    # if err encountered, [0] equals 0
    if not tmp_resp[0]:
        return tmp_resp[1]

    # [1] contains result dict
    resp_dict = tmp_resp[1]

    bc_result = BCResult()
    set_common_attr(resp_dict, bc_result)

    if not bc_result.result_code:
        bc_result.id = resp_dict.get("id")

    return bc_result


def rest_query_objects(bc_app, url, query_param, json_obj_name, object_type, para_query_mode=False):
    """
    query object list by conditions
    :param bc_app: used to attach app sign
    :param url: do NOT contain params at the end
    :param query_param: query condition object beecloud.entity.BCQueryCriteria,
                        more specific conditions can be attached to it
    :param json_obj_name: like 'plans' for plan list query
    :param object_type: object type like beecloud.entity.BCPlan
    :param para_query_mode: true if query string is para={}, else k1=v1&k2=v2
    :return: beecloud.entity.BCResult
    """
    if not query_param:
        query_param = _TmpObject()

    attach_app_sign(query_param, BCReqType.QUERY, bc_app)

    if para_query_mode:
        url = url + '?para=' + obj_to_quote_str(query_param)
        tmp_resp = http_get(url, bc_app.timeout)
    else:
        tmp_resp = http_get(url, bc_app.timeout, obj_to_dict(query_param))

    # if err encountered, [0] equals 0
    if not tmp_resp[0]:
        return tmp_resp[1]

    # [1] contains result dict
    resp_dict = tmp_resp[1]
    bc_result = BCResult()
    set_common_attr(resp_dict, bc_result)
    if not bc_result.result_code:
        # if only query count
        if hasattr(query_param, 'count_only') and query_param.count_only:
            bc_result.total_count = resp_dict.get('total_count')
        else:
            if resp_dict.get(json_obj_name):
                setattr(bc_result, json_obj_name, [parse_dict_to_obj(dict_data, object_type)
                                                   for dict_data in resp_dict.get(json_obj_name) if dict_data])
            else:
                setattr(bc_result, json_obj_name, [])

    return bc_result


def rest_query_object_by_id(bc_app, url, obj_id, json_obj_name, object_type, para_query_mode=False):
    """
    query object by id
    :param bc_app: used to attach app sign
    :param url: do NOT contain params at the end
    :param obj_id: object id
    :param json_obj_name: like 'plan' for plan query
    :param object_type: object type like beecloud.entity.BCPlan
    :param para_query_mode: true if query string is para={}, else k1=v1&k2=v2
    :return: beecloud.entity.BCResult
    """
    query_param = _TmpObject()
    attach_app_sign(query_param, BCReqType.QUERY, bc_app)

    if para_query_mode:
        url = url + '/' + obj_id + '?para=' + obj_to_quote_str(query_param)
        tmp_resp = http_get(url, bc_app.timeout)
    else:
        tmp_resp = http_get(url + '/' + obj_id, bc_app.timeout, obj_to_dict(query_param))

    # if err encountered, [0] equals 0
    if not tmp_resp[0]:
        return tmp_resp[1]

    # [1] contains result dict
    resp_dict = tmp_resp[1]
    bc_result = BCResult()
    set_common_attr(resp_dict, bc_result)

    if not bc_result.result_code:
        setattr(bc_result, json_obj_name, parse_dict_to_obj(resp_dict.get(json_obj_name), object_type))

    return bc_result

# ======== BeeCloud restful object CURD end ========


def send_sms_passcode(bc_app, phone):
    """
    send sms verify code
    :param bc_app: beecloud.entity.BCApp
    :param phone: phone number passcode sent to
    :return: beecloud.entity.BCResult, which contains sms_id
    """
    tmp_obj = _TmpObject()
    tmp_obj.phone = phone
    attach_app_sign(tmp_obj, BCReqType.PAY, bc_app)
    tmp_resp = http_post(get_rest_root_url() + "sms", tmp_obj, bc_app.timeout)

    # if err encountered, [0] equals 0
    if not tmp_resp[0]:
        return tmp_resp[1]

    # [1] contains result dict
    resp_dict = tmp_resp[1]

    bc_result = BCResult()
    set_common_attr(resp_dict, bc_result)

    if not bc_result.result_code:
        bc_result.sms_id = resp_dict.get('sms_id')

    return bc_result


# 鉴权
def verify_card_factors(bc_app, name, id_no, card_no=None, mobile=None):
    """
    verify bank card factors
    :param bc_app: beecloud.entity.BCApp
    :param name: id card name
    :param id_no: id card number
    :param card_no: bank card number
    :param mobile: mobile bind to bank card
    :return:
    """
    tmp_obj = _TmpObject()
    tmp_obj.name = name
    tmp_obj.id_no = id_no
    tmp_obj.card_no = card_no
    tmp_obj.mobile = mobile

    attach_app_sign(tmp_obj, BCReqType.PAY, bc_app)
    tmp_resp = http_post(get_rest_root_url() + "auth", tmp_obj, bc_app.timeout)

    # if err encountered, [0] equals 0
    if not tmp_resp[0]:
        return tmp_resp[1]

    # [1] contains result dict
    resp_dict = tmp_resp[1]

    bc_result = BCResult()
    set_common_attr(resp_dict, bc_result)

    if not bc_result.result_code:
        bc_result.card_id = resp_dict.get('card_id')
        bc_result.auth_result = resp_dict.get('auth_result')
        bc_result.auth_msg = resp_dict.get('auth_msg')

    return bc_result


wx_oauth_url_basic = 'https://open.weixin.qq.com/connect/oauth2/authorize?'
wx_sns_token_url_basic = 'https://api.weixin.qq.com/sns/oauth2/access_token?'


# 获取code 的url生成规则，redirect_url是微信用户登录后的回调页面，将会有code的返回
def fetch_code(wx_app_id, redirect_url):
    code_data = {}
    code_data['appid'] = wx_app_id
    code_data['redirect_uri'] = redirect_url
    code_data['response_type'] = 'code'
    code_data['scope'] = 'snsapi_base'
    code_data['state'] = 'STATE#wechat_redirect'
    if sys.version_info[0] == 3:
        params = urllib.parse.urlencode(code_data)
    else:
        params = urllib.urlencode(code_data)
    return wx_oauth_url_basic + params


# 获取openid的url生成方法
def create_fetch_open_id_url(wx_app_id, wx_app_secret, code):
    fetch_data = {}
    fetch_data['appid'] = wx_app_id
    fetch_data['secret'] = wx_app_secret
    fetch_data['grant_type'] = 'authorization_code'
    fetch_data['code'] = code
    if sys.version_info[0] == 3:
        params = urllib.parse.urlencode(fetch_data)
    else:
        params = urllib.urlencode(fetch_data)
    return wx_sns_token_url_basic + params


def fetch_open_id(wx_app_id, wx_app_secret, code):
    url = create_fetch_open_id_url(wx_app_id, wx_app_secret, code)
    http_response = requests.get(url)
    if http_response.status_code == 200:
        resp_dict = http_response.json()
        return resp_dict.get('openid')
    else:
        return ''
