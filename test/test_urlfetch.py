import os
import sys
import unittest
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise

import postmaster
from postmaster.http import *
from test_urllib2 import UrlLib2TestCase

class UrlFetchTestCase(UrlLib2TestCase):
    def setUp(self):
        super(UrlFetchTestCase, self).setUp()
        from google.appengine.api import (apiproxy_stub_map, urlfetch_stub,
            urlfetch)

        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
        apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', urlfetch_stub.URLFetchServiceStub())
        postmaster.http.HTTP_LIB = 'urlfetch'
        postmaster.http.urlfetch = urlfetch

    def testDelete(self):
        # empty because in urlfetch you can't pass body in DELETE method
        # issue : http://code.google.com/p/googleappengine/issues/detail?id=601
        pass
