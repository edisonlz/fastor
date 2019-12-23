# -*- coding: utf-8 -*-
"""
    beecloud.subscribe
    ~~~~~~~~~
    This module contains user API.
    :created by xuanzhui on 2017/7/12.
    :copyright (c) 2015 BeeCloud.
    :license: MIT, see LICENSE for more details.
"""


from beecloud.utils import attach_app_sign, get_rest_root_url, http_post, set_common_attr, \
    http_put, obj_to_quote_str, http_get, parse_dict_to_obj
from beecloud.entity import BCReqType, _TmpObject, BCResult, BCMerchantUser


def add_merchant_user(bc_app, buyer_id):
    """
    add merchant user
    :param bc_app: beecloud.entity.BCApp
    :param buyer_id: merchant unique user id, can be used as buyer id for bill
    :return: beecloud.entity.BCResult
    """
    req_param = _TmpObject()
    req_param.buyer_id = buyer_id
    attach_app_sign(req_param, BCReqType.PAY, bc_app)

    url = get_rest_root_url() + 'rest/user'

    tmp_resp = http_post(url, req_param, bc_app.timeout)

    # if err encountered, [0] equals 0
    if not tmp_resp[0]:
        return tmp_resp[1]

    # [1] contains result dict
    resp_dict = tmp_resp[1]

    bc_result = BCResult()
    set_common_attr(resp_dict, bc_result)

    return bc_result


def batch_add_merchant_users(bc_app, merchant, buyer_ids):
    """
    add merchant user
    :param bc_app: beecloud.entity.BCApp
    :param merchant: merchant account
    :param buyer_ids: merchant unique user id list
    :return: beecloud.entity.BCResult
    """
    req_param = _TmpObject()
    req_param.email = merchant
    req_param.buyer_ids = buyer_ids
    attach_app_sign(req_param, BCReqType.PAY, bc_app)

    url = get_rest_root_url() + 'rest/users'

    tmp_resp = http_post(url, req_param, bc_app.timeout)

    # if err encountered, [0] equals 0
    if not tmp_resp[0]:
        return tmp_resp[1]

    # [1] contains result dict
    resp_dict = tmp_resp[1]

    bc_result = BCResult()
    set_common_attr(resp_dict, bc_result)

    return bc_result


def query_merchant_users(bc_app, merchant=None, start_time=None, end_time=None):
    """
    query merchant users
    :param bc_app: beecloud.entity.BCApp
    :param merchant: merchant account, if not passed, only users associated with app will be returned
    :param start_time: if passed, only users registered after it will be returned
    :param end_time: if passed, only users registered before it will be returned
    :return: result contains beecloud.entity.MerchantUser list
    """
    req_param = _TmpObject()
    if merchant:
        req_param.email = merchant

    if start_time:
        req_param.start_time = start_time

    if end_time:
        req_param.end_time = end_time

    attach_app_sign(req_param, BCReqType.QUERY, bc_app)

    url = get_rest_root_url() + 'rest/users?para=' + obj_to_quote_str(req_param)

    tmp_resp = http_get(url, bc_app.timeout)
    # if err encountered, [0] equals 0
    if not tmp_resp[0]:
        return tmp_resp[1]

    # [1] contains result dict
    resp_dict = tmp_resp[1]
    bc_result = BCResult()
    set_common_attr(resp_dict, bc_result)

    if not bc_result.result_code:
        user_dict_arr = resp_dict.get('users')
        class_name = BCMerchantUser

        users = []
        if user_dict_arr:
            users = [parse_dict_to_obj(user_dict, class_name) for user_dict in user_dict_arr]

        bc_result.users = users

    return bc_result


def attach_buyer_history_bills(bc_app, bill_info):
    """
    query merchant users
    :param bc_app: beecloud.entity.BCApp
    :param bill_info: {buyer_id: [bill_no...]...} dict, key is buyer id,
                        value is bill number list that belong to the buyer
    :return: result contains failed_bills, which indicates the bills that fail to connect to the buyer,
                failed_bills is also dict like bill_info
    """
    req_param = _TmpObject()
    req_param.bill_info = bill_info
    attach_app_sign(req_param, BCReqType.QUERY, bc_app)

    url = get_rest_root_url() + 'rest/history_bills'

    tmp_resp = http_put(url, req_param, bc_app.timeout)

    # if err encountered, [0] equals 0
    if not tmp_resp[0]:
        return tmp_resp[1]

    # [1] contains result dict
    resp_dict = tmp_resp[1]

    bc_result = BCResult()
    set_common_attr(resp_dict, bc_result)
    if resp_dict.get('failed_bills'):
        bc_result.failed_bills = resp_dict.get('failed_bills')

    return bc_result
