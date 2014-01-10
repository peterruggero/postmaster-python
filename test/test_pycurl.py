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


HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org/')

class PyCurlTestCase(UrlLib2TestCase):
    def setUp(self):
        super(PyCurlTestCase, self).setUp()
        postmaster.http.HTTP_LIB = 'pycurl'
        import pycurl
        postmaster.http.pycurl = pycurl

    def testDelete(self):
        pass
