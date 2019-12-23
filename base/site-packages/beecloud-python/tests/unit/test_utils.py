# -*- coding: utf-8 -*-
"""
    beecloud utils module unit test
    ~~~~~~~~~
    :created by xuanzhui on 2016/1/11.
    :copyright (c) 2015 BeeCloud.
    :license: MIT, see LICENSE for more details.
"""

import unittest
import mock
from beecloud import NETWORK_ERROR_CODE, NETWORK_ERROR_NAME
from beecloud.utils import http_get, http_post, http_put, URL_REQ_FAIL, URL_REQ_SUCC
from beecloud.entity import BCPayReqParams, BCApp
import requests
import requests.exceptions
import sys


class UtilsTestCase(unittest.TestCase):
    @mock.patch('beecloud.utils.requests.get')
    def test_http_get(self, mock_get):
        self._inner_test_http_method(http_get, mock_get)

    @mock.patch('beecloud.utils.requests.post')
    def test_http_post(self, mock_post):
        # app id and secret is required when init BC prefixed request class
        BCApp.app_id = 'your app id'
        BCApp.app_secret = 'your app sec'
        self._inner_test_http_method(http_post, mock_post, req_param=BCPayReqParams())

    @mock.patch('beecloud.utils.requests.put')
    def test_http_put(self, mock_put):
        self._inner_test_http_method(http_put, mock_put, req_param={'key': 'value'})

    # api_method is the target method to be tested, requests_mock_method is http request method like requests.get
    def _inner_test_http_method(self, api_method, requests_mock_method, url='mock://url', req_param=None):
        # error case: exception
        requests_mock_method.side_effect = requests.exceptions.ConnectionError('time out')
        if req_param:
            result = api_method(url, req_param)
        else:
            result = api_method(url)
        assert result[0] == URL_REQ_FAIL
        assert result[1].result_code == NETWORK_ERROR_CODE
        assert result[1].result_msg == NETWORK_ERROR_NAME
        assert result[1].err_detail == 'ConnectionError: normally caused by timeout'

        # error case: 404
        requests_mock_method.side_effect = None
        resp = requests.Response()
        resp.status_code = 500
        resp.reason = 'internal error'
        requests_mock_method.return_value = resp
        if req_param:
            result = api_method(url, req_param)
        else:
            result = api_method(url)
        assert result[0] == URL_REQ_FAIL
        assert result[1].result_code == NETWORK_ERROR_CODE
        assert result[1].result_msg == 500
        assert result[1].err_detail == 'internal error'

        # succ case
        resp.status_code = 200
        # _content will be used by requests.json
        if sys.version_info[0] == 3:
            resp._content = bytes(r'{"result_code":0, "result_msg": "OK"}', 'UTF-8')
        else:
            resp._content = r'{"result_code":0, "result_msg": "OK"}'
        resp.reason = 'OK'
        requests_mock_method.return_value = resp
        if req_param:
            result = api_method(url, req_param)
        else:
            result = api_method(url)

        assert result[0] == URL_REQ_SUCC
        assert isinstance(result[1], dict)
        assert result[1]['result_code'] == 0
        assert result[1]['result_msg'] == 'OK'

if __name__ == '__main__':
    unittest.main()
