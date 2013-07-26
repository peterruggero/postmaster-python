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
                'company': 'Acme Inc.',
                'contact': 'Joe Smith',
                'line1': '720 Brazos St.',
                'city': 'Austin',
                'state': 'TX',
                'zip_code': '78701',
                'phone_no': '919-720-7941'
            },
            from_={
                'company': 'ASLS',
                'contact': 'Joe Smith',
                'line1': '1110 Algarita Ave.',
                'city': 'Austin',
                'state': 'TX',
                'zip_code': '78704',
                'phone_no': '919-720-7941'
            },
            packages=[{
                'weight': 1.5,
                'length': 10,
                'width': 6,
                'height': 8,
            }],
            carrier='ups',
            service='GROUND',
        )
        shipment2 = postmaster.Shipment.retrieve(shipment1.id)
        self.assertEqual(shipment1.id, shipment2.id)

    def testShipmentCreateInternational(self):
        shipment = postmaster.Shipment.create(
            to={
                'company': 'Hotel',
                'contact': 'Jan Nowak',
                'line1': 'Aleja ks Biskupa Juliusza Bursche 3',
                'city': 'Wisla',
                'state': 'TX',
                'zip_code': '43460',
                'phone_no': '33 855 47 00',
                'phone_ext': '+48',
                'country': 'PL',
                #'tax_id': '965-71-4343',
                #'residential': False,
            },
            from_={
                'company': 'ASLS',
                'contact': 'Joe Smith',
                'line1': '1110 Algarita Ave. 2',
                'city': 'Austin',
                'state': 'TX',
                'zip_code': '78704',
                'phone_no': '919-720-7941'
            },
            packages=[{
                'weight': 3.5,
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
            carrier='ups',
            service='INTL_PRIORITY',
        )
        customs = shipment._data['packages'][0]['customs']
        assert shipment._data['to']['country'] == 'PL'
        assert shipment._data['service'] == 'INTL_PRIORITY'
        assert customs['type'] == 'Gift'
        assert customs['contents'][0]['value'] == '15'

    def testShipmentTrack(self):
        shipment = postmaster.Shipment.create(
            to={
                'company': 'Acme Inc.',
                'contact': 'Joe Smith',
                'line1': '720 Brazos St.',
                'city': 'Austin',
                'state': 'TX',
                'zip_code': '78701',
                'phone_no': '919-720-7941'
            },
            from_={
                'company': 'ASLS',
                'contact': 'Joe Smith',
                'line1': '1110 Algarita Ave 2.',
                'city': 'Austin',
                'state': 'TX',
                'zip_code': '78704',
                'phone_no': '919-720-7941'
            },
            packages=[{
                'weight': 1.5,
                'length': 10,
                'width': 6,
                'height': 8,
            }],
            carrier='ups',
            service='GROUND',
        )
        shipment.track()

    def testTimes(self):
        resp = postmaster.get_transit_time(
            '78704',
            '78701',
            '5',
            'ups'
        )
        assert resp is not None

    def testRates(self):
        resp = postmaster.get_rate(
            'ups',
            '78704',
            '5',
            '78701',
        )
        assert resp is not None

    def testPackageCreate(self):
        box = postmaster.Package.create(width=5, height=5, length=5, weight=10)
        assert box._data['weight_units'] == 'LB'
        assert box._data['size_units'] == 'IN'
        boxes = postmaster.Package.list()
        self.assertIn('width', boxes._data['results'][0])



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
