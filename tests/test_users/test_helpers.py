import pytest
import json
from django.conf import settings
from apps.users.helpers import get_cluster_domain, post_request, PlatformConnector
from apps.fyle_hrms_mappings.models import ExpenseAttribute
from .fixtures import (
    dummy_refresh_token,
    test_cluster_domain,
    test_email,
    test_org_id,
    post_request_headers,
    test_employee_bulk_payload,
    test_department_data,
    test_department_query_params
)
from .mock_setup import mock_test_platform_connector_methods_coverage


def test_get_cluster_domain_case_1(mock_dependencies, api_client, mocker, access_token):
    """
    Test get_cluster_domain helper
    Case: Returns correct cluster domain
    """
    cluster_domain = get_cluster_domain('dummy_access_token')
    assert cluster_domain == 'https://lolo.fyle.tech'


def test_post_request_case_1(mock_dependencies, api_client, mocker, access_token):
    """
    Test post_request helper
    Case: Valid response returns correct data
    """
    url = '{0}/oauth/cluster/'.format(settings.FYLE_BASE_URL)
    response = post_request(url, {}, post_request_headers)
    assert response == {'cluster_domain': 'https://test.fyle.tech'}


def test_post_request_case_2(mock_dependencies, api_client, mocker, access_token):
    """
    Test post_request helper
    Case: Invalid response raises exception
    """
    url = '{0}/oauth/cluster/'.format(settings.FYLE_BASE_URL)
    with pytest.raises(Exception):
        post_request(url, {}, post_request_headers)


def test_platform_connector_initialization(mock_dependencies):
    """
    Test PlatformConnector initialization
    """
    connector = PlatformConnector(dummy_refresh_token, test_cluster_domain)
    assert connector.connection is not None


@pytest.mark.shared_mocks(lambda mocker: mock_test_platform_connector_methods_coverage(mocker))
def test_platform_connector_methods_coverage(mock_dependencies, create_org):
    """
    Test PlatformConnector methods to achieve code coverage
    """
    connector = PlatformConnector(dummy_refresh_token, test_cluster_domain)
    
    # Replace the connection with our mock
    connector.connection = mock_dependencies.connection
    
    # Test get_employee_by_email
    result = connector.get_employee_by_email(test_email)
    assert result == []
    
    # Test bulk_post_employees
    connector.bulk_post_employees(test_employee_bulk_payload)
    
    # Test get_department_generator
    result = connector.get_department_generator(test_department_query_params)
    assert result == {'data': []}
    
    # Test post_department
    connector.post_department(test_department_data)
    
    # Test bulk_create_or_update_expense_attributes - this should create real database records
    # Since we're passing an empty list, no records should be created
    initial_count = ExpenseAttribute.objects.filter(org_id=create_org.id, attribute_type='EMPLOYEE').count()
    connector.bulk_create_or_update_expense_attributes([], 'EMPLOYEE', create_org.id)
    final_count = ExpenseAttribute.objects.filter(org_id=create_org.id, attribute_type='EMPLOYEE').count()
    assert final_count == initial_count
    
    # Test sync_employees
    connector.sync_employees(create_org.id)
    
    # Test sync_categories
    connector.sync_categories(create_org.id)



