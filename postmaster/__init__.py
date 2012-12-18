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
                json.dumps(self._data), headers=config.headers)
        else:
            response = HTTPTransport.post(
                self.PATH, 
                json.dumps(self._data), headers=config.headers)
        return response
        
    def get(self, id_=None, action=None, params=None):
        """
        Get object(s) from server.
        """
        
        if id_
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

class AddressValidation(PostmasterOjbect):
    pass
            
class Shipment(PostmasterObject):
    
    PATH = '/v1/shipments'
    
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
    pass
    
def validate_address(address_object):
    """
    Validate that an address is correct.
    """
    pass
    
def get_transit_time(to, from_=None, service='ground', carrier=None):
    """
    Find the time needed for a package to get from point A to point B
    with a given service level.
    """
    pass
    
def get_rate(carrier, to, from_=None, service='ground'):
    """
    Find the cost to ship a package from point A to point B.
    """
    pass
    