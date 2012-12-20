
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


HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org/')

class PostmasterTestCase(unittest.TestCase):
    def setUp(self):
        super(PostmasterTestCase, self).setUp()
        postmaster.config.base_url = os.environ.get('PM_API_HOST', 'http://localhost:8000')
        postmaster.config.api_key = os.environ.get('PM_API_KEY', 'pp_MTp4cjdEYnJHTWhCbUR0Yi11a3FuU1czdHhLaWs')

    def testToken(self):
        token = postmaster.get_token()
        assert len(token) > 0

    def testTrack(self):
        resp = postmaster.track_by_reference('1ZW470V80310800043')
        assert 'history' in resp

    def testValidate(self):
        address = postmaster.AddressValidation(
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
        resp = shipment.track()
        assert resp is not None

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
