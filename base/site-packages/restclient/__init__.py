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


#!/usr/bin/python

"""
REST client convenience library

This module contains everything that's needed for a nice, simple REST client.

the main function it provides is rest_invoke(), which will make an HTTP
request to a REST server. it allows for all kinds of nice things like:

    * alternative verbs: POST, PUT, DELETE, etc.
    * parameters
    * file uploads (multipart/form-data)
    * proper unicode handling
    * Accept: headers
    * ability to specify other headers

this library is mostly a wrapper around the standard urllib and
httplib2 functionality, but also includes file upload support via a
python cookbook recipe
(http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/146306) and
has had additional work to make sure high unicode characters in the
parameters or headers don't cause any UnicodeEncodeError problems. 

Joe Gregario's httplib2 library is required. It can be easy_installed, or downloaded
nose is required to run the unit tests.

CHANGESET:
  * 2009-10-08 - Anders - merged Taras Mankovski's patch for adding body to POST/PUT and test improvements
  * 2009-10-08 - Anders - merged Peter Fein's patch for specifying mimetypes on file uploads
  * 2007-06-13 - Anders - added experimental, partial support for HTTPCallback
  * 2007-03-28 - Anders - merged Christopher Hesse's patches for fix_params and to eliminate
                          mutable default args
  * 2007-03-14 - Anders - quieted BaseHTTPServer in the test suite
  * 2007-03-06 - Anders - merged Christopher Hesse's bugfix and self-contained test suite
  * 2006-12-01 - Anders - switched to httplib2. Improved handling of parameters and made it
                          stricter about unicode in headers (only ASCII is allowed). Added
                          resp option. More docstrings.
  * 2006-03-23 - Anders - working around cherrypy bug properly now by being more
                          careful about sending the right 
  * 2006-03-17 - Anders - fixed my broken refactoring :) also added async support
n                          and we now use post_multipart for everything since it works
                          around a cherrypy bug.
  * 2006-03-10 - Anders - refactored and added GET, POST, PUT, and DELETE
                          convenience functions
  * 2006-02-22 - Anders - handles ints in params + headers correctly now

"""


import urllib2,urllib, mimetypes, types, thread, httplib2

__version__ = "0.9.10"

