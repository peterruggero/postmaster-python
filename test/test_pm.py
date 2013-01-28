
import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise

import postmaster
from postmaster.http import *


HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org/')

class PostmasterTestCase_Urllib2(unittest.TestCase):
    def setUp(self):
        super(PostmasterTestCase_Urllib2, self).setUp()
        postmaster.http.HTTP_LIB = 'urllib2'
        postmaster.config.base_url = os.environ.get('PM_API_HOST', 'http://localhost:8000')
        postmaster.config.api_key = os.environ.get('PM_API_KEY', 'pp_MTp4cjdEYnJHTWhCbUR0Yi11a3FuU1czdHhLaWs')

    def testToken(self):
        token = postmaster.get_token()
        assert len(token) > 0

    def testTrack(self):
        resp = postmaster.track_by_reference('1ZW470V80310800043')
        assert 'history' in resp

    def testValidate(self):
        address = postmaster.Address(
            company='ASLS',
            contact='Joe Smith',
            address=['1110 Algarita Ave.'],
            city='Austin',
            state='TX',
            zip_code='78704',
        )
        resp = address.validate()
        assert resp is not None

    def testShipmentCreateRetrive(self):
        shipment1 = postmaster.Shipment.create(
            to={
                'company':'ASLS',
                'contact':'Joe Smith',
                'line1':'1110 Algarita Ave.',
                'city':'Austin',
                'state':'TX',
                'zip_code':'78704',
                'phone_no':'919-720-7941'
            },
            package={
                'weight':1.5,
                'length':10,
                'width':6,
                'height':8,
            },
            carrier='ups',
            service='2DAY',
        )
        shipment2 = postmaster.Shipment.retrieve(shipment1.id)
        self.assertEqual(shipment1.id, shipment2.id)

    def testShipmentTrack(self):
        shipment = postmaster.Shipment.create(
            to={
                'company':'ASLS',
                'contact':'Joe Smith',
                'line1':'1110 Algarita Ave.',
                'city':'Austin',
                'state':'TX',
                'zip_code':'78704',
                'phone_no':'919-720-7941'
            },
            package={
                'weight':1.5,
                'length':10,
                'width':6,
                'height':8,
                },
            carrier='fedex',
            service='2DAY',
        )
        # how to test track ?
        #resp = shipment.track()
        #assert resp is not None

    def testTimes(self):
        resp = postmaster.get_transit_time(
            '78704',
            '28806',
            '5',
            'ups'
        )
        assert resp is not None

    def testRates(self):
        resp = postmaster.get_rate(
            'ups',
            '78704',
            '5',
            '28806',
        )
        assert resp is not None


class PostmasterTestCase_Urlfetch(PostmasterTestCase_Urllib2):
    def setUp(self):
        super(PostmasterTestCase_Urlfetch, self).setUp()
        from google.appengine.api import apiproxy_stub_map, urlfetch_stub

        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
        apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', urlfetch_stub.URLFetchServiceStub())
        postmaster.http.HTTP_LIB = 'urlfetch'


class PostmasterTestCase_Pycurl(PostmasterTestCase_Urllib2):
    def setUp(self):
        super(PostmasterTestCase_Pycurl, self).setUp()
        postmaster.http.HTTP_LIB = 'pycurl'

if __name__ == '__main__':
    unittest.main()
