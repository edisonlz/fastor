import json
import logging
from jpush import common

logger = logging.getLogger('jpush')


class Schedule(object):
    """JPush Report API V3"""
    def __init__(self, jpush, zone = None):
        self._jpush = jpush
        self.zone = zone or jpush.zone

    def send(self, method, url, body = None, content_type=None, version=3, params = None):
        response = self._jpush._request(method, body, url, content_type, version=3, params = params)
        return ScheduleResponse(response)

    def post_schedule(self, schedulepayload):
        url = common.get_url('schedule', self.zone)
        body = json.dumps(schedulepayload)
        result = self.send("POST", url, body)
        return result

    def get_schedule_by_id(self, schedule_id):
        url = common.get_url('schedule', self.zone) + schedule_id
        result = self.send("GET", url)
        return result

    def get_schedule_list(self, page = 1):
        url = common.get_url('schedule', self.zone)
        params = { 'page': page }
        result = self.send("GET", url, params = params)
        return result

    def put_schedule(self, schedulepayload, schedule_id):
        url = common.get_url('schedule', self.zone) + schedule_id
        body = json.dumps(schedulepayload)
        result = self.send("PUT", url, body)
        return result

    def delete_schedule(self,schedule_id):
        url = common.get_url('schedule', self.zone) + schedule_id
        result = self.send("DELETE", url)
        return result


class ScheduleResponse(object):
    """Response to a successful device request send.

    Right now this is a fairly simple wrapper around the json payload response,
    but making it an object gives us some flexibility to add functionality
    later.

    """
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
        return "Schedule response Payload: {0}".format(self.payload)