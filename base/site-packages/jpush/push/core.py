import json
import logging
from jpush import common

logger = logging.getLogger('jpush')


class Push(object):
    """A push notification. Set audience, message, etc, and send."""

    def __init__(self, jpush, end_point = 'push', zone = None):
        self._jpush = jpush
        self.audience = None
        self.notification = None
        self.platform = None
        self.cid = None
        self.options = None
        self.message = None
        self.smsmessage=None
        self.end_point = end_point
        self.zone = zone or jpush.zone

    @property
    def payload(self):
        data = {
            "audience": self.audience,
            "platform": self.platform,
        }
        if (self.notification is None) and (self.message is None):
            raise ValueError("Notification and message cannot be both empty")
        if self.cid is not None:
            data['cid'] = self.cid
        if self.notification is not None:
            data['notification'] = self.notification
        if self.smsmessage is not None:
            data['sms_message'] = self.smsmessage
        if self.options is not None:
            data['options'] = self.options
        if self.message is not None:
            data['message'] = self.message
        return data

    def send(self):
        """Send the notification.

        :returns: :py:class:`PushResponse` object with ``push_ids`` and
            other response data.
        :raises JPushFailure: Request failed.
        :raises Unauthorized: Authentication failed.

        """
        body = json.dumps(self.payload)
        url = common.get_url('push', self.zone) + self.end_point
        response = self._jpush._request('POST', body, url, 'application/json', version=3)
        return PushResponse(response)

    def send_validate(self):
        """Send the notification to validate.

        :returns: :py:class:`PushResponse` object with ``push_ids`` and
            other response data.
        :raises JPushFailure: Request failed.
        :raises Unauthorized: Authentication failed.

        """
        body = json.dumps(self.payload)
        url = common.get_url('push', self.zone) + 'push/validate'

        response = self._jpush._request('POST', body, url, 'application/json', version=3)
        return PushResponse(response)

    def get_cid(self, count, type = None):
        body = None
        url = common.get_url('push', self.zone) + 'push/cid'

        params = {
            'count': count,
            'type': type
        }
        response = self._jpush._request('GET', body, url, 'application/json', version=3, params = params)
        return PushResponse(response)


class PushResponse(object):
    """Response to a successful push notification send.

    Right now this is a fairly simple wrapper around the json payload response,
    but making it an object gives us some flexibility to add functionality
    later.

    """
    payload = None
    status_code = None

    def __init__(self, response):
        self.status_code = response.status_code
        data = response.json()
        self.payload = data

    def get_status_code(self):
        return self.status_code

    def __str__(self):
        return "Response Payload: {0}".format(self.payload)
