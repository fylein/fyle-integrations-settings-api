import pytest
from bamboosdk.api.api_base import ApiBase
from bamboosdk.exceptions import (
    BambooHrSDKError,
    NoPrivilegeError,
    NotFoundItemError,
    InvalidTokenError
)
from .fixtures import (
    api_token,
    sub_domain,
    expected_headers,
    employee_report_url,
    employee_report_payload,
    status_200,
    status_201,
    status_401,
    status_403,
    status_404,
    status_500,
    error_401_message,
    error_403_message,
    error_404_message,
    error_500_message
)
from .mock_setup import (
    mock_requests_get_success,
    mock_requests_post_success,
    mock_requests_delete_success,
    mock_requests_get_401_error,
    mock_requests_get_403_error,
    mock_requests_get_404_error,
    mock_requests_get_500_error,
    mock_requests_post_401_error,
    mock_requests_post_403_error,
    mock_requests_post_404_error,
    mock_requests_post_500_error,
    mock_requests_delete_401_error,
    mock_requests_delete_403_error,
    mock_requests_delete_404_error,
    mock_requests_delete_500_error
)


def test_api_base_initialization():
    """
    Test ApiBase initialization
    """
    api_base = ApiBase()
    
    assert api_base._ApiBase__api_token is None
    assert api_base._ApiBase__sub_domain is None
    assert api_base.headers is None
    assert api_base.API_BASE_URL == 'https://api.bamboohr.com/api/gateway.php/{}'


def test_api_base_set_api_token():
    """
    Test ApiBase set_api_token method
    """
    api_base = ApiBase()
    api_base.set_api_token(api_token)
    
    assert api_base._ApiBase__api_token == api_token
    assert api_base.headers is not None
    assert api_base.headers['Accept'] == 'application/json'
    assert api_base.headers['content-type'] == 'application/json'
    assert 'Basic' in api_base.headers['authorization']


def test_api_base_set_sub_domain():
    """
    Test ApiBase set_sub_domain method
    """
    api_base = ApiBase()
    api_base.set_sub_domain(sub_domain)
    
    assert api_base._ApiBase__sub_domain == sub_domain


def test_api_base_encode_username_password():
    """
    Test ApiBase __encode_username_password method
    """
    api_base = ApiBase()
    api_base.set_api_token(api_token)
    
    # The method is private, so we test it indirectly through headers
    assert 'Basic' in api_base.headers['authorization']
    
    # Extract the base64 part
    auth_header = api_base.headers['authorization']
    base64_part = auth_header.split(' ')[1]
    
    # Decode and verify format
    import base64
    decoded = base64.b64decode(base64_part).decode()
    assert decoded == f'{api_token}:a'


def test_api_base_get_request_success(mocker):
    """
    Test ApiBase _get_request method with success response
    """
    api_base = ApiBase()
    api_base.set_api_token(api_token)
    api_base.set_sub_domain(sub_domain)
    
    mock_requests_get_success(mocker)
    
    result = api_base._get_request(employee_report_url)
    
    assert result == {'success': True, 'data': 'test_data'}


def test_api_base_get_request_401_error(mocker):
    """
    Test ApiBase _get_request method with 401 error
    """
    api_base = ApiBase()
    api_base.set_api_token(api_token)
    api_base.set_sub_domain(sub_domain)
    
    mock_requests_get_401_error(mocker)
    
    with pytest.raises(InvalidTokenError) as excinfo:
        api_base._get_request(employee_report_url)
    
    assert 'Invalid token, try to refresh it' in str(excinfo.value)


def test_api_base_get_request_403_error(mocker):
    """
    Test ApiBase _get_request method with 403 error
    """
    api_base = ApiBase()
    api_base.set_api_token(api_token)
    api_base.set_sub_domain(sub_domain)
    
    mock_requests_get_403_error(mocker)
    
    with pytest.raises(NoPrivilegeError) as excinfo:
        api_base._get_request(employee_report_url)
    
    assert 'Forbidden, the user has insufficient privilege' in str(excinfo.value)


def test_api_base_get_request_404_error(mocker):
    """
    Test ApiBase _get_request method with 404 error
    """
    api_base = ApiBase()
    api_base.set_api_token(api_token)
    api_base.set_sub_domain(sub_domain)
    
    mock_requests_get_404_error(mocker)
    
    with pytest.raises(NotFoundItemError) as excinfo:
        api_base._get_request(employee_report_url)
    
    assert 'Not found item with ID' in str(excinfo.value)


def test_api_base_get_request_500_error(mocker):
    """
    Test ApiBase _get_request method with 500 error
    """
    api_base = ApiBase()
    api_base.set_api_token(api_token)
    api_base.set_sub_domain(sub_domain)
    
    mock_requests_get_500_error(mocker)
    
    with pytest.raises(BambooHrSDKError) as excinfo:
        api_base._get_request(employee_report_url)
    
    assert 'Status code 500' in str(excinfo.value)


def test_api_base_post_request_success_200(mocker):
    """
    Test ApiBase _post_request method with 200 success response
    """
    api_base = ApiBase()
    api_base.set_api_token(api_token)
    api_base.set_sub_domain(sub_domain)
    
    mock_requests_post_success(mocker)
    
    result = api_base._post_request(employee_report_url, employee_report_payload)
    
    assert result == {'success': True, 'data': 'created'}


def test_api_base_post_request_success_201(mocker):
    """
    Test ApiBase _post_request method with 201 success response
    """
    api_base = ApiBase()
    api_base.set_api_token(api_token)
    api_base.set_sub_domain(sub_domain)
    
    # Mock 201 response
    mock_response = mocker.MagicMock()
    mock_response.status_code = status_201
    mock_response.text = '{"success": true, "data": "created"}'
    mocker.patch('requests.post', return_value=mock_response)
    
    result = api_base._post_request(employee_report_url, employee_report_payload)
    
    assert result == {'success': True, 'data': 'created'}


