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

class HttpLibTestCase(unittest.TestCase):
    def setUp(self):
        super(HttpLibTestCase, self).setUp()
        base_url = os.environ.get('PM_API_HOST')
        #if api_base:
        #	stripe.base_url = base_url
        #postmaster.config.api_key = os.environ.get('PM_API_KEY', 'tGN0bIwXnHdwOa85VABjPdSn8nWY7G7I')
        postmaster.config.base_url = HTTPBIN

    def testEmptyPost(self):
        resp = HTTPTransport.post('post')
        self.assertEqual(resp['data'], '')
        self.assertDictEqual(resp['args'], {})
        self.assertEqual(resp['headers']['Content-Type'], 'application/json')
        self.assertEqual(resp['headers']['Accept'], 'application/json')
        self.assertEqual(resp['headers']['User-Agent'], postmaster.config.headers['User-Agent'])

    def testPost(self):
        resp = HTTPTransport.post(
            'post',
            data={
                'postmasterkey1': 'postmastervalue1',
                'postmasterkey2': 'postmastervalue2'
            },
            headers={
                'Postmastertestheader':'postmastertest'
            }
        )
        assert 'Postmastertestheader' in resp['headers']
        self.assertEqual(resp['headers']['Postmastertestheader'], 'postmastertest')
        self.assertEqual(resp['headers']['Content-Type'], 'application/json')
        self.assertEqual(resp['headers']['Accept'], 'application/json')
        self.assertEqual(resp['json']['postmasterkey1'], 'postmastervalue1')
        self.assertEqual(resp['json']['postmasterkey2'], 'postmastervalue2')

    def testEmptyGet(self):
        resp = HTTPTransport.get('get')
        assert 'data' not in resp
        self.assertDictEqual(resp['args'], {})
        self.assertEqual(resp['headers']['Content-Type'], 'application/json')
        self.assertEqual(resp['headers']['Accept'], 'application/json')
        self.assertEqual(resp['headers']['User-Agent'], postmaster.config.headers['User-Agent'])

    def testGet(self):
        resp = HTTPTransport.get(
            'get',
            data={
                'postmasterkey1': 'postmastervalue1',
                'postmasterkey2': 'postmastervalue2'
            },
            headers={
                'Postmastertestheader':'postmastertest'
            }
        )

        assert 'Postmastertestheader' in resp['headers']
        self.assertEqual(resp['headers']['Postmastertestheader'], 'postmastertest')
        self.assertEqual(resp['headers']['Content-Type'], 'application/json')
        self.assertEqual(resp['headers']['Accept'], 'application/json')
        self.assertEqual(resp['args']['postmasterkey1'], 'postmastervalue1')
        self.assertEqual(resp['args']['postmasterkey2'], 'postmastervalue2')
        assert 'data' not in resp

    def testEmptyPut(self):
        resp = HTTPTransport.put('put')
        self.assertEqual(resp['data'], '')
        self.assertDictEqual(resp['args'], {})
        self.assertEqual(resp['headers']['Content-Type'], 'application/json')
        self.assertEqual(resp['headers']['Accept'], 'application/json')
        self.assertEqual(resp['headers']['User-Agent'], postmaster.config.headers['User-Agent'])

    def testPut(self):
        resp = HTTPTransport.put(
            'put',
            data={
                'postmasterkey1': 'postmastervalue1',
                'postmasterkey2': 'postmastervalue2'
            },
            headers={
                'Postmastertestheader':'postmastertest'
            }
        )

        assert 'Postmastertestheader' in resp['headers']
        self.assertEqual(resp['headers']['Postmastertestheader'], 'postmastertest')
        self.assertEqual(resp['headers']['Content-Type'], 'application/json')
        self.assertEqual(resp['headers']['Accept'], 'application/json')
        self.assertEqual(resp['json']['postmasterkey1'], 'postmastervalue1')
        self.assertEqual(resp['json']['postmasterkey2'], 'postmastervalue2')

    def testEmptyDelete(self):
        resp = HTTPTransport.delete('delete')
        self.assertEqual(resp['data'], '')
        self.assertDictEqual(resp['args'], {})
        self.assertEqual(resp['headers']['Content-Type'], 'application/json')
        self.assertEqual(resp['headers']['Accept'], 'application/json')
        self.assertEqual(resp['headers']['User-Agent'], postmaster.config.headers['User-Agent'])

    def testDelete(self):
        resp = HTTPTransport.delete(
            'delete',
            data={
                'postmasterkey1': 'postmastervalue1',
                'postmasterkey2': 'postmastervalue2'
            },
            headers={
                'Postmastertestheader':'postmastertest'
            }
        )

        assert 'Postmastertestheader' in resp['headers']
        self.assertEqual(resp['headers']['Postmastertestheader'], 'postmastertest')
        self.assertEqual(resp['headers']['Content-Type'], 'application/json')
        self.assertEqual(resp['headers']['Accept'], 'application/json')
        self.assertEqual(resp['json']['postmasterkey1'], 'postmastervalue1')
        self.assertEqual(resp['json']['postmasterkey2'], 'postmastervalue2')

    def testStatusCodes(self):
        data = json.dumps({'message':'def'})
        self.assertRaises(APIError, HTTPTransport._decode, data, 500)
        self.assertRaises(InvalidDataError, HTTPTransport._decode, data, 400)
        self.assertRaises(AuthenticationError, HTTPTransport._decode, data, 401)
        self.assertRaises(PermissionError, HTTPTransport._decode, data, 403)

        try:
            HTTPTransport._decode(data, 400)
        except InvalidDataError as e:
            self.assertEqual(e.message, 'def')
            self.assertEqual(e.json_body, data)
        try:
            HTTPTransport._decode(data, 401)
        except AuthenticationError as e:
            self.assertEqual(e.message, 'def')
            self.assertEqual(e.json_body, data)
        try:
            HTTPTransport._decode(data, 403)
        except PermissionError as e:
            self.assertEqual(e.message, 'def')
            self.assertEqual(e.json_body, data)
