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

dummy_org_id = 'orTwovfDpEYc'
dummy_org_name = 'Test org'

# Test constants
test_expense_purpose = '10205 - Flight to West Lisaville, Apr 12 - Apr 13 - Nilesh Pant - Nilesh Pant - Vueling'
test_category_id_flight = '228953'
test_category_id_default = '228952'
test_expense_id = 'test_expense_id'
test_file_id = 'test_file_id'
test_integration_tpa_name = 'Fyle TravelPerk Integration'
test_integration_tpa_id = 'dummy'
test_integration_type = 'TRAVEL'
test_refresh_token = 'test_refresh_token'
test_code = 'test_code'
invalid_code = 'invalid_code'
test_employee_email = 'test@example.com'
nonexistent_employee_email = 'nonexistent@example.com'
test_amount = '100.00'
test_card_id = 'card_123'
test_url = 'https://example.com/file.pdf'
test_presigned_url = 'https://s3.amazonaws.com/bucket/file.pdf?signature=abc123'
test_file_content = b'test file content'
test_signature = 'test_signature'
test_org_id_invalid = 99999

# Webhook test data
webhook_data_valid = {
    'id': 'test_invoice_id',
    'profile_name': 'Test Profile',
    'lines': [
        {
            'id': 'test_line_id',
            'description': 'Test expense',
            'total_amount': '100.00'
        }
    ]
}

webhook_data_invalid = {
    'id': 'test_invoice_id',
    'profile_name': 'Test Profile'
}

# Connect travelperk test data
connect_travelperk_data = {
    'code': 'invalid_code'
}

# Integration test data
integration_test_data = {
    'type': 'TRAVEL',
    'is_active': True,
    'tpa_id': 'dummy',
    'tpa_name': 'Fyle TravelPerk Integration'
}

# Employee data for tests
employee_query_params = {
    'user->email': 'eq.test@example.com',
    'order': "updated_at.asc",
    'offset': 0,
    'limit': 1
}

employee_query_params_nonexistent = {
    'user->email': 'eq.nonexistent@example.com',
    'order': "updated_at.asc",
    'offset': 0,
    'limit': 1
}

# Corporate card transaction query params
transaction_query_params = {
    'order': 'updated_at.asc',
    'corporate_card_id': 'eq.card_123',
    'amount': 'eq.100.00',
    'offset': 0,
    'limit': 1
}

# File upload headers
file_upload_headers = {
    'Content-Type': 'application/pdf'
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

# TravelPerk Connector test data
webhook_create_data = {
    'name': 'Test Webhook',
    'url': 'https://test.example.com/webhook',
    'secret': 'test_secret',
    'events': ['invoice.created', 'invoice.updated']
}

webhook_response_data = {
    'id': 'webhook_123',
    'name': 'Test Webhook',
    'url': 'https://test.example.com/webhook',
    'enabled': True,
    'events': ['invoice.created', 'invoice.updated']
}

webhook_delete_response = {
    'message': 'Webhook deleted successfully'
}

invoice_profile_data = [
    {
        'id': 'profile_123',
        'name': 'Test Profile 1',
        'currency': 'USD',
        'billing_information': {
            'country_name': 'United States',
            'address': '123 Test St',
            'city': 'Test City'
        }
    },
    {
        'id': 'profile_456',
        'name': 'Test Profile 2',
        'currency': 'EUR',
        'billing_information': {
            'country_name': 'Germany',
            'address': '456 Test Ave',
            'city': 'Berlin'
        }
    }
]

invoice_profile_no_country = {
    'id': 'profile_789',
    'name': 'Test Profile No Country',
    'currency': 'GBP',
    'billing_information': {
        'address': '789 Test Rd',
        'city': 'London'
    }
}

invoice_profile_no_currency = {
    'id': 'profile_999',
    'name': 'Test Profile No Currency',
    'billing_information': {
        'country_name': 'Canada',
        'address': '999 Test Blvd',
        'city': 'Toronto'
    }
}

# TravelPerk connector constants
test_webhook_subscription_id = 'webhook_123'
test_profile_id_1 = 'profile_123'
test_profile_id_2 = 'profile_456'
test_profile_name_1 = 'Test Profile 1'
test_profile_name_2 = 'Test Profile 2'
test_currency_usd = 'USD'
test_currency_eur = 'EUR'
test_country_us = 'United States'
test_country_germany = 'Germany'
test_refresh_token_updated = 'updated_refresh_token'