def test_api_base_post_request_401_error(mocker):
    """
    Test ApiBase _post_request method with 401 error
    """
    api_base = ApiBase()
    api_base.set_api_token(api_token)
    api_base.set_sub_domain(sub_domain)
    
    mock_requests_post_401_error(mocker)
    
    with pytest.raises(InvalidTokenError) as excinfo:
        api_base._post_request(employee_report_url, employee_report_payload)
    
    assert 'Invalid token, try to refresh it' in str(excinfo.value)


def test_api_base_post_request_403_error(mocker):
    """
    Test ApiBase _post_request method with 403 error
    """
    api_base = ApiBase()
    api_base.set_api_token(api_token)
    api_base.set_sub_domain(sub_domain)
    
    mock_requests_post_403_error(mocker)
    
    with pytest.raises(NoPrivilegeError) as excinfo:
        api_base._post_request(employee_report_url, employee_report_payload)
    
    assert 'Forbidden, the user has insufficient privilege' in str(excinfo.value)


def test_api_base_post_request_404_error(mocker):
    """
    Test ApiBase _post_request method with 404 error
    """
    api_base = ApiBase()
    api_base.set_api_token(api_token)
    api_base.set_sub_domain(sub_domain)
    
    mock_requests_post_404_error(mocker)
    
    with pytest.raises(NotFoundItemError) as excinfo:
        api_base._post_request(employee_report_url, employee_report_payload)
    
    assert 'Not found item with ID' in str(excinfo.value)


def test_api_base_post_request_500_error(mocker):
    """
    Test ApiBase _post_request method with 500 error
    """
    api_base = ApiBase()
    api_base.set_api_token(api_token)
    api_base.set_sub_domain(sub_domain)
    
    mock_requests_post_500_error(mocker)
    
    with pytest.raises(BambooHrSDKError) as excinfo:
        api_base._post_request(employee_report_url, employee_report_payload)
    
    assert 'Status code 500' in str(excinfo.value)


def test_api_base_delete_request_success(mocker):
    """
    Test ApiBase _delete_request method with success response
    """
    api_base = ApiBase()
    api_base.set_api_token(api_token)
    api_base.set_sub_domain(sub_domain)
    
    mock_requests_delete_success(mocker)
    
    result = api_base._delete_request('/v1/webhooks/456')
    
    assert result == {'message': 'Webhook has been deleted'}


def test_api_base_delete_request_401_error(mocker):
    """
    Test ApiBase _delete_request method with 401 error
    """
    api_base = ApiBase()
    api_base.set_api_token(api_token)
    api_base.set_sub_domain(sub_domain)
    
    mock_requests_delete_401_error(mocker)
    
    with pytest.raises(InvalidTokenError) as excinfo:
        api_base._delete_request('/v1/webhooks/456')
    
    assert 'Invalid token, try to refresh it' in str(excinfo.value)


def test_api_base_delete_request_403_error(mocker):
    """
    Test ApiBase _delete_request method with 403 error
    """
    api_base = ApiBase()
    api_base.set_api_token(api_token)
    api_base.set_sub_domain(sub_domain)
    
    mock_requests_delete_403_error(mocker)
    
    with pytest.raises(NoPrivilegeError) as excinfo:
        api_base._delete_request('/v1/webhooks/456')
    
    assert 'Forbidden, the user has insufficient privilege' in str(excinfo.value)


def test_api_base_delete_request_404_error(mocker):
    """
    Test ApiBase _delete_request method with 404 error
    """
    api_base = ApiBase()
    api_base.set_api_token(api_token)
    api_base.set_sub_domain(sub_domain)
    
    mock_requests_delete_404_error(mocker)
    
    with pytest.raises(NotFoundItemError) as excinfo:
        api_base._delete_request('/v1/webhooks/456')
    
    assert 'Not found item with ID' in str(excinfo.value)


def test_api_base_delete_request_500_error(mocker):
    """
    Test ApiBase _delete_request method with 500 error
    """
    api_base = ApiBase()
    api_base.set_api_token(api_token)
    api_base.set_sub_domain(sub_domain)
    
    mock_requests_delete_500_error(mocker)
    
    with pytest.raises(BambooHrSDKError) as excinfo:
        api_base._delete_request('/v1/webhooks/456')
    
    assert 'Status code 500' in str(excinfo.value)


def test_api_base_url_construction():
    """
    Test ApiBase URL construction
    """
    api_base = ApiBase()
    api_base.set_sub_domain(sub_domain)
    
    expected_base_url = f'https://api.bamboohr.com/api/gateway.php/{sub_domain}'
    actual_base_url = api_base.API_BASE_URL.format(sub_domain)
    
    assert actual_base_url == expected_base_url


def test_api_base_with_none_values():
    """
    Test ApiBase with None values
    """
    api_base = ApiBase()
    
    # Test with None api_token
    api_base.set_api_token(None)
    assert api_base._ApiBase__api_token is None
    
    # Test with None sub_domain
    api_base.set_sub_domain(None)
    assert api_base._ApiBase__sub_domain is None


def test_api_base_with_empty_strings():
    """
    Test ApiBase with empty strings
    """
    api_base = ApiBase()
    
    # Test with empty api_token
    api_base.set_api_token('')
    assert api_base._ApiBase__api_token == ''
    
    # Test with empty sub_domain
    api_base.set_sub_domain('')
    assert api_base._ApiBase__sub_domain == '' 
