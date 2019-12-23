import logging
from jpush import common

logger = logging.getLogger('jpush')


class Report(object):
    """JPush Report API V3"""
    def __init__(self, jpush, zone = None):
        self._jpush = jpush
        self.zone = zone or jpush.zone

    def send(self, method, url, body = None, content_type=None, version=3, params = None):
        """Send the request
        """
        response = self._jpush._request(method, body,url,content_type,version=3, params = params)
        return ReportResponse(response)

    def get_received(self,msg_ids):
        url = common.get_url('report', self.zone) + 'received'
        params = { 'msg_ids': msg_ids }
        received = self.send("GET", url, params = params)
        return received

    def get_messages(self, msg_ids):
        url = common.get_url('report', self.zone) + 'messages'
        params = { 'msg_ids': msg_ids }
        messages = self.send("GET", url, params = params)
        return messages

    def get_users(self, time_unit,start,duration):
        url = common.get_url('report', self.zone) + 'users'
        params = {
            'time_unit': time_unit,
            'start': start,
            'duration': duration
        }
        users = self.send("GET", url, params = params)
        return users


class ReportResponse(object):

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
        return "Report response Payload: {0}".format(self.payload)