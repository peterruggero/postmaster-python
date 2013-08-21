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
        packages={
            'weight': 1.5,
            'length': 10,
            'width': 6,
            'height': 8,
        },
        service='2DAY',
    )
    return shipment


def create_shipment_international():
    shipment = postmaster.Shipment.create(
        to={
            'contact': 'Joe Smith',
            'line1': '701 Brazos St.',
            'city': 'Austin',
            'state': 'TX',
            'zip_code': '78701',
            'phone_no': '555-123-4452'
        },
        packages={
            'weight': 1.5,
            'length': 10,
            'width': 6,
            'height': 8,
            'customs': {
                'type': 'Gift',
                'contents': {
                    'description': 'description',
                    'value': '15',
                    'weight': 2.5,
                    'quantity': 1,
                }
            },
        },
        carrier='usps',
        service='2DAY',
    )
    return shipment


def create_shipment_full():
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
            },
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
            },
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
        }],
        packages=[{
            'width': 6,
            'length': 6,
            'height': 6,
            'sku': '123ABC',
        }, {
            'width': 12,
            'length': 12,
            'height': 12,
            'sku': '456XYZ',
        }]
    )
    return response


def list_shipments():
    shipments, cursor, prev_cursor = postmaster.Shipment.list(limit=1)
    return shipments, cursor, prev_cursor


def delete():
    response = postmaster.Shipment().delete(1234)
    return response


if __name__ == '__main__':

    print create_shipment_simplest()
    #print create_shipment_international()
    #print create_shipment_full()
    #ship()
    #address()
    #time()
    #rate()
    #box()
    #fit()
    #list_shipments()
    #delete()
    pass
