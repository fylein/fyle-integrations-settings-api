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
            'admin_amount':'120.63',
            'file_ids': ['123'],
            'assignee_user_email': 'johndoe@gmail.com'
        }
    },
    'advance_setting_payload': {
        "default_employee_name": "ashwin.t@fyle.in",
        "default_employee_id": "usqywo0f3nBY",
        "default_category_name": "Historical Adjustment",
        "default_category_id": "292516",
        "invoice_lineitem_structure": "MULTIPLE",
        "description_structure": [
            "trip_id",
            "trip_name",
            "traveler_name",
            "booker_name",
            "merchant_name"
        ],
        "category_mappings": {
            "Cars": {
                "name": "Wages Payable",
                "id": "292527"
            },
            "Hotels": {
                "name": "Taxes",
                "id": "274629"
            },
            "Trains": {
                "name": "Utilities",
                "id": "135646"
            },
            "Flights": {
                "name": "Unpaid Expense Claims",
                "id": "292526"
            }
        },
        "org": 360
    },
    "integrations_response": {
        "org_id": "orTwovfDpEYc",
        "org_name": "Test org",
        "tpa_id": "dummy",
        "tpa_name": "Fyle TravelPerk Integration",
        "type": "TRAVEL",
        "is_active": True,
        "is_beta": True,
        "connected_at": "2025-01-09T10:08:20.434443Z",
        "disconnected_at": None,
        "updated_at": "2025-01-09T10:08:20.434443Z"
    }
}

advance_setting_payload = {
    'default_employee_name': 'ashwin.t@fyle.in',
    'default_employee_id': 'usqywo0f3nBY',
    'default_category_name': 'Acc. Dep-Leasehold Improvements',
    'default_category_id': '228952',
    'invoice_lineitem_structure': 'MULTIPLE',
    'description_structure': [
        'trip_id', 'trip_name', 'traveler_name', 'booker_name', 'merchant_name'
    ],
    'category_mappings': {
        'Cars': {'id': '228952', 'name': 'Acc. Dep-Leasehold Improvements'},
        'Hotels': {'id': '264337', 'name': 'Elon Baba'},
        'Trains': {'id': '228955', 'name': 'Sales - Merchandise'},
        'Flights': {'id': '228953', 'name': 'Customer Deposits'}
    }
}

integrations_response = {
    "org_id": "orTwovfDpEYc",
    "org_name": "Test org",
    "tpa_id": "dummy",
    "tpa_name": "Fyle TravelPerk Integration",
    "type": "TRAVEL",
    "is_active": True,
    "is_beta": True,
    "connected_at": "2025-01-09T10:08:20.434443Z",
    "disconnected_at": None,
    "updated_at": "2025-01-09T10:08:20.434443Z"
}

profile_mapping_payload = [
    {
        "profile_name": 'Dummy Profile',
        "is_import_enabled": False,
        "user_role": "CARD_HOLDER"
    }
]

profile_mapping_response = {
    'results': [{
        "id": 1,
        "profile_name": 'Dummy Profile',
        "is_import_enabled": False,
        "user_role": "CARD_HOLDER",
        "org": 1,
        "created_at": "2022-11-29T15:39:49.221955Z",
        "updated_at": "2022-11-29T15:41:59.535831Z"
    }]
}
