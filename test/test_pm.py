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
        postmaster.config.api_key = os.environ.get('PM_API_KEY', 'tt_NzAwMTpfOFFzNGxmQ29NaGE4VkJDSTdOdF8zaXk2UTQ')

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
            line1='1110 Algarita Ave.',
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
            from_={
                'company':'ASLS',
                'contact':'Joe Smith',
                'line1':'1110 Algarita Ave.',
                'city':'Austin',
                'state':'TX',
                'zip_code':'78704',
                'phone_no':'919-720-7941'
            },
            packages={
                'weight':1.5,
                'length':10,
                'width':6,
                'height':8,
            },
            carrier='usps',
            service='2DAY',
        )
        shipment2 = postmaster.Shipment.retrieve(shipment1.id)
        self.assertEqual(shipment1.id, shipment2.id)

    def testShipmentCreateInternational(self):
        shipment = postmaster.Shipment.create(
            to={
                'company': 'Acme Inc.',
                'contact': 'Joe Smith',
                'line1': '701 Brazos St.',
                'line2': 'Elevator at end of hallway',
                'line3': 'Spot with umbrella on the roof',
                'city': 'Austin',
                'state': 'TX',
                'zip_code': '78701',
                'phone_no': '555-123-4452',
                'phone_ext': '555',
                'country': 'FR',
                'tax_id': '965-71-4343',
                'residential': False,
            },
            packages=[{
                'weight': 1.5,
                'length': 10,
                'width': 6,
                'height': 8,
                'customs': {
                    'type': 'Gift',
                    'contents': [{
                            'description': 'description',
                            'value': '15',
                            'weight': 2.5,
                            'weight_units': 'LB',
                            'quantity': 1,
                            'hs_tariff_number': '060110',
                            'country_of_origin': 'AI',
                    }, ],
                },
            }, ],
            carrier='usps',
            service='INTL_SURFACE',
        )
        customs = shipment._data['packages'][0]['customs']
        assert shipment._data['to']['country'] == 'FR'
        assert shipment._data['service'] == 'INTL_SURFACE'
        assert customs['type'] == 'Gift'
        assert customs['contents'][0]['value'] == '15'

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
            from_={
                'company':'ASLS',
                'contact':'Joe Smith',
                'line1':'1110 Algarita Ave.',
                'city':'Austin',
                'state':'TX',
                'zip_code':'78704',
                'phone_no':'919-720-7941'
            },
            packages=[{
                'weight':1.5,
                'length':10,
                'width':6,
                'height':8,
                }],
            carrier='usps',
            service='2DAY',
        )
        shipment.track()

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
        postmaster.http.HTTP_LIB = 'pycurl'
        super(PostmasterTestCase_Pycurl, self).setUp()



if __name__ == '__main__':
    unittest.main()
