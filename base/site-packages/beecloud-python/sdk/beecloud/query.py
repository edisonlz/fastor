# -*- coding: utf-8 -*-
"""
    beecloud.query
    ~~~~~~~~~
    This module contains query API.
    :created by xuanzhui on 2015/12/24.
    :copyright (c) 2015 BeeCloud.
    :license: MIT, see LICENSE for more details.
"""

from beecloud.entity import BCResult, BCBill, BCRefund, BCReqType, BCPlan, BCSubscription, _TmpObject
from beecloud.utils import get_rest_root_url, http_get, obj_to_quote_str, set_common_attr, \
    report_not_supported_err, attach_app_sign, obj_to_dict, parse_dict_to_obj, rest_query_objects,\
    rest_query_object_by_id, http_post


class _OrderType:
    BILL = 0
    REFUND = 1


class BCQuery:
    def __init__(self):
        self.bc_app = None

    def register_app(self, bc_app):
        """
        register app, which is mandatory before calling other API
        :param bc_app: beecloud.entity.self.bc_app
        """
        self.bc_app = bc_app
    
    def _query_bills_url(self):
        if self.bc_app.is_test_mode:
            return get_rest_root_url() + 'rest/sandbox/bills'
        else:
            return get_rest_root_url() + 'rest/bills'

    def _query_refunds_url(self):
        return get_rest_root_url() + 'rest/refunds'

    def _query_bill_url(self):
        if self.bc_app.is_test_mode:
            return get_rest_root_url() + 'rest/sandbox/bill'
        else:
            return get_rest_root_url() + 'rest/bill'

    def _query_refund_url(self):
        return get_rest_root_url() + 'rest/refund'

    def _query_plan_url(self):
        return get_rest_root_url() + 'plan'

    def _query_subscription_url(self):
        return get_rest_root_url() + 'subscription'

    def _query_orders(self, query_params, query_type):
        if query_type == _OrderType.BILL:
            if query_params.refund_no:
                raise ValueError('refund_no should NOT be used to query bills')
            if query_params.need_approval:
                raise ValueError('need_approval should NOT be used to query bills')
            partial_url = self._query_bills_url()
        elif query_type == _OrderType.REFUND:
            if query_params.spay_result:
                raise ValueError('spay_result should NOT be used to query refunds')
            partial_url = self._query_refunds_url()
        else:
            return

        if not query_params:
            query_params = _TmpObject()

        attach_app_sign(query_params, BCReqType.QUERY, self.bc_app)
        url = partial_url + '?para=' + obj_to_quote_str(query_params)

        tmp_resp = http_get(url, self.bc_app.timeout)
        # if err encountered, [0] equals 0
        if not tmp_resp[0]:
            return tmp_resp[1]

        # [1] contains result dict
        resp_dict = tmp_resp[1]
        bc_result = BCResult()
        set_common_attr(resp_dict, bc_result)

        if not bc_result.result_code:
            if query_type == _OrderType.BILL:
                order_dict_arr = resp_dict.get('bills')
                class_name = BCBill
            else:
                order_dict_arr = resp_dict.get('refunds')
                class_name = BCRefund

            orders = []
            if order_dict_arr:
                orders = [parse_dict_to_obj(order_dict, class_name)
                          for order_dict in order_dict_arr]

            bc_result.count = len(orders)

            if query_type == _OrderType.BILL:
                bc_result.bills = orders
            else:
                bc_result.refunds = orders

        return bc_result

    def query_bills(self, query_params=None):
        """
        query bills API
        refer to https://beecloud.cn/doc/?index=rest-api #5
        result contains a list(bills), its items are beecloud.entity.BCBill
        :param query_params: beecloud.entity.BCQueryReqParams
        :return: beecloud.entity.BCResult
        """
        return self._query_orders(query_params, _OrderType.BILL)

    def query_refunds(self, query_params=None):
        """
        query refunds API
        refer to https://beecloud.cn/doc/?index=rest-api #7
        result contains a list(refunds), its items are beecloud.entity.BCRefund
        :param query_params: beecloud.entity.BCQueryReqParams
        :return: beecloud.entity.BCResult
        """
        if self.bc_app.is_test_mode:
            return report_not_supported_err('query_refunds')
        return self._query_orders(query_params, _OrderType.REFUND)

    def _query_orders_count(self, query_params, query_type):
        if query_params.need_detail or query_params.skip or query_params.limit:
            raise ValueError('need_detail or skip or limit should NOT be used to query order count')

        if query_type == _OrderType.BILL:
            if query_params.refund_no:
                raise ValueError('refund_no should NOT be used to query bills')
            if query_params.need_approval:
                raise ValueError('need_approval should NOT be used to query bills')
            partial_url = self._query_bills_url() + '/count'
        elif query_type == _OrderType.REFUND:
            if query_params.spay_result:
                raise ValueError('spay_result should NOT be used to query refunds')
            partial_url = self._query_refunds_url() + '/count'
        else:
            return

        attach_app_sign(query_params, BCReqType.QUERY, self.bc_app)
        url = partial_url + '?para=' + obj_to_quote_str(query_params)
        tmp_resp = http_get(url, self.bc_app.timeout)
        # if err encountered, [0] equals 0
        if not tmp_resp[0]:
            return tmp_resp[1]

        # [1] contains result dict
        resp_dict = tmp_resp[1]
        bc_result = BCResult()

        set_common_attr(resp_dict, bc_result)

        if not bc_result.result_code:
            bc_result.count = resp_dict.get('count')

        return bc_result

    def query_bills_count(self, query_params):
        """
        query bills count API
        refer to https://beecloud.cn/doc/?index=rest-api #6
        :param query_params: beecloud.entity.BCQueryReqParams
        :return: beecloud.entity.BCResult
        """
        return self._query_orders_count(query_params, _OrderType.BILL)

    def query_refunds_count(self, query_params):
        """
        query refunds count API
        refer to https://beecloud.cn/doc/?index=rest-api #8
        :param query_params: beecloud.entity.BCQueryReqParams
        :return: beecloud.entity.BCResult
        """
        if self.bc_app.is_test_mode:
            return report_not_supported_err('query_refunds_count')
        return self._query_orders_count(query_params, _OrderType.REFUND)

    def _query_order_by_id(self, order_id, query_type):
        if query_type == _OrderType.BILL:
            partial_url = self._query_bill_url()
        elif query_type == _OrderType.REFUND:
            partial_url = self._query_refund_url()
        else:
            return

        query_params = _TmpObject()
        attach_app_sign(query_params, BCReqType.QUERY, self.bc_app)
        url = partial_url + '/' + order_id + '?para=' + obj_to_quote_str(query_params)
        tmp_resp = http_get(url, self.bc_app.timeout)
        # if err encountered, [0] equals 0
        if not tmp_resp[0]:
            return tmp_resp[1]

        # [1] contains result dict
        resp_dict = tmp_resp[1]
        bc_result = BCResult()
        set_common_attr(resp_dict, bc_result)

        if not bc_result.result_code:
            if query_type == _OrderType.BILL:
                order_dict = resp_dict.get('pay')
                bc_result.pay = parse_dict_to_obj(order_dict, BCBill)
            else:
                order_dict = resp_dict.get('refund')
                bc_result.refund = parse_dict_to_obj(order_dict, BCRefund)

        return bc_result

    def query_bill_by_id(self, bill_id):
        """
        query bill based on id(NOT bill number)
        refer to https://beecloud.cn/doc/?index=rest-api #11
        result.pay is type of beecloud.entity.BCBill
        :param bill_id: string type
        :return: beecloud.entity.BCResult
        """
        return self._query_order_by_id(bill_id, _OrderType.BILL)

    def query_refund_by_id(self, refund_id):
        """
        query refund based on id(NOT refund number)
        refer to https://beecloud.cn/doc/?index=rest-api #10
        result.refund is type of beecloud.entity.BCRefund
        :param refund_id: string type
        :return: beecloud.entity.BCResult
        """
        if self.bc_app.is_test_mode:
            return report_not_supported_err('query_refund_by_id')
        return self._query_order_by_id(refund_id, _OrderType.REFUND)

    def query_refund_status(self, channel, refund_no):
        """
        query refund status, it is for WX, YEE, KUAIQIAN, BD
        refer to https://beecloud.cn/doc/?index=rest-api #9
        :param channel: str of WX, YEE, KUAIQIAN, BD
        :param refund_no: refund number
        :return: beecloud.entity.BCResult
        """
        if self.bc_app.is_test_mode:
            return report_not_supported_err('query_refund_status')

        query_params = _TmpObject()
        query_params.channel = channel
        query_params.refund_no = refund_no
        attach_app_sign(query_params, BCReqType.QUERY, self.bc_app)
        url = self._query_refund_url() + '/status?para=' + obj_to_quote_str(query_params)
        tmp_resp = http_get(url, self.bc_app.timeout)
        # if err encountered, [0] equals 0
        if not tmp_resp[0]:
            return tmp_resp[1]

        # [1] contains result dict
        resp_dict = tmp_resp[1]
        bc_result = BCResult()

        set_common_attr(resp_dict, bc_result)

        if not bc_result.result_code:
            bc_result.refund_status = resp_dict.get('refund_status')

        return bc_result

    def query_offline_bill_status(self, bill_no, channel=None):
        """
        query offline bill status
        refer to https://beecloud.cn/doc/?index=rest-api-offline #3
        :param bill_no: bill number
        :param channel: bill payment channel like WX_SCAN
        :return: beecloud.entity.BCResult
        """
        if self.bc_app.is_test_mode:
            return report_not_supported_err('query_offline_bill_status')

        query_params = _TmpObject()
        setattr(query_params, 'bill_no', bill_no)
        if channel:
            setattr(query_params, 'channel', channel)
        attach_app_sign(query_params, BCReqType.QUERY, self.bc_app)
        url = get_rest_root_url() + 'rest/offline/bill/status'
        tmp_resp = http_post(url, query_params, self.bc_app.timeout)
        # if err encountered, [0] equals 0
        if not tmp_resp[0]:
            return tmp_resp[1]

        # [1] contains result dict
        resp_dict = tmp_resp[1]
        bc_result = BCResult()

        set_common_attr(resp_dict, bc_result)

        if not bc_result.result_code:
            setattr(bc_result, 'pay_result', resp_dict.get('pay_result'))

        return bc_result

    def query_bc_transfer_supported_banks(self, transfer_type):
        """
        query bc_transfer supported banks, used by BCCardTransferParams field: bank_fullname
        :param transfer_type: P_DE:对私借记卡, P_CR:对私信用卡, C:对公账户
        :return:
        """
        query_param = _TmpObject()
        query_param.type = transfer_type
        url = get_rest_root_url() + 'rest/bc_transfer/banks?para=' + obj_to_quote_str(query_param)
        tmp_resp = http_get(url, self.bc_app.timeout)
        # if err encountered, [0] equals 0
        if not tmp_resp[0]:
            return tmp_resp[1]

        # [1] contains result dict
        resp_dict = tmp_resp[1]
        bc_result = BCResult()

        set_common_attr(resp_dict, bc_result)

        if not bc_result.result_code:
            bc_result.size = resp_dict.get('size')
            bc_result.bank_list = resp_dict.get('bank_list')

        return bc_result

    def query_bc_gateway_supported_banks(self):
        """
        query bc_gateway supported banks
        :return: map, keys as bank abbr, value as bank name
        """
        return {u'CMB': u'招商银行', u'ICBC': u'工商银行', u'BOC': u'中国银行', u'ABC': u'农业银行',
                u'BOCM': u'交通银行', u'SPDB': u'浦发银行', u'GDB': u'广发银行', u'CITIC': u'中信银行',
                u'CEB': u'光大银行', u'CIB': u'兴业银行', u'SDB': u'平安银行', u'CMBC': u'民生银行',
                u'BEA': u'东亚银行', u'BOB': u'北京银行', u'SRCB': u'上海农商行', u'NJCB': u'南京银行',
                u'NBCB': u'宁波银行'}

    def query_plans(self, query_param=None):
        """
        query plans
        result contains a list(plan), its items are beecloud.entity.BCPlan
        :param query_param: query condition object beecloud.entity.BCQueryCriteria
                            attach more condition like obj.interval = 'day'
        :return: beecloud.entity.BCResult
        """
        return rest_query_objects(self.bc_app, self._query_plan_url(), query_param, 'plans', BCPlan)

    def query_plan_by_id(self, plan_id):
        """
        query subscription plan by id
        :param plan_id: plan object id
        :return: beecloud.entity.BCResult
        """
        return rest_query_object_by_id(self.bc_app, self._query_plan_url(), plan_id, 'plan', BCPlan)

    def query_subscription_payment_supported_banks(self):
        """
        query subscription payment supported banks
        :return: beecloud.entity.BCResult
        """
        query_param = _TmpObject()
        attach_app_sign(query_param, BCReqType.QUERY, self.bc_app)
        url = get_rest_root_url() + 'subscription_banks'
        tmp_resp = http_get(url, self.bc_app.timeout, params=obj_to_dict(query_param))
        # if err encountered, [0] equals 0
        if not tmp_resp[0]:
            return tmp_resp[1]

        # [1] contains result dict
        resp_dict = tmp_resp[1]
        bc_result = BCResult()

        set_common_attr(resp_dict, bc_result)

        if not bc_result.result_code:
            bc_result.banks = resp_dict.get('banks')
            bc_result.common_banks = resp_dict.get('common_banks')

        return bc_result

    def query_subscriptions(self, query_param=None):
        """
        query subscriptions
        result contains a list(plan), its items are beecloud.entity.BCPlan
        :param query_param: query condition object beecloud.entity.BCQueryCriteria
                            attach more condition like obj.interval = 'day'
        :return: beecloud.entity.BCResult
        """
        return rest_query_objects(self.bc_app, self._query_subscription_url(), query_param,
                                  'subscriptions', BCSubscription)

    def query_subscription_by_id(self, subscription_id):
        """
        query plans
        result contains a list(plan), its items are beecloud.entity.BCPlan
        :param subscription_id: subscription object id
        :return: beecloud.entity.BCResult
        """
        return rest_query_object_by_id(self.bc_app, self._query_subscription_url(), subscription_id,
                                       'subscription', BCSubscription)
