import pytest
from datetime import datetime
from bamboosdk.api.employee import Employee
from bamboosdk.exceptions import (
    BambooHrSDKError,
    NoPrivilegeError,
    NotFoundItemError,
    InvalidTokenError
)
from .fixtures import (
    api_token,
    sub_domain,
    employee_id,
    employee_report_payload,
    employee_report_incremental_payload,
    employee_list_response,
    single_employee_response,
    sync_employee_from_date,
    status_200,
    status_401,
    status_403,
    status_404,
    status_500
)



def test_employee_initialization():
    """
    Test Employee class initialization
    """
    employee_api = Employee()
    
    assert employee_api.GET_EMPLOYEE_REPORT == '/v1/reports/custom?format=JSON&onlyCurrent=false'
    assert employee_api.GET_EMPLOYEE == '/v1/employees/{}/?fields=workEmail&onlyCurrent=false'
    assert employee_api.payload == {
        'fields': ['displayName', 'firstName', 'lastName', 'department', 'workEmail', 'supervisorEmail', 'status']
    }
    assert employee_api._ApiBase__api_token is None
    assert employee_api._ApiBase__sub_domain is None
    assert employee_api.headers is None


def test_employee_get_all_without_incremental_sync(mock_dependencies):
    """
    Test Employee get_all method without incremental sync
    """
    employee_api = Employee()
    employee_api.set_api_token(api_token)
    employee_api.set_sub_domain(sub_domain)
    
    result = employee_api.get_all(is_incremental_sync=False)
    
    assert result == employee_list_response


def test_employee_get_all_with_incremental_sync(mock_dependencies):
    """
    Test Employee get_all method with incremental sync
    """
    employee_api = Employee()
    employee_api.set_api_token(api_token)
    employee_api.set_sub_domain(sub_domain)
    
    sync_date = datetime.fromisoformat(sync_employee_from_date.replace('Z', '+00:00'))
    result = employee_api.get_all(is_incremental_sync=True, sync_employee_from=sync_date)
    
    # Verify that filters were added to payload
    assert 'filters' in employee_api.payload
    assert 'lastChanged' in employee_api.payload['filters']
    assert employee_api.payload['filters']['lastChanged']['includeNull'] == 'yes'
    assert employee_api.payload['filters']['lastChanged']['value'] == sync_date
    
    assert result == employee_list_response


def test_employee_get_all_with_incremental_sync_none_date(mock_dependencies):
    """
    Test Employee get_all method with incremental sync but None date
    """
    employee_api = Employee()
    employee_api.set_api_token(api_token)
    employee_api.set_sub_domain(sub_domain)
    
    result = employee_api.get_all(is_incremental_sync=True, sync_employee_from=None)
    
    # Verify that filters were added to payload even with None date
    assert 'filters' in employee_api.payload
    assert employee_api.payload['filters']['lastChanged']['value'] is None
    
    assert result == employee_list_response


def test_employee_get_all_401_error(mock_dependencies):
    """
    Test Employee get_all method with 401 error
    """
    employee_api = Employee()
    employee_api.set_api_token(api_token)
    employee_api.set_sub_domain(sub_domain)
    
    with pytest.raises(InvalidTokenError):
        employee_api.get_all(is_incremental_sync=False)


def test_employee_get_all_403_error(mock_dependencies):
    """
    Test Employee get_all method with 403 error
    """
    employee_api = Employee()
    employee_api.set_api_token(api_token)
    employee_api.set_sub_domain(sub_domain)
    
    with pytest.raises(NoPrivilegeError):
        employee_api.get_all(is_incremental_sync=False)


def test_employee_get_all_404_error(mock_dependencies):
    """
    Test Employee get_all method with 404 error
    """
    employee_api = Employee()
    employee_api.set_api_token(api_token)
    employee_api.set_sub_domain(sub_domain)
    
    with pytest.raises(NotFoundItemError):
        employee_api.get_all(is_incremental_sync=False)


def test_employee_get_all_500_error(mock_dependencies):
    """
    Test Employee get_all method with 500 error
    """
    employee_api = Employee()
    employee_api.set_api_token(api_token)
    employee_api.set_sub_domain(sub_domain)
    
    with pytest.raises(BambooHrSDKError):
        employee_api.get_all(is_incremental_sync=False)


def test_employee_get_success(mock_dependencies):
    """
    Test Employee get method with success response
    """
    employee_api = Employee()
    employee_api.set_api_token(api_token)
    employee_api.set_sub_domain(sub_domain)
    
    result = employee_api.get(employee_id)
    
    assert result == single_employee_response


