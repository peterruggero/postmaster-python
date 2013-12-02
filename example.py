import postmaster


postmaster.config.api_key = '0b9a54438fba2dc0d39be8f7c6c71a58'


def create_shipment_simplest():
    shipment = postmaster.Shipment.create(
        to={
            'contact': 'Joe Smith',
            'line1': '701 Brazos St.',
            'city': 'Austin',
            'state': 'TX',
            'zip_code': '78701',
            'phone_no': '555-123-4452'
        },
        packages=[{
            'weight': 1.5,
            'length': 10,
            'width': 6,
            'height': 8,
        }],
        service='2DAY',
    )
    return shipment


def create_shipment_complex():
    shipment = postmaster.Shipment.create(
        from_={
            'company': 'ASLS',
            'contact': 'Joe Dirt',
            'line1': '22 Knightbridge Road',
            'line2': 'Stairway no 2',
            'line3': 'Level -3',
            'city': 'Arnprior',
            'state': 'ON',
            'zip_code': '23407',
            'phone_no': '919-720-7941',
            'phone_ext': '12',
            'country': 'US',
            'tax_id': '934-70-5435',
            'residential': False,
        },
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
            'country': 'US',
            'tax_id': '965-71-4343',
            'residential': False,
        },
        packages=[
            {
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
                        }, {
                            'description': 'description',
                            'value': '15',
                            'weight': 2.5,
                            'weight_units': 'LB',
                            'quantity': 1,
                            'hs_tariff_number': '060110',
                            'country_of_origin': 'AI',
                        },
                    ],
                    'invoice_number': '050912173216-1234',
                    'comments': 'Comments on the commercial invoice',
                },
            }
        ],
        carrier='usps',
        service='2DAY',
    )
    return shipment


def ship():
    shipment = postmaster.Shipment.create(
        to={
            'company': 'Acme Inc.',
            'contact': 'Joe Smith',
            'line1': '701 Brazos St.',
            'city': 'Austin',
            'state': 'TX',
            'zip_code': '78701',
            'phone_no': '555-123-4452'
        },
        packages=[{
            'weight': 1.5,
            'length': 10,
            'width': 6,
            'height': 8,
        }],
        carrier='ups',
        service='2DAY',
    )
    return shipment


def ship_international():
    shipment = postmaster.Shipment.create(
        to={
            'company': 'Groupe SEB',
            'contact': 'Joe Smith',
            'line1': 'Les 4 M - Chemin du Petit Bois',
            'line2': 'BP 172',
            'city': 'ECULLY CEDEX',
            'state': 'TX',
            'zip_code': '69134',
            'phone_no': '9197207941',
            'country': 'FR',
        },
        packages=[{
            'weight': 2.2,
            'length': 10,
            'width': 6,
            'height': 8,
            'customs': {
                'type': 'Other',
                'description': 'Some great stuff.',
                'contents': [{
                    'description': 'A Bolt',
                    'value': 0.34,
                    'weight': 1,
                    'quantity': 1,
                    'country_of_origin': 'FR',
                }],
            },
        }],
        carrier='fedex',
        service='INTL_PRIORITY',
    )
    return shipment

def address():
    address = postmaster.Address(
        company='ACME',
        contact='Joe Smith',
        line1='100 Congress Ave.',
        city='Austin',
        state='TX',
        zip_code='78701',
    )
    response = address.validate()
    return response


def time():
    response = postmaster.get_transit_time(
        from_zip='28771',
        to_zip='78704',
        weight='1.0',
        carrier='ups'
    )
    return response


def rate():
    response = postmaster.get_rate(
        from_zip='28771',
        to_zip='78704',
        weight='1.0',
        carrier='ups',
    )
    return response


def box():
    box = postmaster.Package.create(
        width=10,
        height=12,
        length=8,
        name='My Fun Box'
    )
    return box


def fit():
    response = postmaster.Package.fit(
        items=[{
            'width': 2.2,
            'length': 3,
            'height': 1,
            'count': 2,
            'sku': '123ABC',
        }],
        packages=[{
            'width': 6,
            'length': 6,
            'height': 6,
        }, {
            'width': 12,
            'length': 12,
            'height': 12,
        }]
    )
    return response


def list_shipments():
    shipments, cursor, prev_cursor = postmaster.Shipment.list(limit=1)
    return shipments, cursor, prev_cursor


def delete():
    response = postmaster.Shipment().delete(1234)
    return response


def monitor():
    response = postmaster.Tracking(
        tracking_no='1Z1896X70305267337',
        url='http://example.com/your-listener',
        events=['Delivered', 'Exception']
    ).monitor_external()
    return response


if __name__ == '__main__':
    from pprint import pprint

    #Ship = create_shipment_simplest()
    #print Ship
    #pprint(Ship._data)

    #Ship = create_shipment_complex()
    #print Ship
    #pprint(Ship._data)

    #Ship = ship()
    #print Ship
    #pprint(Ship._data)

    #Ship = ship_international()
    #print Ship
    #pprint(Ship._data)

    #pprint(address())

    #pprint(time())

    #pprint(rate())

    #pprint(box())

    #Fit = fit()
    #print Fit
    #pprint(Fit._data)

    #pprint(list_shipments())

    #print delete()

    #print monitor()
