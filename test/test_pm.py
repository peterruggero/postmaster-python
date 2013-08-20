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
        postmaster.config.api_key = os.environ.get('PM_API_KEY', 'tt_MTpBdl9rdTBWSUIwN0tVN1dWT2dwV3VBYVUySjA')

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
            packages=[{
                'weight':1.5,
                'length':10,
                'width':6,
                'height':8,
            }],
            carrier='usps',
            service='2DAY',
        )
        shipment2 = postmaster.Shipment.retrieve(shipment1.id)

        self.assertEqual(shipment1.id, shipment2.id)
        self.assertDictEqual(shipment1._data, shipment2._data)

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
            '78704',
            '28806',
            '5',
            'ups',
        )
        assert resp is not None

        resp = postmaster.get_rate(
            '78704',
            '28806',
            '5',
        )
        assert resp is not None
        assert 'best' in resp

    def testPackageCreate(self):
        box = postmaster.Package.create(width=5, height=5, length=5, weight=10)
        self.assertEqual(box.weight_units, 'LB')
        self.assertEqual(box.dimension_units, 'IN')
        self.assertIsInstance(box.id, int)
        return box

    def testPackageCreateFail(self):
        # fail
        with self.assertRaises(postmaster.InvalidDataError):
            postmaster.Package().create(1, 2, '345asd')

    def testShipmentVoid(self):
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
        # succeed
        status = shipment.void()
        self.assertTrue(status)
        # fail
        status = postmaster.Shipment(id=893457898937834589).void()
        self.assertFalse(status)

    def testListShipments(self):
        self.testShipmentCreateRetrive()
        shipments, cursor, prev_cursor = postmaster.Shipment.list()
        self.assertGreater(len(shipments), 0)
        self.assertIsInstance(cursor, unicode)
        self.assertIsInstance(prev_cursor, unicode)

    def testListPackages(self):
        for _ in range(11):
            self.testPackageCreate()
        packages, cursor, prev_cursor = postmaster.Package.list(limit=6)
        self.assertEqual(len(packages), 6)
        self.assertIsInstance(cursor, unicode)
        self.assertIsInstance(prev_cursor, unicode)

        packages, cursor, prev_cursor = postmaster.Package.list(cursor=cursor, limit=5)
        self.assertEqual(len(packages), 5)

    def testRemovePackage(self):
        package = self.testPackageCreate()
        id_ = package.id
        package = postmaster.Package.retrieve(package_id=id_)
        self.assertIsInstance(package.id, int)
        self.assertTrue(package.remove())
        package = postmaster.Package.retrieve(package_id=id_)
        self.assertIsNone(package)


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
