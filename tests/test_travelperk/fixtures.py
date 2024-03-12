fixture = {
    'travelperk': {
       'id':1,
       'folder_id':'1231',
       'package_id':'1231',
       'is_fyle_connected':'t',
       'travelperk_connection_id': None,
       'is_travelperk_connected': True,
       'onboarding_state': 'CONNECTION',
       'is_s3_connected':'dtmmy',
       'created_at':'2022-11-29T15:39:49.221955Z',
       'updated_at':'2022-11-29T15:41:59.535831Z',
       'webhook_subscription_id': '123',
       'webhook_enabled': True,
       'org':2
    },
    'profile_mapping': {
        'count': 1,
        'next': None,
        'previous': None,
        'results': [
            {
                'id': 4,
                'profile_name': 'Kamalini Visa Card',
                'user_role': 'CARD_HOLDER',
                'is_import_enabled': False,
                'country': None,
                'currency': 'USD',
                'source_id': 'b2cca47d-c3bc-4b09-8f86-358a83cae842',
                'created_at': '2024-03-12T06:30:59.896680Z',
                'updated_at': '2024-03-12T06:31:27.662549Z',
                'org': 7
            },
        ]
    },
    'advanced_settings': {
        'default_employee_name': 'ashwin.t@fyle.in',
        'default_employee_id': 'usqywo0f3nBY',
        'default_category_name': 'Acc. Dep-Leasehold Improvements',
        'default_category_id': '228952',
        'invoice_lineitem_structure': 'MULTIPLE',
        'description_structure': [
            'trip_id',
            'trip_name',
            'traveler_name',
            'booker_name',
            'merchant_name'
        ],
        'category_mappings': {
            'Cars': {
                'id': '228952',
                'name': 'Acc. Dep-Leasehold Improvements'
            },
            'Hotels': {
                'id': '264337',
                'name': 'Elon Baba'
            },
            'Trains': {
                'id': '228955',
                'name': 'Sales - Merchandise'
            },
            'Flights': {
                'id': '228953',
                'name': 'Customer Deposits'
            }
        },
        'org': 7
    },
    'payload': {
        'data': {
            'source':'CORPORATE_CARD',
            'spent_at':'2024-03-10 00:00:00+00:00',
            'purpose':'10205 - Flight to West Lisaville, Apr 12 - Apr 13 - Nilesh Pant - Nilesh Pant - Vueling',
            'merchant':'Travelperk',
            'category_id':'1234',
            'claim_amount':'120.63'
        }
    }
}
