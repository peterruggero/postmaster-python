# Postmaster Python bindings
# API docs at http://postmaster.io/docs
# Author: Jesse Lovelace <jesse@postmaster.io>

from .version import *
from .http import *
from .conf import config

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise


class PostmasterObject(object):
    """
    Base object for Postmaster.  Allows slightly easlier access to data and
    some REST-like opertations.
    """
    
    ARGS = []
    PATH = None
    
    def __init__(self, **kwargs):
        if self.ARGS:
            for k in kwargs.iterkeys():
                if not k in self.ARGS:
                    raise TypeError('%s is an invalid argument for %s.' % (k, self.__class__.__name__))
                
        self._data = kwargs

    def __getattr__(self, name):
        if not name in self._data:
            raise AttributeError("Cannot find attribute.")
        
        return self._data[name]
        
    def __repr__(self):
        return '<postmaster.%s at %s> JSON: %s' % (self.__class__.__name__, id(self), self._data)

    def put(self, id_=None, action=None):
        """
        Put object to server.
        """
        if id_:
            response = HTTPTransport.put(
                action and '%s/%s/%s' % (self.PATH, id_, action) or \
                    '%s/%s' % (self.PATH, id_),
                self._data, headers=config.headers)
        else:
            response = HTTPTransport.post(self.PATH, self._data, headers=config.headers)
        return response
        
    def get(self, id_=None, action=None, params=None):
        """
        Get object(s) from server.
        """
        
        if id_:
            response = HTTPTransport.get(
                action and '%s/%s/%s' % (self.PATH, id_, action) or \
                    '%s/%s' % (self.PATH, id_), params, headers=config.headers)
        else:
            response = HTTPTransport.get(
                self.PATH, params, headers=config.headers)
        return response
    
class Tracking(PostmasterObject):
    pass

class Rate(PostmasterObject):
    pass

class TimeInTransit(PostmasterObject):
    pass

class AddressValidation(PostmasterObject):

    PATH = '/api/v1/validate'

    @classmethod
    def create(cls, company=None, contact=None, address=[], city=None, state=None, zip_code=None, country=None):
        address_obj = cls()
        data = {}
        data['company'] = company
        data['contact'] = contact
        data['line1'] = address[0]
        if len(address) > 1:
            data['line2'] = address[1]
        if len(address) > 2:
            data['line3'] = address[2]
        data['city'] = city
        data['state'] = state
        data['zip_code'] = zip_code
        data['country'] = country
        address_obj._data = data
        return address_obj

    def validate(self):
        return self.put()


class Shipment(PostmasterObject):
    
    PATH = '/api/v1/shipments'
    
    @classmethod
    def create(cls, to, package, from_=None, carrier=None, service=None, reference=None):
        """
        Create a new shipment.  
        
        Arguments:
        
         * to (required) - a dict representing the ship-to address: 
           * company
           * contact
           * street - a list of strings defining the street address
           * city
           * state
           * zip
         * package (required) - a dict (or list of dicts) representing the package:
           * value
           * weight
           * dimentions
         * from (optional) - a dict representing the ship-from address.  Will use default
           for account if not provided.
        """
        shipment = Shipment()
        shipment._data = {
            'to':to,
            'from':from_,
            'package':package,
            'carrier':carrier,
            'service':service,
            'reference':reference
        }
        resp = shipment.put()
        shipment.id = resp['id']
        return shipment
       
    @classmethod
    def retrieve(cls, package_id):
        """
        Retrieve a package by ID.
        """
        shipment = Shipment()
        shipment._data = shipment.get(package_id)
        return shipment
       
    def track(self):
        """
        Track a shipment (from an object)
        """
        return Tracking(**self.get(self.id, 'track'))
        
    def void(self):
        """
        Void a shipment (from an object)
        """
        self.put(self.id, 'void')

def track_by_reference(tracking_number):
    """
    Track any package by it's carrier-specific tracking number.
    Note: if this package was not shipped my Postmaster
    the resulting data will not contain detailed information
    about the shipment.
    """
    return HTTPTransport.get('/api/v1/track', dict(tracking=tracking_number))

def validate_address(address_object):
    """
    Validate that an address is correct.
    """
    pass
    
def get_transit_time(from_zip, to_zip, weight, carrier=None):
    """
    Find the time needed for a package to get from point A to point B
    with a given service level.
    """
    return HTTPTransport.post('/api/v1/times', {
        'from_zip': from_zip,
        'to_zip': to_zip,
        'weight': weight,
        'carrier': carrier,
    })

def get_rate(carrier, to, from_=None, service='ground'):
    """
    Find the cost to ship a package from point A to point B.
    """
    pass

def get_token():
    return HTTPTransport.get('/api/v1/token')
    