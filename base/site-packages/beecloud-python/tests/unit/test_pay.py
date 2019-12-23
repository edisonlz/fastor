# -*- coding: utf-8 -*-
"""
    beecloud pay module unit test
    ~~~~~~~~~
    :created by xuanzhui on 2016/1/11.
    :copyright (c) 2015 BeeCloud.
    :license: MIT, see LICENSE for more details.
"""

import unittest
import mock
from beecloud import NETWORK_ERROR_CODE, NETWORK_ERROR_NAME, NOT_SUPPORTED_CODE
from beecloud.utils import URL_REQ_SUCC, URL_REQ_FAIL, order_num_on_datetime
from beecloud.pay import BCPay
from beecloud.entity import BCApp, BCResult, BCPayReqParams, BCChannelType, BCRefundReqParams, BCPreRefundAuditParams, \
    BCTransferRedPack, BCTransferReqParams, BCBatchTransferItem, BCBatchTransferParams, BCInternationalPayParams, \
    BCCardTransferParams


class PayTestCase(unittest.TestCase):
    def setUp(self):
        self.bc_app = BCApp()
        self.bc_app.app_id = 'your_app_id'
        self.bc_app.app_secret = 'your_app_sec'
        self.bc_app.master_secret = 'your_master_sec'

        self.bc_pay = BCPay()
        self.bc_pay.register_app(self.bc_app)

        # set up err result
        self.http_err = BCResult()
        self.http_err.result_code = NETWORK_ERROR_CODE
        self.http_err.result_msg = 404
        self.http_err.err_detail = 'not found'

        self.timeout_err = BCResult()
        self.timeout_err.result_code = NETWORK_ERROR_CODE
        self.timeout_err.result_msg = NETWORK_ERROR_NAME
        self.timeout_err.err_detail = 'ConnectionError: normally caused by timeout'

    def _inner_test_http_err_case(self, mock_obj, req_param, api_method):
        # error case: http err like 404
        mock_obj.return_value = URL_REQ_FAIL, self.http_err

        result = api_method(req_param)
        assert result.result_code == NETWORK_ERROR_CODE
        assert result.result_msg == 404

        # error case: http error like timeout
        mock_obj.return_value = URL_REQ_FAIL, self.timeout_err

        result = api_method(req_param)
        assert result.result_code == NETWORK_ERROR_CODE
        assert result.result_msg == NETWORK_ERROR_NAME

    # http_post is imported from utils
    @mock.patch('beecloud.pay.http_post')
    def test_pay(self, mock_post):
        # err case
        self._inner_test_http_err_case(mock_post, BCPayReqParams(), self.bc_pay.pay)

        # succ case
        # here is a trick that for py2, keys and values of requests returned dict are tagged with [u],
        # which indicates they are unicode strings, here and below mocks will ignore it
        resp_dict = {'url': 'https://mapi.alipay.com/more', 'result_code': 0,
                     'id': '5668e844-4161-4ac5-973b-7630d4c09a64', 'result_msg': 'OK',
                     'err_detail': '', 'html': 'html_content_more'}
        mock_post.return_value = URL_REQ_SUCC, resp_dict

        pay_params = BCPayReqParams()
        # not really required for unit test as http request is mocked
        pay_params.title = 'test case'
        pay_params.total_fee = 100
        pay_params.channel = BCChannelType.ALI_WEB
        pay_params.bill_no = 'billno12345678'
        pay_params.return_url = 'http://return_url'
        result = self.bc_pay.pay(pay_params)
        assert result.result_code == 0
        assert result.result_msg == 'OK'
        assert result.err_detail == ''
        assert result.id == '5668e844-4161-4ac5-973b-7630d4c09a64'
        assert result.url == 'https://mapi.alipay.com/more'
        assert result.html == 'html_content_more'

    @mock.patch('beecloud.pay.http_post')
    def test_refund(self, mock_post):
        # err case
        self._inner_test_http_err_case(mock_post, BCRefundReqParams(), self.bc_pay.refund)

        # if test mode
        self.bc_app.is_test_mode = True
        self.bc_app.test_secret = 'your_test_sec'
        result = self.bc_pay.refund(BCRefundReqParams())
        assert result.result_code == NOT_SUPPORTED_CODE
        # print(result.err_detail)

        # succ case
        self.bc_app.is_test_mode = None   # or False

        resp_dict = {'url': 'https://mapi.alipay.com/more', 'result_code': 0,
                     'id': '5668e844-4161-4ac5-973b-7630d4c09a64', 'result_msg': 'OK',
                     'err_detail': ''}
        mock_post.return_value = URL_REQ_SUCC, resp_dict

        refund_params = BCRefundReqParams()
        # not really required for unit test as http request is mocked
        refund_params.channel = BCChannelType.ALI   # channel is not mandatory
        refund_params.refund_no = 'refundno1234567'
        refund_params.bill_no = 'billno12345678'
        refund_params.refund_fee = 100
        refund_params.optional = {'key1': 'value1'}
        result = self.bc_pay.refund(refund_params)
        assert result.result_code == 0
        assert result.result_msg == 'OK'
        assert result.err_detail == ''
        assert result.id == '5668e844-4161-4ac5-973b-7630d4c09a64'
        assert result.url == 'https://mapi.alipay.com/more'

    @mock.patch('beecloud.pay.http_put')
    def test_audit_pre_refunds(self, mock_put):
        # err case
        self._inner_test_http_err_case(mock_put, BCPreRefundAuditParams(), self.bc_pay.audit_pre_refunds)

        # if test mode
        self.bc_app.is_test_mode = True
        self.bc_app.test_secret = 'your_test_sec'
        result = self.bc_pay.audit_pre_refunds(BCPreRefundAuditParams())
        assert result.result_code == NOT_SUPPORTED_CODE
        # print(result.err_detail)

        # succ case
        self.bc_app.is_test_mode = None   # or False

        resp_dict = {'result_code': 0, 'result_msg': 'OK', 'err_detail': '',
                     'result_map': {'4b45eb63-2a2d-402e-8d87-efaf05c29719': 'OK',
                                    '8c0efdf8-d599-47e7-ad03-2f04087ea4be': 'OK'}}
        mock_put.return_value = URL_REQ_SUCC, resp_dict

        pre_refund_params = BCPreRefundAuditParams()
        # not really required for unit test as http request is mocked
        pre_refund_params.channel = BCChannelType.ALI
        pre_refund_params.ids = ["d9690a6e-ae99-44b7-9904-bd9d43fcc21b", "6f263aa6-111d-4c95-b51e-001b3f7e6ddf"]
        pre_refund_params.bill_no = 'billno12345678'
        pre_refund_params.agree = True
        result = self.bc_pay.audit_pre_refunds(pre_refund_params)
        assert result.result_code == 0
        assert result.result_msg == 'OK'
        assert result.err_detail == ''
        assert result.result_map == {'4b45eb63-2a2d-402e-8d87-efaf05c29719': 'OK',
                                     '8c0efdf8-d599-47e7-ad03-2f04087ea4be': 'OK'}

    @mock.patch('beecloud.pay.http_post')
    def test_transfer(self, mock_post):
        # err case
        self._inner_test_http_err_case(mock_post, BCTransferReqParams(), self.bc_pay.transfer)

        # if test mode
        self.bc_app.is_test_mode = True
        self.bc_app.test_secret = 'your_test_sec'
        result = self.bc_pay.transfer(BCTransferReqParams())
        assert result.result_code == NOT_SUPPORTED_CODE
        # print(result.err_detail)

        # succ case
        self.bc_app.is_test_mode = None   # or False

        resp_dict = {'result_msg': 'OK', 'err_detail': '', 'result_code': 0}
        mock_post.return_value = URL_REQ_SUCC, resp_dict

        transfer_params = BCTransferReqParams()
        # not really required for unit test as http request is mocked
        transfer_params.channel = BCChannelType.WX_REDPACK
        # 10 digits for WX
        transfer_params.transfer_no = order_num_on_datetime()[0:10]
        transfer_params.desc = 'desc'
        # range for WX 1-200 RMB
        transfer_params.total_fee = 100     # cent
        transfer_params.channel_user_id = 'wx_open_id'
        redpack = BCTransferRedPack()
        redpack.send_name = 'BeeCloud'
        redpack.wishing = u'BeeCloud祝福开发者工作顺利'
        redpack.act_name = u'BeeCloud开发者测试中'
        transfer_params.redpack_info = redpack
        result = self.bc_pay.transfer(transfer_params)
        assert result.result_code == 0
        assert result.result_msg == 'OK'
        assert result.err_detail == ''

    @mock.patch('beecloud.pay.http_post')
    def test_bc_transfer(self, mock_post):
        # err case
        self._inner_test_http_err_case(mock_post, BCCardTransferParams(), self.bc_pay.bc_transfer)

        # if test mode
        self.bc_app.is_test_mode = True
        self.bc_app.test_secret = 'your_test_sec'
        result = self.bc_pay.bc_transfer(BCCardTransferParams())
        assert result.result_code == NOT_SUPPORTED_CODE
        # print(result.err_detail)

        # succ case
        self.bc_app.is_test_mode = None   # or False

        resp_dict = {'result_msg': 'OK', 'err_detail': '', 'result_code': 0}
        mock_post.return_value = URL_REQ_SUCC, resp_dict

        transfer_params = BCCardTransferParams()
        transfer_params.total_fee = 1
        transfer_params.bill_no = order_num_on_datetime()
        # 最长支持16个汉字
        transfer_params.title = u'python比可代付测试'
        # 银行缩写编码
        transfer_params.bank_code = 'BOC'
        # 银行联行行号
        transfer_params.bank_associated_code = '12345678'
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
        result = self.bc_pay.bc_transfer(transfer_params)
        assert result.result_code == 0
        assert result.result_msg == 'OK'
        assert result.err_detail == ''

    @mock.patch('beecloud.pay.http_post')
    def test_batch_transfer(self, mock_post):
        # err case
        self._inner_test_http_err_case(mock_post, BCBatchTransferParams(), self.bc_pay.batch_transfer)

        # if test mode
        self.bc_app.is_test_mode = True
        self.bc_app.test_secret = 'your_test_sec'
        result = self.bc_pay.batch_transfer(BCBatchTransferParams())
        assert result.result_code == NOT_SUPPORTED_CODE
        # print(result.err_detail)

        # succ case
        self.bc_app.is_test_mode = None   # or False

        resp_dict = {'result_msg': 'OK', 'url': 'https://mapi.alipay.com/more', 'err_detail': '', 'result_code': 0}
        mock_post.return_value = URL_REQ_SUCC, resp_dict

        transfer_params = BCBatchTransferParams()
        # not really required for unit test as http request is mocked
        transfer_params.channel = BCChannelType.ALI
        transfer_params.batch_no = order_num_on_datetime()
        transfer_params.account_name = u'苏州比可网络科技有限公司'
        item1 = BCBatchTransferItem()
        item1.transfer_id = order_num_on_datetime() + 'a'
        item1.receiver_account = '1234567'
        item1.receiver_name = u'某人1'
        item1.transfer_fee = 1
        item1.transfer_note = u'python支付宝批量打款item1'

        item2 = BCBatchTransferItem()
        item2.transfer_id = order_num_on_datetime() + 'b'
        item2.receiver_account = 'ali@account.c'
        item2.receiver_name = 'account2'
        item2.transfer_fee = 1
        item2.transfer_note = u'python支付宝批量打款item2'

        transfer_params.transfer_data = [item1, item2]

        result = self.bc_pay.batch_transfer(transfer_params)
        assert result.result_code == 0
        assert result.result_msg == 'OK'
        assert result.err_detail == ''
        assert result.url == 'https://mapi.alipay.com/more'

    @mock.patch('beecloud.pay.http_post')
    def test_international_pay(self, mock_post):
        # err case
        self._inner_test_http_err_case(mock_post, BCInternationalPayParams(), self.bc_pay.international_pay)

        # if test mode
        self.bc_app.is_test_mode = True
        self.bc_app.test_secret = 'your_test_sec'
        result = self.bc_pay.international_pay(BCInternationalPayParams())
        assert result.result_code == NOT_SUPPORTED_CODE
        # print(result.err_detail)

        # succ case
        self.bc_app.is_test_mode = None   # or False

        resp_dict = {'err_detail': '', 'url': 'https://www.paypal.com/more', 'result_msg': 'OK', 'result_code': 0}
        mock_post.return_value = URL_REQ_SUCC, resp_dict

        req_params = BCInternationalPayParams()
        # not really required for unit test as http request is mocked
        req_params.channel = BCChannelType.PAYPAL_PAYPAL
        req_params.title = u'python PayPal 支付测试'
        req_params.total_fee = 1    # cent
        req_params.currency = 'USD'
        req_params.bill_no = order_num_on_datetime()
        # 支付完成后的跳转页面
        req_params.return_url = 'https://beecloud.cn/'

        result = self.bc_pay.international_pay(req_params)

        assert result.result_code == 0
        assert result.result_msg == 'OK'
        assert result.err_detail == ''
        assert result.url == 'https://www.paypal.com/more'

if __name__ == '__main__':
    unittest.main()
