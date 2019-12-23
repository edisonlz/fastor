# Copyright (c) 2007, Columbia Center For New Media Teaching And Learning (CCNMTL)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the CCNMTL nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY CCNMTL ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <copyright holder> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

""" Test Suite for restclient

Contributed by Christopher Hesse, modified by Anders Pearson

Requires nose to run.

By default, starts a server on port 11123. set the RESTCLIENT_TEST_PORT environment variable to change.

If anyone knows how to make BaseHTTPServer not print the stuff like
  "localhost - - [08/Mar/2007 17:12:54] "GET / HTTP/1.1" 200 -"
on each request it handles, please submit a patch. 

"""

from restclient import *
import threading, os
import BaseHTTPServer
import cgi
import random

random.seed()
port_num = int(os.environ.get('RESTCLIENT_TEST_PORT',random.randint(10000,11000)))
hostname = "http://localhost:%d/" % port_num
image = open(os.path.join(os.getcwd(), 'sample.jpg')).read()

# default headers
headers = {'accept-encoding': 'compress, gzip'}

def start_server(callback):
    class LoopbackHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        """ a simple http server that will basically echo back the request
        that was made to it """
        def respond(self):
            s = self.requestline + u"\n" \
                + str(self.headers) + u"\n\n" \
                + self.body()

            response = s.encode('utf-8')

            self.send_response(200)
            self.send_header('Content-Type','text/html; charset=utf-8')
            self.send_header('Content-Length',str(len(response)))
            self.end_headers()
            self.wfile.write(response)
            self.wfile.close()
            self.rfile.close()

        do_GET = do_POST = do_PUT = do_HEAD = do_DELETE = respond

        def body(self):
            ct = self.headers.getheader('content-type')
            body = self.rfile.read(int(self.headers.getheader('content-length')))
            if ct.startswith('multipart/form-data'):
                return "multipart: %d\n" % len(body) + body.encode('base64')
            else:
                return body

        def log_request(self,format,*args):
            """ shut the hell up """
            pass


    def run():
        """ start the server for a single request """
        server_class=BaseHTTPServer.HTTPServer
        handler_class=LoopbackHandler
        server_address = ('', port_num)
        httpd = server_class(server_address, handler_class)
        httpd.handle_request()
        
    thread = threading.Thread(target=run)
    thread.setDaemon(True)
    thread.start()
    callback()
    

def servify(f):
    def test(*args, **kwargs):
        def run():
            f(*args, **kwargs)
        global port_num, hostname
        port_num += 1
        hostname = "http://localhost:%d/" % port_num
        start_server(run)
    test.__doc__ = f.__doc__
    return test


@servify
def test_get():
    "Testing GET request"
    
    expected = "GET / HTTP/1.1\nHost: localhost:%s\r\ncontent-length: 0\r\n"%(port_num) + \
    "content-type: application/x-www-form-urlencoded\r\naccept-encoding: compress, gzip\r\n" + \
    "accept: */*\r\nuser-agent: Python-httplib2/%s \r\n\n\n"%httplib2.__version__

    r = GET(hostname, headers=headers)
    assert r.startswith('GET /')
    assert r.strip() == expected.strip()

@servify
def test_post():
    "Testing POST request without body"
    expected = "POST\nvalue: store this\nDONE\n"
    r = POST(hostname, params={'value' : 'store this'}, accept=["text/plain","text/html"], async=False)
    assert r.startswith('POST /')
    assert "value=store+this" in r
    assert "accept: text/plain,text/html" in r
    
@servify
def test_post_image():
    "Testing POST with image without body"
    result = POST(hostname + "resize", files={'image' : {'file' : image, 'filename' : 'sample.jpg'}},
                  async=False)
    assert result.startswith('POST /resize')
    assert "multipart" in result

@servify
def test_get_unicode():
    "Testing GET with Unicode"
    
    expected = u"GET\nfoo\u2012: \u2012\nDONE\n".encode('utf-8')
    r = GET(unicode(hostname + "foo/"),params={u'foo\u2012' : u'\u2012'},
            headers={u"foo\u2012" : u"foo\u2012"})
    # unicode in params gets urlencoded
    assert r.startswith('GET /foo/?foo%E2%80%92=%E2%80%92')
    # unicode in headers gets stripped out. they can only contain ascii.
    assert u"foo: foo" in r

@servify
def test_post_unicode():
    "Testing POST Unicode without body"
    
    result = POST(unicode(hostname + "foo/"), 
                  params={u'foo\u2012' : u'\u2012'},
                  async=False)
    assert result.startswith('POST /foo/')
    expected = "foo%E2%80%92=%E2%80%92" # urlencoded 
    assert expected in result

@servify
def test_post_with_body():
    "Testing POST request with body"
    body = '<test><string>Some text</string></test>'
    r = POST(hostname, body=body, accept=["text/plain","text/html"], async=False )
    assert r.startswith('POST /')
    assert body in r

def main():
    import nose
    nose.main()

if __name__ == "__main__":
    main()
 
