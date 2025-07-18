"""
Mock setup functions for orgs tests
"""

from .fixtures import (
    fyle_admin_response,
    fyle_admin_simple_response,
    platform_employees_response,
    platform_employees_simple_response
)


def mock_get_fyle_admin(mocker):
    """
    Mock get_fyle_admin function
    """
    mocker.patch(
        'apps.orgs.serializers.get_fyle_admin',
        return_value=fyle_admin_response
    )


def mock_platform_employees_list(mocker):
    """
    Mock platform employees list function
    """
    mocker.patch(
        'fyle.platform.apis.v1.admin.employees.list_all',
        return_value=platform_employees_response
    )


def mock_orgs_shared_mock(mocker):
    """
    Shared mock setup for orgs tests
    Returns a dictionary of mocks that can be used with mock_dependencies
    """
    mock_fyle_admin = mocker.patch(
        'apps.orgs.serializers.get_fyle_admin',
        return_value=fyle_admin_simple_response
    )
    
    mock_platform_employees = mocker.patch(
        'fyle.platform.apis.v1.admin.employees.list_all',
        return_value=platform_employees_simple_response
    )
    
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector.connection.v1.admin.employees.list_all.return_value = platform_employees_simple_response
    mocker.patch('apps.orgs.actions.Platform', return_value=mock_platform_connector)
    
    return {
        'get_fyle_admin': mock_fyle_admin,
        'platform_employees_list': mock_platform_employees,
        'platform_connector': mock_platform_connector,
        'employees_list_all': mock_platform_connector.connection.v1.admin.employees.list_all,
    } 


def mock_test_import_categories_success(mocker):
    expected_categories = [
        {
            'attribute_type': 'CATEGORY',
            'display_name': 'Category',
            'value': 'Category 1 / Sub Cat 1',
            'source_id': 'cat1',
            'active': True,
            'detail': None
        },
        {
            'attribute_type': 'CATEGORY',
            'display_name': 'Category',
            'value': 'Category 2 / Sub Cat 2',
            'source_id': 'cat2',
            'active': True,
            'detail': None
        }
    ]
    mock_connector = mocker.MagicMock()
    mock_connector.sync_categories.return_value = expected_categories
    return {
        'platform_connector': mock_connector,
        'expected_categories': expected_categories
    }

def mock_test_create_fyle_connection_success(mocker):
    mock_platform_class = mocker.patch('fyle.platform.Platform')
    mock_platform_instance = mocker.MagicMock()
    mock_platform_class.return_value = mock_platform_instance
    return {
        'platform_class': mock_platform_class,
        'platform_instance': mock_platform_instance
    } 
