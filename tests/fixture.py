fixture = {
    'my_profile': {
        'data': {
            'org': {
                'currency': 'EUR',
                'domain': 'afyle.in',
                'id': 'orHVw3ikkCxJ',
                'name': 'Anagha Org'
            },
            'org_id': 'orHVw3ikkCxJ',
            'roles': [
                'FYLER',
                'ADMIN'
            ],
            'user': {
                'email': 'ashwin.t@fyle.in',
                'full_name': 'Joanna',
                'id': 'usqywo0f3nBY'
            },
            'user_id': 'usqywo0f3nBY'
        }
    },
    'expense': {
        'serial_number':'INV-04-00439',
        'profile_id':'a72eccb0-85da-4ca3-ac8b-59242889eff8',
        'profile_name': 'Dummy Profile',
        'billing_information':{
            'legal_name':'Fyle',
            'vat_number':None,
            'address_line_1':'B-48 GM Complex',
            'address_line_2':'',
            'city':'Barcelona',
            'postal_code':'480551',
            'country_name':'Spain'
        },
        'mode':'us-reseller',
        'status':'paid',
        'issuing_date':'2024-03-10',
        'billing_period':'instant',
        'from_date':'2024-03-10',
        'to_date':'2024-03-10',
        'due_date':'2024-03-10',
        'currency':'USD',
        'total':'124.25',
        'taxes_summary':[
            {
                'tax_regime':'US-G-VAT-R-0',
                'subtotal':'124.25',
                'tax_percentage':'0.00',
                'tax_amount':'0.00',
                'total':'124.25'
            }
        ],
        'reference':'Trip #10205',
        'travelperk_bank_account':None,
        'pdf':'xyz.s3.amazonaws.com/invoices/2067/INV-04-00439.pdf?AWSAccessKeyId=XXXX&Signature=uELtA4ryfUv%2Funzoc%2FHZ2UnoCM4%3D&Expires=1710107789',
        'lines':[
            {
                'id':'4cd6abae-762b-4706-8503-28b937f50ada',
                'expense_date':'2024-03-10',
                'description':'PRO for Trip 10205',
                'quantity':1,
                'unit_price':'3.62',
                'non_taxable_unit_price':'0',
                'tax_percentage':'0.00',
                'tax_amount':'0.00',
                'tax_regime':'US-G-VAT-R-0',
                'total_amount':'3.62',
                'metadata':{
                    'trip_id':10205,
                    'trip_name':'Flight to West Lisaville, Apr 12 - Apr 13',
                    'service':'pro_v2',
                    'travelers':[
                    {
                        'name':'Nilesh Pant',
                        'email':'nilesh.p@fyle.in',
                        'external_id':None
                    }
                    ],
                    'booker':{
                    'name':'Nilesh Pant',
                    'email':'nilesh.p@fyle.in',
                    'external_id':None
                    },
                    'start_date':None,
                    'end_date':None,
                    'cost_center':'',
                    'labels':[
                    
                    ],
                    'vendor':None,
                    'out_of_policy':'',
                    'approvers':[
                    
                    ],
                    'service_location':None,
                    'include_breakfast':None,
                    'credit_card_last_4_digits':'4242'
                }
            },
            {
                'id':'c9c61e21-4c5c-469c-a1dd-41ce56189a64',
                'expense_date':'2024-03-10',
                'description':'FLIGHT for Trip ID 10205',
                'quantity':1,
                'unit_price':'120.63',
                'non_taxable_unit_price':'0',
                'tax_percentage':'0.00',
                'tax_amount':'0.00',
                'tax_regime':'US-G-VAT-R-0',
                'total_amount':'120.63',
                'metadata':{
                    'trip_id':10205,
                    'trip_name':'Flight to West Lisaville, Apr 12 - Apr 13',
                    'service':'flight',
                    'travelers':[
                    {
                        'name':'Nilesh Pant',
                        'email':'nilesh.p@fyle.in',
                        'external_id':None
                    }
                    ],
                    'booker':{
                    'name':'Nilesh Pant',
                    'email':'nilesh.p@fyle.in',
                    'external_id':None
                    },
                    'start_date':'2024-04-13',
                    'end_date':'2030-04-17',
                    'cost_center':'',
                    'labels':[
                    
                    ],
                    'vendor':{
                    'code':'VY',
                    'name':'Vueling'
                    },
                    'out_of_policy':True,
                    'approvers':[
                    
                    ],
                    'service_location':{
                    'origin':{
                        'name':'Salasstad Airport',
                        'code':'MAD',
                        'city':'West Lisaville',
                        'country':'Trinidad and Tobago',
                        'country_code':'VE',
                        'latitude':'15.4886261',
                        'longitude':'131.0075138'
                    },
                    'destination':{
                        'name':'North Tara Airport',
                        'code':'BCN',
                        'city':'Oliviaport',
                        'country':'Bulgaria',
                        'country_code':'BY',
                        'latitude':'76.5021054',
                        'longitude':'42.3743066'
                    }
                    },
                    'include_breakfast':None,
                    'credit_card_last_4_digits':'4242'
                }
            }
        ]
    }
}

# Static data for model fixtures
org_data = {
    'name': 'Test Org',
    'fyle_org_id': 'orTwovfDpEYc',
    'cluster_domain': 'https://test.fyle.tech'
}

fyle_credential_data = {
    'refresh_token': 'dummy_refresh_token'
}

bamboohr_data = {
    'folder_id': 'dummy',
    'package_id': 'dummy',
    'api_token': 'dummy_api_token',
    'sub_domain': 'dummy_subdomain'
}

bamboohr_configuration_data = {
    'additional_email_options': [
        {
            'name': 'Admin',
            'email': 'admin@example.com'
        },
        {
            'name': 'Manager',
            'email': 'manager@example.com'
        }
    ],
    'emails_selected': [
        {
            'name': 'Admin',
            'email': 'admin@example.com'
        },
        {
            'name': 'Manager',
            'email': 'manager@example.com'
        }
    ]
}

travelperk_data = {
    'folder_id': 'dummy',
    'package_id': 'dummy',
    'is_travelperk_connected': True
}

travelperk_profile_mapping_data = {
    'profile_name': 'Dummy Profile',
    'user_role': 'TRAVELLER',
    'is_import_enabled': True,
    'country': 'US',
    'currency': 'USD',
    'source_id': 'dummy_source_id'
}

travelperk_advanced_setting_data = {
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

travelperk_credential_data = {
    'refresh_token': 'dummy_refresh_token'
}

integration_accounting_data = {
    'org_id': 'or3P3xJ0603e',
    'org_name': 'Dummy Org',
    'tpa_id': 'tpa129sjcjkjx',
    'tpa_name': 'Fyle QuickBooks Online Integration',
    'type': 'ACCOUNTING',
    'is_active': True,
    'is_beta': True
}

integration_hrms_data = {
    'org_id': 'or3P3xJ0603e',
    'org_name': 'Dummy Org',
    'tpa_id': 'tpa129sjcjkjx',
    'tpa_name': 'Fyle HRMS',
    'type': 'HRMS',
    'is_active': True,
    'is_beta': True
}
