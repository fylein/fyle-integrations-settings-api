mock_post_new_integration_response = {
    "id": 15,
    "org_id": "or3P3xJ0603e",
    "tpa_id": "tpa129sjcjkjx",
    "tpa_name": "Fyle QuickBooks Online Integration",
    "type": "ACCOUNTING",
    "is_active": True,
    "is_beta": False,
    "connected_at": "2023-08-29T11:21:13.840713Z",
    "disconnected_at": None,
    "updated_at": "2023-08-29T11:21:13.840746Z"
}

post_integration_accounting = {
    'tpa_id': 'tpa129sjcjkjx',
    'tpa_name': 'Fyle QuickBooks Online Integration',
    'type': 'ACCOUNTING',
    'is_active': True,
    'connected_at': '2023-08-29T11:21:13.840713Z'
}

post_integration_accounting_2 = {
    'tpa_id': 'tpasample_id1',
    'tpa_name': 'Fyle Some Other Integration',
    'type': 'ACCOUNTING',
    'is_active': True,
    'connected_at': '2025-01-22T11:21:13.840713Z'
}


patch_integration = {
    'tpa_name': 'Fyle QuickBooks Online Integration',
    'errors_count': 12,
    'is_token_expired': False
}

patch_integration_partial = {
    'tpa_name': 'Fyle QuickBooks Online Integration',
    'is_token_expired': True
}

patch_integration_invalid_tpa_name = {
    'tpa_name': 'Very Invalid TPA Name',
    'errors_count': 12,
    'is_token_expired': False
}

patch_integration_no_tpa_name = {
    'errors_count': 12,
    'is_token_expired': False
}

post_integration_hrms = {
    'tpa_id': 'tpa129sjcjkjx',
    'tpa_name': 'Fyle HRMS',
    'type': 'HRMS',
    'is_active': True,
    'connected_at': '2023-08-29T11:21:13.840713Z'
}

delete_integration = {
    'tpa_name': 'Fyle QuickBooks Online Integration'
}

delete_integration_no_tpa_name = {
    'some_field': 'some_value'
}