def test_employee_get_401_error(mock_dependencies):
    """
    Test Employee get method with 401 error
    """
    employee_api = Employee()
    employee_api.set_api_token(api_token)
    employee_api.set_sub_domain(sub_domain)
    
    with pytest.raises(InvalidTokenError):
        employee_api.get(employee_id)


def test_employee_get_403_error(mock_dependencies):
    """
    Test Employee get method with 403 error
    """
    employee_api = Employee()
    employee_api.set_api_token(api_token)
    employee_api.set_sub_domain(sub_domain)
    
    with pytest.raises(NoPrivilegeError):
        employee_api.get(employee_id)


def test_employee_get_404_error(mock_dependencies):
    """
    Test Employee get method with 404 error
    """
    employee_api = Employee()
    employee_api.set_api_token(api_token)
    employee_api.set_sub_domain(sub_domain)
    
    with pytest.raises(NotFoundItemError):
        employee_api.get(employee_id)


def test_employee_get_500_error(mock_dependencies):
    """
    Test Employee get method with 500 error
    """
    employee_api = Employee()
    employee_api.set_api_token(api_token)
    employee_api.set_sub_domain(sub_domain)
    
    with pytest.raises(BambooHrSDKError):
        employee_api.get(employee_id)


def test_employee_payload_modification(mock_dependencies):
    """
    Test Employee payload modification during incremental sync
    """
    employee_api = Employee()
    employee_api.set_api_token(api_token)
    employee_api.set_sub_domain(sub_domain)
    
    original_payload = employee_api.payload.copy()
    
    # Test without incremental sync
    employee_api.get_all(is_incremental_sync=False)
    assert employee_api.payload == original_payload
    
    # Test with incremental sync
    sync_date = datetime.fromisoformat(sync_employee_from_date.replace('Z', '+00:00'))
    
    # Reset payload
    employee_api.payload = {
        'fields': ['displayName', 'firstName', 'lastName', 'department', 'workEmail', 'supervisorEmail', 'status']
    }
    
    employee_api.get_all(is_incremental_sync=True, sync_employee_from=sync_date)
    
    assert 'filters' in employee_api.payload
    assert employee_api.payload['filters']['lastChanged']['value'] == sync_date


def test_employee_url_formatting():
    """
    Test Employee URL formatting
    """
    employee_api = Employee()
    
    expected_url = f'/v1/employees/{employee_id}/?fields=workEmail&onlyCurrent=false'
    actual_url = employee_api.GET_EMPLOYEE.format(employee_id)
    
    assert actual_url == expected_url


def test_employee_inheritance():
    """
    Test Employee inheritance from ApiBase
    """
    employee_api = Employee()
    
    # Test that Employee inherits from ApiBase
    assert hasattr(employee_api, 'set_api_token')
    assert hasattr(employee_api, 'set_sub_domain')
    assert hasattr(employee_api, '_get_request')
    assert hasattr(employee_api, '_post_request')
    assert hasattr(employee_api, 'API_BASE_URL')
    
    # Test Employee-specific attributes
    assert hasattr(employee_api, 'GET_EMPLOYEE_REPORT')
    assert hasattr(employee_api, 'GET_EMPLOYEE')
    assert hasattr(employee_api, 'payload')
    assert hasattr(employee_api, 'get_all')
    assert hasattr(employee_api, 'get')


def test_employee_with_none_values(mock_dependencies):
    """
    Test Employee methods with None values
    """
    employee_api = Employee()
    employee_api.set_api_token(api_token)
    employee_api.set_sub_domain(sub_domain)
    
    # Test get method with None ID - should format URL with None
    result = employee_api.get(None)
    assert result == single_employee_response


def test_employee_with_empty_string_id(mock_dependencies):
    """
    Test Employee get method with empty string ID
    """
    employee_api = Employee()
    employee_api.set_api_token(api_token)
    employee_api.set_sub_domain(sub_domain)
    
    result = employee_api.get('')
    
    assert result == single_employee_response


def test_employee_payload_fields():
    """
    Test Employee payload contains correct fields
    """
    employee_api = Employee()
    
    expected_fields = ['displayName', 'firstName', 'lastName', 'department', 'workEmail', 'supervisorEmail', 'status']
    
    assert employee_api.payload['fields'] == expected_fields
    assert len(employee_api.payload['fields']) == 7
