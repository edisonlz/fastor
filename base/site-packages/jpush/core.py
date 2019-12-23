import json
import logging
import warnings

import requests
from . import common
from .push import Push
from .device import Device
from .report import Report
from .schedule import Schedule


logger = logging.getLogger('jpush')


class JPush(object):
    def __init__(self, key, secret, timeout=30, zone = 'default'):
        self.key = key
        self.secret = secret
        self.timeout = timeout
        self.zone = zone
        self.session = requests.Session()
        self.session.auth = (key, secret)

    def _request(self, method, body, url, content_type=None, version=None, params=None):
        headers = {}
        headers['user-agent'] = 'jpush-api-python-client'
        headers['connection'] = 'keep-alive'
        headers['content-type'] = 'application/json;charset:utf-8'

        logger.debug("Making %s request to %s. Headers:\n\t%s\nBody:\n\t%s",
                     method, url, '\n\t'.join('%s: %s' % (key, value) for (key, value) in headers.items()), body)
        try:
            response = self.session.request(method, url, data=body, params=params,
                                            headers=headers, timeout=self.timeout)
        except requests.exceptions.ConnectTimeout:
            raise common.APIConnectionException("Connection to api.jpush.cn timed out.")
        except Exception:
            raise common.APIConnectionException("Connection to api.jpush.cn error.")

        logger.debug("Received %s response. Headers:\n\t%s\nBody:\n\t%s", response.status_code, '\n\t'.join(
                '%s: %s' % (key, value) for (key, value) in response.headers.items()), response.content)

        if response.status_code == 401:
            raise common.Unauthorized("Please check your AppKey and Master Secret")
        elif not (200 <= response.status_code < 300):
            raise common.JPushFailure.from_response(response)
        return response

    def push(self, payload):
        """Push this payload to the specified recipients.

        Payload: a dictionary the contents to send, e.g.:
            {'aps': {'alert': 'Hello'}, 'android': {'alert': 'Hello'}}
        """
        warnings.warn(
            "JPush.push() is deprecated. See documentation on upgrading.",
            DeprecationWarning)
        body = json.dumps(payload)
        url = common.get_url('push', self.zone) + 'push'
        self._request('POST', body, url, 'application/json', version=1)

    def  set_logging(self, level):
        level_list= ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]
        if level in level_list:
            if(level == "CRITICAL"):
                logging.basicConfig(level=logging.CRITICAL)
            if (level == "ERROR"):
                logging.basicConfig(level=logging.ERROR)
            if (level == "WARNING"):
                logging.basicConfig(level=logging.WARNING)
            if (level == "INFO"):
                logging.basicConfig(level=logging.INFO)
            if (level == "DEBUG"):
                logging.basicConfig(level=logging.DEBUG)
            if (level == "NOTSET"):
                logging.basicConfig(level=logging.NOTSET)
        else:
            print ("set logging level failed ,the level is invalid.")

    def create_push(self):
        """Create a Push notification."""
        return Push(self)

    def create_device(self):
        """Create a Device information."""
        return Device(self)

    def create_report(self):
        """Create a Report."""
        return Report(self)

    def create_schedule(self):
        """Create a Schedule."""
        return Schedule(self)

class GroupPush(JPush):

    def __init__(self, key, secret):
        JPush.__init__(self, 'group-' + key, secret)

    def create_push(self):
        """Create a Group Push notification."""
        return Push(self, end_point = 'grouppush')

class Admin(JPush):
    def __init__(self, key, secret):
        JPush.__init__(self, key, secret)

    def create_app(self, app_name, android_package, group_name=None):
        url = 'https://admin.jpush.cn/v1/app'
        entity = {
            'app_name': app_name,
            'android_package': android_package,
            'group_name': group_name
        }
        body = json.dumps(entity)
        response = self._request('post', body, url, content_type=None, version=3)
        return AdminResponse(response)

    def delete_app(self, app_key):
        url = 'https://admin.jpush.cn/v1/app/' + app_key + '/delete'
        response = self._request('post', None, url, content_type=None, version=3)
        return AdminResponse(response)

class AdminResponse(object):

    payload = None
    status_code = None

    def __init__(self, response):
        self.status_code = response.status_code
        if 0 != len(response.content):
            data = response.json()
            self.payload = data
        elif 200 == response.status_code:
            self.payload = "success"

    def get_status_code(self):
        return self.status_code

    def __str__(self):
        return "Admin response Payload: {0}".format(self.payload)
