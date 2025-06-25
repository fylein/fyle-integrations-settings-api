"""
Mock setup functions for TravelPerk tests
"""


def mock_platform_connector(mocker):
    """
    Mock PlatformConnector for TravelPerk tests
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
    mocker.patch('apps.travelperk.views.PlatformConnector', return_value=mock_connector)
    return mock_connector


def mock_travelperk_connector_disconnect(mocker):
    """
    Mock TravelperkConnector for disconnect operations
    """
    mock_connector = mocker.MagicMock()
    mock_connector.delete_webhook_connection.return_value = {'message': 'success'}
    mocker.patch('apps.travelperk.views.TravelperkConnector', return_value=mock_connector)
    return mock_connector


def mock_travelperk_connector_connect(mocker):
    """
    Mock TravelperkConnector for connect operations
    """
    mock_connector = mocker.MagicMock()
    mock_connector.create_webhook.return_value = {'id': 123}
    mocker.patch('apps.travelperk.views.TravelperkConnector', return_value=mock_connector)
    return mock_connector


def mock_get_refresh_token(mocker):
    """
    Mock get_refresh_token_using_auth_code function
    """
    mocker.patch(
        'apps.travelperk.views.get_refresh_token_using_auth_code',
        return_value={'123e3rwer'}
    )


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
