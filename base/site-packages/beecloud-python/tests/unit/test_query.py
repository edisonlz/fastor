# -*- coding: utf-8 -*-
"""
    beecloud query module unit test
    ~~~~~~~~~
    :created by xuanzhui on 2016/1/11.
    :copyright (c) 2015 BeeCloud.
    :license: MIT, see LICENSE for more details.
"""

import unittest
import mock
from beecloud import NETWORK_ERROR_CODE, NETWORK_ERROR_NAME, NOT_SUPPORTED_CODE
from beecloud.entity import BCApp, BCResult, BCQueryReqParams, BCChannelType, BCBill, BCRefund
from beecloud.utils import URL_REQ_SUCC, URL_REQ_FAIL
from beecloud.query import BCQuery


class QueryTestCase(unittest.TestCase):
    def setUp(self):
        self.bc_app = BCApp()
        self.bc_app.app_id = 'your_app_id'
        self.bc_app.app_secret = 'your_app_sec'
        self.bc_app.master_secret = 'your_master_sec'

        self.bc_query = BCQuery()
        self.bc_query.register_app(self.bc_app)

        # set up err result
        self.http_err = BCResult()
        self.http_err.result_code = NETWORK_ERROR_CODE
        self.http_err.result_msg = 404
        self.http_err.err_detail = 'not found'

        self.timeout_err = BCResult()
        self.timeout_err.result_code = NETWORK_ERROR_CODE
        self.timeout_err.result_msg = NETWORK_ERROR_NAME
        self.timeout_err.err_detail = 'ConnectionError: normally caused by timeout'

    def _inner_test_http_err_case(self, mock_obj, api_method, *args):
        # error case: http err like 404
        mock_obj.return_value = URL_REQ_FAIL, self.http_err

        result = api_method(*args)
        assert result.result_code == NETWORK_ERROR_CODE
        assert result.result_msg == 404

        # error case: http error like timeout
        mock_obj.return_value = URL_REQ_FAIL, self.timeout_err

        result = api_method(*args)
        assert result.result_code == NETWORK_ERROR_CODE
        assert result.result_msg == NETWORK_ERROR_NAME

    @mock.patch('beecloud.query.http_get')
    def test_query_bills(self, mock_get):
        # err case
        self._inner_test_http_err_case(mock_get, self.bc_query.query_bills, BCQueryReqParams())

        # succ case
        # in real request, bills contains more records
        resp_dict = {'result_msg': 'OK', 'err_detail': '', 'result_code': 0,
                     'bills': [{'id': 'unique_id', 'spay_result': True, 'create_time': 1447658025661, 'total_fee': 1,
                                'channel': 'UN', 'trade_no': '', 'bill_no': 'bc1447657931',
                                'optional': {'test': 'willreturn'}, 'revert_result': False,
                                'title': 'your bill title', 'sub_channel': 'UN_WEB', 'refund_result': False}]}
        mock_get.return_value = URL_REQ_SUCC, resp_dict

        query_params = BCQueryReqParams()
        query_params.channel = BCChannelType.UN
        result = self.bc_query.query_bills(query_params)
        assert result.result_code == 0
        assert result.result_msg == 'OK'
        assert result.err_detail == ''
        bill = result.bills[0]
        assert isinstance(bill, BCBill)
        assert bill.id == 'unique_id'
        assert bill.bill_no == 'bc1447657931'
        assert bill.channel == 'UN'
        assert bill.sub_channel == 'UN_WEB'
        assert bill.create_time == 1447658025661
        assert bill.optional == {'test': 'willreturn'}
        assert bill.spay_result
        assert bill.title == 'your bill title'
        assert bill.total_fee == 1
        assert not bill.revert_result
        assert not bill.refund_result

    @mock.patch('beecloud.query.http_get')
    def test_query_refunds(self, mock_get):
        # err case
        self._inner_test_http_err_case(mock_get, self.bc_query.query_refunds, BCQueryReqParams())

        # if test mode
        self.bc_app.is_test_mode = True
        self.bc_app.test_secret = 'your_test_sec'
        result = self.bc_query.query_refunds(BCQueryReqParams())
        assert result.result_code == NOT_SUPPORTED_CODE

        # succ case
        self.bc_app.is_test_mode = None   # or False
        # in real request, bills contains more records
        resp_dict = {"result_msg": "OK", "err_detail": "", "result_code": 0,
                     "refunds": [{"id": "unique_id", "result": False, "create_time": 1447430833318,
                                  "refund_no": "201511141447430832000", "total_fee": 1, "refund_fee": 1,
                                  "channel": "WX", "bill_no": "20151113132244266", "finish": True,
                                  "title": "2015-10-21 Release", "sub_channel": "WX_APP"}]}
        mock_get.return_value = URL_REQ_SUCC, resp_dict

        query_params = BCQueryReqParams()
        query_params.channel = BCChannelType.WX
        result = self.bc_query.query_refunds(query_params)
        assert result.result_code == 0
        assert result.result_msg == 'OK'
        assert result.err_detail == ''
        refund = result.refunds[0]
        assert isinstance(refund, BCRefund)
        assert refund.id == 'unique_id'
        assert refund.bill_no == '20151113132244266'
        assert refund.channel == 'WX'
        assert refund.sub_channel == 'WX_APP'
        assert refund.finish
        assert refund.create_time == 1447430833318
        assert not refund.result
        assert refund.title == '2015-10-21 Release'
        assert refund.total_fee == 1
        assert refund.refund_fee == 1
        assert refund.refund_no == '201511141447430832000'

    @mock.patch('beecloud.query.http_get')
    def test_query_bill_by_id(self, mock_get):
        # err case
        self._inner_test_http_err_case(mock_get, self.bc_query.query_bill_by_id, "unique_id")

        # succ case
        self.bc_app.is_test_mode = None   # or False
        resp_dict = {'result_msg': 'OK', 'err_detail': '', 'result_code': 0,
                     'pay': {'id': 'unique_id', 'spay_result': True, 'create_time': 1447658025661, 'total_fee': 1,
                             'channel': 'UN', 'trade_no': '', 'bill_no': 'bc1447657931',
                             'optional': {'test': 'willreturn'}, 'revert_result': False,
                             'title': 'your bill title', 'sub_channel': 'UN_WEB', 'refund_result': False}}
        mock_get.return_value = URL_REQ_SUCC, resp_dict

        result = self.bc_query.query_bill_by_id('unique_id')
        assert result.result_code == 0
        assert result.result_msg == 'OK'
        assert result.err_detail == ''
        bill = result.pay
        assert isinstance(bill, BCBill)
        assert bill.id == 'unique_id'
        assert bill.bill_no == 'bc1447657931'
        assert bill.channel == 'UN'
        assert bill.sub_channel == 'UN_WEB'
        assert bill.create_time == 1447658025661
        assert bill.optional == {'test': 'willreturn'}
        assert bill.spay_result
        assert bill.title == 'your bill title'
        assert bill.total_fee == 1
        assert not bill.revert_result
        assert not bill.refund_result

    @mock.patch('beecloud.query.http_get')
    def test_query_refund_by_id(self, mock_get):
        # err case
        self._inner_test_http_err_case(mock_get, self.bc_query.query_refund_by_id, "unique_id")

        # if test mode
        self.bc_app.is_test_mode = True
        self.bc_app.test_secret = 'your_test_sec'
        result = self.bc_query.query_refund_by_id("unique_id")
        assert result.result_code == NOT_SUPPORTED_CODE

        # succ case
        self.bc_app.is_test_mode = None   # or False
        resp_dict = {"result_msg": "OK", "err_detail": "", "result_code": 0,
                     "refund": {"id": "unique_id", "result": False, "create_time": 1447430833318,
                                "refund_no": "201511141447430832000", "total_fee": 1, "refund_fee": 1,
                                "channel": "WX", "bill_no": "20151113132244266", "finish": True,
                                "title": "2015-10-21 Release", "sub_channel": "WX_APP"}}
        mock_get.return_value = URL_REQ_SUCC, resp_dict

        result = self.bc_query.query_refund_by_id('unique_id')
        assert result.result_code == 0
        assert result.result_msg == 'OK'
        assert result.err_detail == ''
        refund = result.refund
        assert isinstance(refund, BCRefund)
        assert refund.id == 'unique_id'
        assert refund.bill_no == '20151113132244266'
        assert refund.channel == 'WX'
        assert refund.sub_channel == 'WX_APP'
        assert refund.finish
        assert refund.create_time == 1447430833318
        assert not refund.result
        assert refund.title == '2015-10-21 Release'
        assert refund.total_fee == 1
        assert refund.refund_fee == 1
        assert refund.refund_no == '201511141447430832000'

    @mock.patch('beecloud.query.http_get')
    def test_query_bills_count(self, mock_get):
        # err case
        self._inner_test_http_err_case(mock_get, self.bc_query.query_bills_count, BCQueryReqParams())

        # succ case
        resp_dict = {'result_msg': 'OK', 'err_detail': '', 'result_code': 0, 'count': 888}
        mock_get.return_value = URL_REQ_SUCC, resp_dict

        query_params = BCQueryReqParams()
        query_params.channel = BCChannelType.UN
        result = self.bc_query.query_bills_count(query_params)
        assert result.result_code == 0
        assert result.result_msg == 'OK'
        assert result.err_detail == ''
        assert result.count == 888

    @mock.patch('beecloud.query.http_get')
    def test_query_refunds_count(self, mock_get):
        # err case
        self._inner_test_http_err_case(mock_get, self.bc_query.query_refunds_count, BCQueryReqParams())

        # if test mode
        self.bc_app.is_test_mode = True
        self.bc_app.test_secret = 'your_test_sec'
        result = self.bc_query.query_refunds_count(BCQueryReqParams())
        assert result.result_code == NOT_SUPPORTED_CODE

        # succ case
        self.bc_app.is_test_mode = None   # or False
        resp_dict = {'result_msg': 'OK', 'err_detail': '', 'result_code': 0, 'count': 888}
        mock_get.return_value = URL_REQ_SUCC, resp_dict

        query_params = BCQueryReqParams()
        query_params.channel = BCChannelType.UN
        result = self.bc_query.query_refunds_count(query_params)
        assert result.result_code == 0
        assert result.result_msg == 'OK'
        assert result.err_detail == ''
        assert result.count == 888

    @mock.patch('beecloud.query.http_get')
    def test_query_refund_status(self, mock_get):
        # err case
        self._inner_test_http_err_case(mock_get, self.bc_query.query_refund_status, 'channel', 'refund_no')

        # if test mode
        self.bc_app.is_test_mode = True
        self.bc_app.test_secret = 'your_test_sec'
        result = self.bc_query.query_refund_status('channel', 'refund_no')
        assert result.result_code == NOT_SUPPORTED_CODE

        # succ case
        self.bc_app.is_test_mode = None   # or False
        resp_dict = {'result_msg': 'OK', 'err_detail': '', 'result_code': 0, 'refund_status': 'SUCCESS'}
        mock_get.return_value = URL_REQ_SUCC, resp_dict

        result = self.bc_query.query_refund_status('channel', 'refund_no')
        assert result.result_code == 0
        assert result.result_msg == 'OK'
        assert result.err_detail == ''
        assert result.refund_status == 'SUCCESS'


if __name__ == '__main__':
    unittest.main()