def post_multipart(host, selector, method,fields, files, headers=None,return_resp=False, body=None):
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
    """
    if headers is None: headers = {}
    content_type, body = encode_multipart_formdata(fields, files, body)
    h = httplib2.Http()
    headers['Content-Length'] = str(len(body))
    headers['Content-Type']   = content_type
    resp, content = h.request("http://%s%s" % (host,selector),method,body,headers)
    if return_resp:
        return resp, content
    else:
        return content

def encode_multipart_formdata(fields, files, body):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    # add body to the beginning
    if body:
        L.append(body)
        L.append('')
        L.append(str(body))
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(str(value))
    for (key, filename, value, mimetype) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        if mimetype is None:
            content_type=get_content_type(filename)
        else:
            content_type=mimetype
        L.append('Content-Type: %s' % content_type)
        L.append('')
        L.append(str(value))
    L.append('--' + BOUNDARY + '--')
    L.append('')
    L = [str(l) for l in L]

    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


def GET(url,params=None,files=None,accept=[],headers=None,async=False,resp=False):
    """ make an HTTP GET request.

    performs a GET request to the specified URL and returns the body of the response.
    
    in addition, parameters and headers can be specified (as dicts). a list of mimetypes
    to accept may be specified.

    if async=True is passed in, it will perform the request in a new thread
    and immediately return nothing.

    if resp=True is passed in, it will return a tuple of an httplib2 response object
    and the content instead of just the content. 
    """
    return rest_invoke(url=url,method=u"GET",params=params,files=files,accept=accept,headers=headers,async=async,resp=resp)

def POST(url,**kwargs):
    """ make an HTTP POST request.

    url - string to make post to
    params - string to include with post ( optional, params and body are mutually exlusive )
    body - string to include with post ( optional, params and body are mutually exlusive )
    accept - list of mimetypes to accept
    files - files to upload may be specified in dict format {'file' : file object, 'filename' : filename}
    headers - dict of headers to include
    async - boolean set to False to wait for response and have it return body of the response
    resp - boolean True will return a tuple of a httplib2 response object and the content instead of just content 
    """
    kwargs['method'] = u'POST'
    return rest_invoke(url=url,**kwargs)

def PUT(url,**kwargs):
    """ make an HTTP PUT request.

    url - string to make post to
    params - string to include with post ( optional, params and body are mutually exlusive )
    body - string to include with post ( optional, params and body are mutually exlusive )
    accept - list of mimetypes to accept
    files - files to upload may be specified in dict format {'file' : file object, 'filename' : filename}
    headers - dict of headers to include
    async - boolean set to False to wait for response and have it return body of the response
    resp - boolean True will return a tuple of a httplib2 response object and the content instead of just content 
    """
    kwargs['method'] = u'PUT'
    return rest_invoke(url=url,**kwargs)

def DELETE(url,**kwargs):
    """ make an HTTP DELETE request.

    url - string to make post to
    params - string to include with post ( optional, params and body are mutually exlusive )
    body - string to include with post ( optional, params and body are mutually exlusive )
    accept - list of mimetypes to accept
    headers - dict of headers to include
    async - boolean set to False to wait for response and have it return body of the response
    resp - boolean True will return a tuple of a httplib2 response object and the content instead of just content 
 
    by default DELETE() performs the request in a new thread and returns (nothing) immediately.

    To wait for the response and have it return the body of the response, specify async=False. 

    if resp=True is passed in, it will return a tuple of an httplib2 response object
    and the content instead of just the content. 
    """
    
    kwargs['method'] = u'DELETE'        
    return rest_invoke(url=url,**kwargs)

def rest_invoke(url, **kwargs):
    """ make an HTTP request with all the trimmings.

    rest_invoke() will make an HTTP request and can handle all the
    advanced things that are necessary for a proper REST client to handle:

    * alternative verbs: POST, PUT, DELETE, etc.
    * parameters
    * file uploads (multipart/form-data)
    * proper unicode handling
    * Accept: headers
    * ability to specify other headers

    rest_invoke() returns the body of the response that it gets from
    the server.

    rest_invoke() does not try to do any fancy error handling. if the
    server is down or gives an error, it will propagate up to the
    caller.

    this function expects to receive unicode strings. passing in byte
    strings risks double encoding.

    parameters:

    url: the full url you are making the request to
    method: HTTP verb to use. defaults to GET
    params: dictionary of params to include in the request
    files: dictionary of files to upload. the structure is

        param : {'file' : file object, 'filename' : filename, 'mimetype': mimetype (optional)}

    accept: list of mimetypes to accept in order of preference. defaults to '*/*'
    headers: dictionary of additional headers to send to the server
    async: Boolean. if true, does request in new thread and nothing is returned
    resp: Boolean. if true, returns a tuple of response,content. otherwise returns just content
    httpcallback: None. an HTTPCallback object (see http://microapps.org/HTTP_Callback). If specified, it will
                  override the other params.
    
    """
    if kwargs.get('async',False):
        method  = kwargs.get('method', u'GET')
        params  = kwargs.get('params', None)
        files   = kwargs.get('files', None)
        accept  = kwargs.get('accept', [])
        headers = kwargs.get('headers', None)
        resp    = kwargs.get('resp', None)
        httpcallback = kwargs.get('httpcallback', None)
        body    = kwargs.get('body', None)
        thread.start_new_thread(_rest_invoke,(url, method, params, files, accept, headers, resp, httpcallback, body))
    else:
        return _rest_invoke(url,**kwargs)

def _rest_invoke(url,**kwargs):
    method  = kwargs.get('method', u'GET')
    params  = kwargs.get('params', {})
    files   = kwargs.get('files', {})
    accept  = kwargs.get('accept', [])
    headers = kwargs.get('headers', {})
    body    = kwargs.get('body', None)
    resp    = kwargs.get('resp', False)
    httpcallback = kwargs.get('httpcallback', None)
    
    if httpcallback is not None:
        method = httpcallback.method
        url    = httpcallback.url
        body   = httpcallback.body
        if httpcallback.queryString != "":
            if "?" not in url:
                url += "?" + httpcallback.queryString
            else:
                url += "&" * httpcallback.queryString
        ps = httpcallback.params
        for (k,v) in ps:
            params[k] = v
        hs = httpcallback.headers
        for (k,v) in hs:
            headers[k] = v

        if httpcallback.username or httpcallback.password:
            print "warning: restclient can't handle HTTP auth yet"
        if httpcallback.redirections != 5:
            print "warning: restclient doesn't support HTTPCallback's restrictions yet"
        if httpcallback.follow_all_redirects:
            print "warning: restclient doesn't support HTTPCallback's follow_all_redirects_yet"
        
    headers = add_accepts(accept,headers)
    if files:
        return post_multipart(extract_host(url),extract_path(url),
                              method,
                              unpack_params(fix_params(params)),
                              unpack_files(fix_files(files)),
                              fix_headers(headers),
                              resp,body)
    else:
        return non_multipart(fix_params(params), extract_host(url),
                             method, extract_path(url), fix_headers(headers),resp,body)

def non_multipart(params,host,method,path,headers,return_resp,body):
    params = urllib.urlencode(params)
    if method == "GET":
        headers['Content-Length'] = '0'
        if params:
            # put the params into the url instead of the body
            if "?" not in path:
                path += "?" + params
            else:
                if path.endswith('?'):
                    path += params
                else:
                    path += "&" + params
            params = ""       
    else:
        if body:
            headers['Content-Length'] = str(len(params) + len(body))
        else:
            headers['Content-Length'] = str(len(params))
    if not headers.has_key('Content-Type'):
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
    h = httplib2.Http()
    url = "http://%s%s" % (host,path)
    if method != 'GET' and body:
        resp,content = h.request(url,method.encode('utf-8'),body.encode('utf-8'),headers)
    else:
        resp, content = h.request(url,method.encode('utf-8'),params.encode('utf-8'),headers)

    if return_resp:
        return resp,content
    else:
        return content

def extract_host(url):
    return my_urlparse(url)[0]

def extract_path(url):
    return my_urlparse(url)[1]

def my_urlparse(url):
    (scheme,host,path,ps,query,fragment) = urllib2.urlparse.urlparse(url)
    if ps:
        path += ";" + ps
    if query:
        path += "?" + query

    return (host,path)
        
def unpack_params(params):
    return [(k,params[k]) for k in params.keys()]

def unpack_files(files):
    return [(k,files[k]['filename'],files[k]['file'],files[k].get('mimetype', None)) 
            for k in files.keys()]

def add_accepts(accept=None,headers=None):
    if accept  is None: accept  = []
    if headers is None: headers = {}
    
    if accept:
        headers['Accept'] = ','.join(accept)
    else:
        headers['Accept'] = '*/*'
    return headers

def fix_params(params=None):
    if params is None: params = {}
    for k in params.keys():
        if type(k) not in types.StringTypes:
            new_k = str(k)
            params[new_k] = params[k]
            del params[k]
        else:
            try:
                k = k.encode('ascii')
            except UnicodeEncodeError:
                new_k = k.encode('utf8')
                params[new_k] = params[k]
                del params[k]
            except UnicodeDecodeError:
                pass

    for k in params.keys():
        if type(params[k]) not in types.StringTypes:
            params[k] = str(params[k])
        try:
            v = params[k].encode('ascii')                
        except UnicodeEncodeError:
            new_v = params[k].encode('utf8')
            params[k] = new_v
        except UnicodeDecodeError:
            pass

    return params

def fix_headers(headers=None):
    if headers is None: headers = {}
    for k in headers.keys():
        if type(k) not in types.StringTypes:
            new_k = str(k)
            headers[new_k] = headers[k]
            del headers[k]
        if type(headers[k]) not in types.StringTypes:
            headers[k] = str(headers[k])        
        try:
            v = headers[k].encode('ascii')                
            k = k.encode('ascii')
        except UnicodeEncodeError:
            new_k = k.encode('ascii','ignore')
            new_v = headers[k].encode('ascii','ignore')
            headers[new_k] = new_v
            del headers[k]
    return headers

def fix_files(files=None):
    if files is None: files = {}
    # fix keys in files
    for k in files.keys():
        if type(k) not in types.StringTypes:
            new_k = str(k)
            files[new_k] = files[k]
            del files[k]
        try:
            k = k.encode('ascii')
        except UnicodeEncodeError:
            new_k = k.encode('utf8')
            files[new_k] = files[k]
            del files[k]                
    # second pass to fix filenames
    for k in files.keys():
        try:
            f = files[k]['filename'].encode('ascii')
        except UnicodeEncodeError:
            files[k]['filename'] = files[k]['filename'].encode('utf8')
    return files


if __name__ == "__main__":
    print rest_invoke("http://localhost:9090/",
                      method="POST",params={'value' : 'store this'},accept=["text/plain","text/html"],async=False)
    image = open('sample.jpg').read()
    r = rest_invoke("http://resizer.ccnmtl.columbia.edu/resize",method="POST",files={'image' : {'file' : image, 'filename' : 'sample.jpg'}},async=False)
    out = open("thumb.jpg","w")
    out.write(r)
    out.close()
    GET("http://resizer.ccnmtl.columbia.edu/")
    r = POST("http://resizer.ccnmtl.columbia.edu/resize",files={'image' : {'file' : image, 'filename' : 'sample.jpg'}},async=False)    
    # evil unicode tests
    print rest_invoke(u"http://localhost:9090/foo/",params={u'foo\u2012' : u'\u2012'},
                      headers={u"foo\u2012" : u"foo\u2012"})
    
    r = rest_invoke(u"http://localhost:9090/resize",method="POST",files={u'image\u2012' : {'file' : image, 'filename' : u'samp\u2012le.jpg'}},async=False)    
