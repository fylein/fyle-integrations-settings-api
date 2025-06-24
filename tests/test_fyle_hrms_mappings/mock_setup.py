"""
Mock setup for fyle_hrms_mappings tests.
Contains all mocking patterns used across fyle_hrms_mappings test files.
"""

# Note: No test files currently import from this mock_setup.py
# All tests use direct mocking with mocker.patch()
# This file is kept as a placeholder for future use if needed.

import pytest
from unittest.mock import MagicMock


def mock_fyle_platform_api(mocker):
    """
    Mock Fyle platform API calls for HRMS mappings
    """
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'data': {
            'mappings': [
                {'id': 1, 'fyle_field': 'department', 'hrms_field': 'dept'},
                {'id': 2, 'fyle_field': 'location', 'hrms_field': 'loc'}
            ]
        }
    }
    
    mock_requests = mocker.patch('requests.get')
    mock_requests.return_value = mock_response
    
    return mock_requests, mock_response


def mock_hrms_integration(mocker):
    """
    Mock HRMS integration operations
    """
    mock_integration = mocker.patch('apps.fyle_hrms_mappings.models.HRMSIntegration')
    mock_integration_instance = mocker.MagicMock()
    mock_integration.objects.get.return_value = mock_integration_instance
    
    return mock_integration, mock_integration_instance


def mock_all_hrms_mapping_dependencies(mocker):
    """
    Mock all HRMS mapping external dependencies
    """
    mock_api = mock_fyle_platform_api(mocker)
    mock_integration = mock_hrms_integration(mocker)
    
    return {
        'api': mock_api,
        'integration': mock_integration
    }


def mock_get_cluster_domain(mocker):
    """
    Mock get_cluster_domain function
    """
    mock_cluster_domain = mocker.patch('apps.fyle_hrms_mappings.views.get_cluster_domain')
    mock_cluster_domain.return_value = 'https://test.fyle.tech'
    return mock_cluster_domain


def mock_requests_get_success(mocker):
    """
    Mock successful requests.get call
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'data': {
            'mappings': [
                {'id': 1, 'fyle_field': 'employee_id', 'hrms_field': 'employee_number'},
                {'id': 2, 'fyle_field': 'department', 'hrms_field': 'department_name'}
            ]
        }
    }
    
    mock_requests_get = mocker.patch('apps.fyle_hrms_mappings.views.requests.get')
    mock_requests_get.return_value = mock_response
    return mock_requests_get, mock_response


def mock_requests_post_success(mocker):
    """
    Mock successful requests.post call
    """
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        'data': {
            'id': 3,
            'fyle_field': 'location',
            'hrms_field': 'location_name'
        }
    }
    
    mock_requests_post = mocker.patch('apps.fyle_hrms_mappings.views.requests.post')
    mock_requests_post.return_value = mock_response
    return mock_requests_post, mock_response


def mock_destination_attribute_shared_mock(mocker):
    """
    Shared mock for DestinationAttribute operations
    """
    mock_destination_attribute = mocker.patch('apps.fyle_hrms_mappings.models.DestinationAttribute')
    mock_instance = MagicMock()
    mock_destination_attribute.objects.create.return_value = mock_instance
    mock_destination_attribute.objects.get.return_value = mock_instance
    mock_destination_attribute.objects.filter.return_value = MagicMock()
    
    return {
        'mock_destination_attribute': mock_destination_attribute,
        'mock_instance': mock_instance
    }


def mock_expense_attribute_shared_mock(mocker):
    """
    Shared mock for ExpenseAttribute operations
    """
    mock_expense_attribute = mocker.patch('apps.fyle_hrms_mappings.models.ExpenseAttribute')
    mock_instance = MagicMock()
    mock_expense_attribute.objects.create.return_value = mock_instance
    mock_expense_attribute.objects.get.return_value = mock_instance
    mock_expense_attribute.objects.filter.return_value = MagicMock()
    
    return {
        'mock_expense_attribute': mock_expense_attribute,
        'mock_instance': mock_instance
    }


def mock_mapping_shared_mock(mocker):
    """
    Shared mock for Mapping operations
    """
    mock_mapping = mocker.patch('apps.fyle_hrms_mappings.models.Mapping')
    mock_instance = MagicMock()
    mock_mapping.objects.create.return_value = mock_instance
    mock_mapping.objects.get.return_value = mock_instance
    mock_mapping.objects.filter.return_value = MagicMock()
    
    return {
        'mock_mapping': mock_mapping,
        'mock_instance': mock_instance
    }


def mock_org_shared_mock(mocker):
    """
    Shared mock for Org operations
    """
    mock_org = mocker.patch('apps.fyle_hrms_mappings.models.Org')
    mock_instance = MagicMock()
    mock_org.objects.get.return_value = mock_instance
    
    return {
        'mock_org': mock_org,
        'mock_instance': mock_instance
    }


def mock_all_fyle_hrms_mappings_dependencies(mocker):
    """
    Mock all fyle_hrms_mappings external dependencies
    """
    mock_destination = mock_destination_attribute_shared_mock(mocker)
    mock_expense = mock_expense_attribute_shared_mock(mocker)
    mock_mapping = mock_mapping_shared_mock(mocker)
    mock_org = mock_org_shared_mock(mocker)
    
    return {
        'destination': mock_destination,
        'expense': mock_expense,
        'mapping': mock_mapping,
        'org': mock_org
    } 
 