import postmaster


postmaster.config.api_key = 'tt_NzAwMTpfOFFzNGxmQ29NaGE4VkJDSTdOdF8zaXk2UT'


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

if __name__ == '__main__':
    print create_shipment_simplest()
    print create_shipment_international()
    print create_shipment_full()