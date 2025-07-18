import pytest
from .fixtures import (
    cluster_domain_response,
    bad_request_response,
    empty_employee_response,
    empty_department_response,
    mock_employee_sync_response,
    mock_category_sync_response
)


def mock_test_get_cluster_domain_case_1(mocker):
    """
    Mock setup for test_get_cluster_domain_case_1
    """
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.text = cluster_domain_response
    
    mock_post = mocker.patch('apps.users.helpers.requests.post', return_value=mock_response)
    return mock_post


def mock_test_post_request_case_1(mocker):
    """
    Mock setup for test_post_request_case_1
    """
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.text = cluster_domain_response
    
    mock_post = mocker.patch('apps.users.helpers.requests.post', return_value=mock_response)
    return mock_post


def mock_test_post_request_case_2(mocker):
    """
    Mock setup for test_post_request_case_2
    """
    mock_response = mocker.MagicMock()
    mock_response.status_code = 400
    mock_response.text = bad_request_response
    
    mock_post = mocker.patch('apps.users.helpers.requests.post', return_value=mock_response)
    return mock_post


def mock_test_platform_connector_methods_coverage(mocker):
    """
    Mock setup for test_platform_connector_methods_coverage
    """
    
    # Create a mock connection object with data from fixtures
    mock_connection = mocker.MagicMock()
    mock_connection.v1.admin.employees.list.return_value = empty_employee_response
    mock_connection.v1.admin.employees.invite_bulk.return_value = None
    mock_connection.v1.admin.departments.list_all.return_value = empty_department_response
    mock_connection.v1.admin.departments.post.return_value = None
    mock_connection.v1.admin.employees.list_all.return_value = mock_employee_sync_response
    mock_connection.v1.admin.categories.list_all.return_value = mock_category_sync_response
    
    return {
        'connection': mock_connection
    } 
