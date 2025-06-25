"""
Mock setup functions for TravelPerk tests
"""


def mock_platform_connector(mocker):
    """
    Mock platform connector for TravelPerk tests
    """
    mock_connector = mocker.MagicMock()
    mock_connector.connection.v1.spender.my_profile.get.return_value = {
        'data': {
            'user': {
                'email': 'janedoe@gmail.com',
                'id': '1234'
            }
        }
    }
    
    mocker.patch('apps.users.helpers.PlatformConnector', return_value=mock_connector)
    return mock_connector


def mock_travelperk_connector_disconnect(mocker):
    """
    Mock TravelPerk connector disconnect
    """
    mock_connector = mocker.MagicMock()
    mock_connector.delete_webhook_connection.return_value = {'message': 'success'}
    mocker.patch('apps.travelperk.views.TravelperkConnector', return_value=mock_connector)
    return mock_connector


def mock_travelperk_connector_connect(mocker):
    """
    Mock TravelPerk connector connect
    """
    mock_connector = mocker.MagicMock()
    mock_connector.create_webhook.return_value = {'id': 123}
    mocker.patch('apps.travelperk.views.TravelperkConnector', return_value=mock_connector)
    return mock_connector


def mock_get_refresh_token(mocker):
    """
    Mock get refresh token
    """
    mock_token = mocker.MagicMock()
    mock_token.return_value = 'dummy_refresh_token'
    mocker.patch('apps.travelperk.views.get_refresh_token_using_auth_code', mock_token)
    return mock_token


def mock_test_get_profile_mappings_case_1(mocker):
    """
    Mock setup for test_get_profile_mappings_case_1
    Provides test data for profile mappings
    """
    return {
        'profile_mapping_payload': [
            {
                "profile_name": 'Dummy Profile',
                "is_import_enabled": False,
                "user_role": "CARD_HOLDER"
            }
        ],
        'profile_mapping_response': {
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
    }


def mock_test_get_advanced_settings_case_1(mocker):
    """
    Mock setup for test_get_advanced_settings_case_1
    Provides test data for advanced settings and mocks platform connector
    """
    # Mock the platform connector
    mock_connector = mocker.MagicMock()
    mock_connector.connection.v1.spender.my_profile.get.return_value = {
        'data': {
            'user': {
                'email': 'janedoe@gmail.com',
                'id': '1234'
            }
        }
    }
    mocker.patch('apps.users.helpers.PlatformConnector', return_value=mock_connector)
    
    return {
        'advance_setting_payload': {
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
        },
        'integrations_response': {
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
        },
        'platform_connector': mock_connector
    }


def mock_travelperk_shared_mock(mocker):
    """
    Shared mock setup for TravelPerk tests
    Returns a dictionary of mocks that can be used with mock_dependencies
    """
    mock_platform = mocker.MagicMock()
    mock_platform.connection.v1.spender.my_profile.get.return_value = {
        'data': {
            'user': {
                'email': 'janedoe@gmail.com',
                'id': '1234'
            }
        }
    }
    
    mock_travelperk_connector = mocker.MagicMock()
    mock_travelperk_connector.create_webhook.return_value = {'id': 123}
    mock_travelperk_connector.delete_webhook_connection.return_value = {'message': 'success'}
    
    mocker.patch('apps.travelperk.views.PlatformConnector', return_value=mock_platform)
    mocker.patch('apps.travelperk.views.TravelperkConnector', return_value=mock_travelperk_connector)
    mocker.patch(
        'apps.travelperk.views.get_refresh_token_using_auth_code',
        return_value={'123e3rwer'}
    )
    
    return {
        'platform_connector': mock_platform,
        'travelperk_connector': mock_travelperk_connector,
        'create_webhook': mock_travelperk_connector.create_webhook,
        'delete_webhook_connection': mock_travelperk_connector.delete_webhook_connection,
        'get_my_profile': mock_platform.connection.v1.spender.my_profile.get,
    } 


def mock_construct_expense_payload_case_1(mocker):
    mock_get_category_id = mocker.patch('apps.travelperk.actions.get_category_id', return_value='1234')
    return {'get_category_id': mock_get_category_id}


def mock_create_invoice_lineitems_case_1(mocker):
    from unittest.mock import MagicMock
    mock_connector = MagicMock()
    mock_connector.v1.admin.employees.list.return_value = {'data': [{'user': {'email': 'johndoe@gmail.com'}}]}
    mock_connector.v1.admin.expenses.post.return_value = {'data': {'id': '123'}}

    mock_construct_file_ids = mocker.patch(
        'apps.travelperk.actions.construct_file_ids',
        return_value=['123']
    )
    mock_platform = mocker.patch(
        'apps.orgs.utils.Platform',
        return_value=mock_connector
    )
    return {
        'construct_file_ids': mock_construct_file_ids,
        'platform': mock_platform,
        'mock_connector': mock_connector
    } 
