"""
Mock setup for orgs tests.
Contains all mocking patterns used across orgs test files.
"""

import pytest
from unittest.mock import MagicMock


def mock_admin_employees(mocker):
    """
    Mock admin employees for admin view tests
    """
    mock_employees = [
        {'id': 1, 'full_name': 'John Doe', 'email': 'john@example.com'},
        {'id': 2, 'full_name': 'Jane Smith', 'email': 'jane@example.com'}
    ]
    mock_get_admin_employees = mocker.patch('apps.orgs.views.get_admin_employees')
    mock_get_admin_employees.return_value = mock_employees
    
    return mock_get_admin_employees


def mock_all_external_dependencies(mocker):
    """
    Mock all external dependencies for org operations
    """
    # Mock Fyle admin response
    mock_fyle_admin_response = mocker.patch('fyle_rest_auth.helpers.get_fyle_admin')
    mock_fyle_admin_response.return_value = {
        'data': {
            'org': {
                'name': 'Test Org',
                'id': 'test_org_id'
            },
            'roles': ['ADMIN']
        }
    }
    # Mock cluster domain functions
    mock_users_cluster_domain = mocker.patch('apps.users.helpers.get_cluster_domain')
    mock_users_cluster_domain.return_value = 'test.fyle.tech'
    mock_fyle_cluster_domain = mocker.patch('fyle_rest_auth.helpers.get_cluster_domain')
    mock_fyle_cluster_domain.return_value = 'test.fyle.tech'
    # Mock requests.get
    mock_http_response = MagicMock()
    mock_http_response.json.return_value = {
        'data': {
            'org': {
                'name': 'Test Org',
                'id': 'test_org_id'
            },
            'roles': ['ADMIN']
        }
    }
    mock_http_response.status_code = 200
    mock_http_response.text = '{"data":{"org":{"name":"Test Org","id":"test_org_id"},"roles":["ADMIN"]}}'
    mock_requests_get = mocker.patch('requests.get')
    mock_requests_get.return_value = mock_http_response
    return {
        'fyle_admin': mock_fyle_admin_response,
        'cluster_domains': (mock_users_cluster_domain, mock_fyle_cluster_domain),
        'requests': (mock_requests_get, mock_http_response)
    }


def mock_platform_connector_shared_mock(mocker):
    """
    Shared mock for PlatformConnector used in actions tests
    """
    # Deep mock for the full attribute chain
    mock_employees = mocker.MagicMock()
    mock_employees.list_all.return_value = [
        {'data': [{'user': {'email': 'admin@example.com', 'full_name': 'Admin User'}}]}
    ]
    mock_admin = mocker.MagicMock(employees=mock_employees)
    mock_v1 = mocker.MagicMock(admin=mock_admin)
    mock_connection = mocker.MagicMock(v1=mock_v1)
    mock_platform = mocker.MagicMock(connection=mock_connection)
    
    # Patch the PlatformConnector in actions module where it's actually used
    mock_platform_connector = mocker.patch('apps.orgs.actions.PlatformConnector')
    mock_platform_connector.return_value = mock_platform
    
    return {
        'mock_platform_connector': mock_platform_connector,
        'mock_platform': mock_platform,
        'mock_connection': mock_connection,
        'mock_v1': mock_v1,
        'mock_admin': mock_admin,
        'mock_employees': mock_employees
    }


def mock_fyle_platform_shared_mock(mocker):
    """
    Shared mock for Fyle Platform used in utils tests
    """
    mock_fyle_platform = mocker.patch('apps.orgs.utils.Platform')
    mock_platform_instance = mocker.MagicMock()
    mock_fyle_platform.return_value = mock_platform_instance
    
    return {
        'mock_fyle_platform': mock_fyle_platform,
        'mock_platform_instance': mock_platform_instance
    }


def mock_platform_connector_sync_categories_shared_mock(mocker):
    """
    Shared mock for PlatformConnector.sync_categories used in utils tests
    """
    mock_sync_categories = mocker.patch('apps.users.helpers.PlatformConnector.sync_categories')
    mock_sync_categories.return_value = []
    
    return {
        'mock_sync_categories': mock_sync_categories
    }


def mock_get_fyle_admin_shared_mock(mocker):
    """
    Shared mock for get_fyle_admin used in serializers tests
    """
    mock_get_fyle_admin = mocker.patch('apps.orgs.serializers.get_fyle_admin')
    mock_get_fyle_admin.return_value = {
        'data': {
            'org': {
                'name': 'Test Org',
                'id': 'org123'
            },
            'user_id': 'user123'
        }
    }
    
    return {
        'mock_get_fyle_admin': mock_get_fyle_admin
    }


def mock_logger_shared_mock(mocker):
    """
    Shared mock for logger used in exceptions tests
    """
    mock_logger = mocker.patch('apps.orgs.exceptions.logger')
    
    return {
        'mock_logger': mock_logger
    } 
