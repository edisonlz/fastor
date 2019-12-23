# -*- coding: utf-8 -*-
"""
 Copyright 2005 Spike^ekipS <spikeekips@gmail.com>

	This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import sys, urllib, urllib2, urlparse
from xml.dom.ext.reader import Sax2
import StringIO

MIMETYPE_XML = (
	"application/atomserv+xml",
	"application/beep+xml",
	"application/docbook+xml",
	"application/rdf+xml",
	"application/rss+xml",
	"application/xhtml+xml",
	"application/xml",
	"application/xml-dtd",
	"application/xml-external-parsed-entity",
	"application/vnd.google-earth.kml+xml",
	"application/vnd.irepository.package+xml",
	"application/vnd.mozilla.xul+xml",
	"application/vnd.pwg-xhtml-print+xml",
	"application/vnd.sun.xml.calc",
	"application/vnd.sun.xml.calc.template",
	"application/vnd.sun.xml.draw",
	"application/vnd.sun.xml.draw.template",
	"application/vnd.sun.xml.impress",
	"application/vnd.sun.xml.impress.template",
	"application/vnd.sun.xml.math",
	"application/vnd.sun.xml.writer",
	"application/vnd.sun.xml.writer.global",
	"application/vnd.sun.xml.writer.template",
	"application/vnd.uplanet.alert-wbxml",
	"application/vnd.uplanet.bearer-choice-wbxml",
	"application/vnd.uplanet.cacheop-wbxml",
	"application/vnd.uplanet.channel-wbxml",
	"application/vnd.uplanet.list-wbxml",
	"application/vnd.uplanet.listcmd-wbxml",
	"application/vnd.wap.wbxml",
	"image/svg+xml",
)

def parse_query (query) :
	__queries = dict()
	__queries.update(
		[urllib.splitvalue(i) for i in query.split("&") if i.strip()]
	)

	return __queries

def join_query (query_parsed) :
	__d = list()
	for k, v in query_parsed.items() :
		if not v : v = ""

		__d.append(
			"%s=%s" % (
				urllib.quote(str(k).strip(), ""),
				urllib.quote(str(v).strip(), "")
			)
		)

	return "&".join(__d)

class URLCollection (object) :
	parsed = dict()

	def __init__ (self, url) :
		self.url = url

		(
			self.parsed["scheme"],
			self.parsed["netloc"],
			self.parsed["path"],
			self.parsed["params"],
			self.parsed["query"],
			self.parsed["fragment"],
		) = urlparse.urlparse(url)

		self.parsed["query_parsed"] = parse_query(self.parsed["query"])

	def __str__ (self) :
		return urlparse.urlunparse(
			(
				self.parsed["scheme"],
				self.parsed["netloc"],
				self.parsed["path"],
				self.parsed["params"],
				self.parsed["query"],
				self.parsed["fragment"],
			)
		)

	def copy (self) :
		return URLCollection(self.url)

	def __getitem__ (self, k) :
		return self.parsed.get(k)

	def __setitem__ (self, k, v) :
		self.parsed[k] = v
		return None

	def update_query (self, queries=dict()) :
		self.parsed["query_parsed"].update(queries)
		self.parsed["query"] = join_query(self.parsed["query_parsed"])

class ResponseErrorCollection (object) :

	def __init__ (self, addinfourl) :
		self.addinfourl = addinfourl

		self.parsed = None

		self.headers = dict()
		self.url = str()
		self.fp = None
		self.code = None
		self.status = self.code

		self.readline = lambda: None
		self.readlines = lambda: None
		self.fileno = lambda: None
		self.next = lambda:None

		self.__repr__ = self.addinfourl.__repr__
		self.close = lambda: None
		self.info = dict()
		self.geturl = lambda: None

class ResponseCollection (object) :

	def __init__ (self, addinfourl) :
		self.addinfourl = addinfourl

		self.parsed = None

		self.headers = self.addinfourl.headers
		self.url = self.addinfourl.url
		self.fp = StringIO.StringIO(self.addinfourl.read())
		self.code = self.addinfourl.code
		self.status = self.code

		self.readline = self.fp.readline
		self.readlines = self.fp.readlines
		self.fileno = lambda: None
		self.next = self.fp.next

		self.__repr__ = self.addinfourl.__repr__
		self.close = self.addinfourl.close
		self.info = self.addinfourl.info
		self.geturl = self.addinfourl.geturl

		self.parse_content()

	def parse_content (self) :
		self.parsed = self.read()

		# parse xml document
		if self.headers.get("content-type") in MIMETYPE_XML :
			reader = Sax2.Reader()
			self.parsed = reader.fromStream(self.fp)
			self.fp.seek(0)

	def read (self) :
		__c = self.fp.read()
		self.fp.seek(0)

		return __c

class RequestCollection (urllib2.Request) :

	method = None

	def get_method (self) :
		if self.method is None :
			return urllib2.Request.get_method(self)
		else :
			return self.method

	def set_method (self, method) :
		self.method = method.upper()

def decorator_handle_request (func) :
	def wrapper (self, *args, **kwargs) :
		return self.do_request(func.func_name, *args, **kwargs)

	return wrapper

class HTTPCollection (object) :

	def __init__ (self, url) :
		self.url = URLCollection(url)

		self.data = None
		self.auth_method = "Basic"
		self.auth_realm = None
		self.auth_handler = None

	def add_data (self, data) :
		if isinstance(data, basestring) :
			self.data = parse_query(data)
		elif isinstance(data, dict) :
			self.data = data

	def __get_auth_realm (self) :
		try :
			urllib2.urlopen(str(self.url))
		except urllib2.URLError, e :
			raise
		except urllib2.HTTPError, e :
			if e.code == 401 :
				if e.headers.has_key("www-authenticate") :
					import re
					(__method, __realm, ) = \
						re.compile("(\w+).*realm=[\"\\\"](.*)[\"\\\"]").findall(
							e.headers.get("www-authenticate", "")
						)[0]
		else :
			__method = "Basic"
			__realm = ""

		return (__method, __realm, )

	def add_auth (self, username, password) :
		if not self.auth_realm :
			try :
				(self.auth_method, self.auth_realm, ) = self.__get_auth_realm()
			except :
				return False

		self.auth_handler = \
			getattr(urllib2, "HTTP%sAuthHandler" % self.auth_method.capitalize())()
		self.auth_handler.add_password(
			self.auth_realm,
			str(self.url),
			username,
			password
		)

		return True

	def do_request (self, method) :
		__data = None
		__url = self.url.copy()

		if self.data :
			if method != "GET" :
				__data = self.data
			else :
				__url.update_query(self.data)

		self.request = RequestCollection(url=str(__url))
		self.request.set_method(method)

		if __data :
			self.request.add_data(__data)

		if self.auth_handler :
			opener = urllib2.build_opener(self.auth_handler)
		else :
			opener = urllib2.build_opener()

		try :
			__response = opener.open(self.request)
		except Exception, __response :
			if isinstance(__response, urllib2.HTTPError) :
				return ResponseCollection(__response)
			else :
				return ResponseErrorCollection(__response)
		else :
			return ResponseCollection(__response)

	@decorator_handle_request
	def GET (self, data=None) : pass

	@decorator_handle_request
	def POST (self, data=None) : pass

	@decorator_handle_request
	def PUT (self, data=None) : pass

	@decorator_handle_request
	def DELETE (self, data=None) : pass

if __name__ == "__main__" :
	hc = HTTPCollection("https://api.del.icio.us0/v1/posts/add?")
	hc.add_data({
		"url" : "http://dirdirdir.com",
		"description" : "dfjla",
	})
	hc.add_auth("spikeekips", "abu333")
	__r = hc.GET()

	print __r.status

	#hc = HTTPCollection("http://lab.miwing.com?dkfaj=dfka&dir=1&dir2=2")
	#hc.add_auth("spikeekips@gmail.com", "abu333")
	#print hc.GET()

	sys.exit()

	hc = HTTPCollection("http://openapi.naver.com/search")
	hc.add_data({
		"key" : "20bedfce2ed6b1b99d5525ed3c3ddfdf",
		"target" : "blog",
		"query" : "오마이뉴스",
		"display" : "10",
	})
	print hc.GET().read()

	sys.exit()


__author__ =  "Spike^ekipS <spikeekips@gmail.com>"
__version__=  "0.1"
__nonsense__ = ""

__file__ = "collection.py"


