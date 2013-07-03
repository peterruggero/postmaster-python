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
    PATH = '/v1/rates'


class TimeInTransit(PostmasterObject):
    PATH = '/v1/times'


class Address(PostmasterObject):

    PATH = '/v1/validate'

    def __init__(self, company=None, contact=None, line1=None, line2=None, line3=None, city=None, state=None, zip_code=None, country=None):
        kwargs = dict(
            company=company,
            contact=contact,
            line1=line1,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country
        )
        if line2:
            kwargs['line2'] = line2
        if line3:
            kwargs['line3'] = line3
        super(Address, self).__init__(**kwargs)

    def validate(self):
        return self.put()


class Shipment(PostmasterObject):

    PATH = '/v1/shipments'

    @classmethod

    def create(cls, to, packages, service, from_=None, carrier=None, reference=None, options=None):
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
         * packages (required) - a dict (or list of dicts) representing the package:
           * weight
           * length
           * width
           * height
         * from (optional) - a dict representing the ship-from address.
                             Will use default for account if not provided.
         * customs (optional)
        """

        shipment = Shipment()
        shipment._data = {
            'to': to,
            'packages': packages,
            'service': service,
        }

        if from_:
            shipment._data['from'] = from_
        if carrier:
            shipment._data['carrier'] = carrier
        if reference:
            shipment._data['reference'] = reference
        if options:
            shipment._data['options'] = options

        resp = shipment.put()

        shipment._data.update(resp)
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


class Package(PostmasterObject):
    PATH = '/v1/packages'
    weight_units = ['LB', 'OZ', 'KG', 'G']
    size_units = ['IN', 'FT', 'CM', 'M']

    @classmethod
    def create(cls, width, height, length, weight=None, weight_units='LB', size_units='IN', name=None):
        """
        Create a new box.

        Arguments:

        * width (required) - The width of the box.
        * height (required) - The height of the box.
        * length (required) - The length of the box.
        * weight The weight of the box.
        * weight_units - The units used to measure weight. LB, OZ, KG, or G
        * size_units - The units used to measure sizes. IN, FT, CM, or M
        * name - A memorable name.
        """

        box = Package()
        box._data = {
            'width': width,
            'height': height,
            'length': length,
        }

        if weight:
            box._data['weight'] = weight
        if weight_units in cls.weight_units:
            box._data['weight_units'] = weight_units
        if size_units in cls.size_units:
            box._data['size_units'] = size_units
        if name:
            box._dat['name'] = name

        resp = box.put()

        box._data.update(resp)
        box.id = resp['id']

        return box

    @classmethod
    def list(cls, limit=10, cursor=None):
        """
        Retrieve a list of all user-defined box types.

        Arguments:

        * limit (optional) - Number of boxes to get. Default 10.
        * cursor (optional) - Cursor offset.
        """

        boxes = Package()
        resp = boxes.get()

        boxes._data.update(resp)

        return boxes

    @classmethod
    def fit(cls, items, packages=None, package_limit=None):
        """
        Given a set of box types, try to fill it optimally.

        Arguments:

        * items (required) - A list of items (dicts) to fit into the box.
          * width (required)
          * height (required)
          * length (required)
          * weight
          * weight_units - Choices: LB, OZ, KG, or G.
          * size_units - Choices: IN, FT, CM, or M.
          * name
          * sku
        * packages (optional) - A list of package types to use. (Default is use API boxes).
          * width (required)
          * height (required)
          * length (required)
          * weight
          * weight_units - Choices: LB, OZ, KG, or G.
          * size_units - Choices: IN, FT, CM, or M.
        * package_limit (optional) - A maximum number of packages to create.
        """

        fit = Package()
        fit.PATH += '/fit'
        fit._data = {'items': items}
        if packages:
            fit._data['packages'] = packages
        if package_limit:
            fit._data['package_limit'] = package_limit

        resp = fit.put()

        fit._data.update(resp)

        return fit


def track_by_reference(tracking_number):
    """
    Track any package by it's carrier-specific tracking number.
    Note: if this package was not shipped my Postmaster
    the resulting data will not contain detailed information
    about the shipment.
    """
    return HTTPTransport.get('/v1/track', dict(tracking=tracking_number))


def validate_address(address_object):
    """
    Validate that an address is correct.
    """
    pass


def get_transit_time(from_zip, to_zip, weight, carrier=None):
    """
    Find the time needed for a package to get from point A to point B
    """
    tit = TimeInTransit(
        from_zip=from_zip,
        to_zip=to_zip,
        weight=weight,
        carrier=carrier,
    )
    return tit.put()


def get_rate(carrier, to_zip, weight, from_zip=None, service='ground'):
    """
    Find the cost to ship a package from point A to point B.
    """
    rate = Rate(
        from_zip=from_zip,
        to_zip=to_zip,
        weight=weight,
        carrier=carrier,
        service=service,
    )

    return rate.put()


def get_token():
    return HTTPTransport.get('/v1/token')
