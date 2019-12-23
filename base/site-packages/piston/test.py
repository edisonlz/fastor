# Django imports
import django.test.client as client
import django.test as test
from django.utils.http import urlencode

# Piston imports
from piston import oauth
from piston.models import Consumer, Token

# 3rd/Python party imports
import httplib2, urllib, cgi

URLENCODED_FORM_CONTENT = 'application/x-www-form-urlencoded'

class OAuthClient(client.Client):
    def __init__(self, consumer, token):
        self.token = oauth.OAuthToken(token.key, token.secret)
        self.consumer = oauth.OAuthConsumer(consumer.key, consumer.secret)
        self.signature = oauth.OAuthSignatureMethod_HMAC_SHA1()

        super(OAuthClient, self).__init__()

    def request(self, **request):
        # Figure out parameters from request['QUERY_STRING'] and FakePayload
        params = {}
        if request['REQUEST_METHOD'] in ('POST', 'PUT'):
            if request['CONTENT_TYPE'] == URLENCODED_FORM_CONTENT:
                payload = request['wsgi.input'].read()
                request['wsgi.input'] = client.FakePayload(payload)
                params = cgi.parse_qs(payload)

        url = "http://testserver" + request['PATH_INFO']

        req = oauth.OAuthRequest.from_consumer_and_token(
            self.consumer, token=self.token, 
            http_method=request['REQUEST_METHOD'], http_url=url, 
            parameters=params
        )

        req.sign_request(self.signature, self.consumer, self.token)
        headers = req.to_header()
        request['HTTP_AUTHORIZATION'] = headers['Authorization']

        return super(OAuthClient, self).request(**request)

    def post(self, path, data={}, content_type=None, follow=False, **extra):
        if content_type is None:
            content_type = URLENCODED_FORM_CONTENT

        if isinstance(data, dict):
            data = urlencode(data)
        
        return super(OAuthClient, self).post(path, data, content_type, follow, **extra)

class TestCase(test.TestCase):
    pass

class OAuthTestCase(TestCase):
    @property
    def oauth(self):
        return OAuthClient(self.consumer, self.token)

