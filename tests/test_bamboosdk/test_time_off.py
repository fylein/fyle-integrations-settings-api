import pytest
from bamboosdk.api.time_off import TimeOff
from bamboosdk.exceptions import (
    BambooHrSDKError,
    NoPrivilegeError,
    NotFoundItemError,
    InvalidTokenError
)
from .fixtures import (
    api_token,
    sub_domain,
    time_off_types_response
)
from .mock_setup import (
    mock_time_off_get_success,
    mock_requests_get_401_error,
    mock_requests_get_403_error,
    mock_requests_get_404_error,
    mock_requests_get_500_error
)


def test_time_off_initialization():
    """
    Test TimeOff class initialization
    """
    time_off_api = TimeOff()
    
    assert time_off_api.CHECK_URL == '/v1/meta/time_off/types/'
    assert hasattr(time_off_api, '_ApiBase__api_token')
    assert hasattr(time_off_api, '_ApiBase__sub_domain')
    assert time_off_api.headers is None


def test_time_off_get_success(mocker):
    """
    Test TimeOff get method with success response
    """
    time_off_api = TimeOff()
    time_off_api.set_api_token(api_token)
    time_off_api.set_sub_domain(sub_domain)
    
    mock_time_off_get_success(mocker)
    
    result = time_off_api.get()
    
    assert result == time_off_types_response


def test_time_off_get_401_error(mocker):
    """
    Test TimeOff get method with 401 error
    """
    time_off_api = TimeOff()
    time_off_api.set_api_token(api_token)
    time_off_api.set_sub_domain(sub_domain)
    
    mock_requests_get_401_error(mocker)
    
    with pytest.raises(InvalidTokenError):
        time_off_api.get()


def test_time_off_get_403_error(mocker):
    """
    Test TimeOff get method with 403 error
    """
    time_off_api = TimeOff()
    time_off_api.set_api_token(api_token)
    time_off_api.set_sub_domain(sub_domain)
    
    mock_requests_get_403_error(mocker)
    
    with pytest.raises(NoPrivilegeError):
        time_off_api.get()


def test_time_off_get_404_error(mocker):
    """
    Test TimeOff get method with 404 error
    """
    time_off_api = TimeOff()
    time_off_api.set_api_token(api_token)
    time_off_api.set_sub_domain(sub_domain)
    
    mock_requests_get_404_error(mocker)
    
    with pytest.raises(NotFoundItemError):
        time_off_api.get()


def test_time_off_get_500_error(mocker):
    """
    Test TimeOff get method with 500 error
    """
    time_off_api = TimeOff()
    time_off_api.set_api_token(api_token)
    time_off_api.set_sub_domain(sub_domain)
    
    mock_requests_get_500_error(mocker)
    
    with pytest.raises(BambooHrSDKError):
        time_off_api.get()


def test_time_off_inheritance():
    """
    Test TimeOff inheritance from ApiBase
    """
    time_off_api = TimeOff()
    
    # Test that TimeOff inherits from ApiBase
    assert hasattr(time_off_api, 'set_api_token')
    assert hasattr(time_off_api, 'set_sub_domain')
    assert hasattr(time_off_api, '_get_request')
    assert hasattr(time_off_api, '_post_request')
    assert hasattr(time_off_api, '_delete_request')
    assert hasattr(time_off_api, 'API_BASE_URL')
    
    # Test TimeOff-specific attributes
    assert hasattr(time_off_api, 'CHECK_URL')
    assert hasattr(time_off_api, 'get')


def test_time_off_url_constant():
    """
    Test TimeOff CHECK_URL constant
    """
    time_off_api = TimeOff()
    
    # Test CHECK_URL constant
    assert time_off_api.CHECK_URL == '/v1/meta/time_off/types/'
    assert time_off_api.CHECK_URL.startswith('/v1/meta/')
    assert time_off_api.CHECK_URL.endswith('/')
    assert 'time_off' in time_off_api.CHECK_URL
    assert 'types' in time_off_api.CHECK_URL


def test_time_off_method_call():
    """
    Test TimeOff method call without actual API request
    """
    time_off_api = TimeOff()
    
    # Mock the underlying method to avoid actual API call
    time_off_api._get_request = lambda url: time_off_types_response
    
    # Test get method
    result = time_off_api.get()
    assert result == time_off_types_response


def test_time_off_api_setup():
    """
    Test TimeOff API setup with token and subdomain
    """
    time_off_api = TimeOff()
    
    # Test setting API token
    time_off_api.set_api_token(api_token)
    assert hasattr(time_off_api, '_ApiBase__api_token')
    assert time_off_api.headers is not None
    
    # Test setting subdomain
    time_off_api.set_sub_domain(sub_domain)
    assert hasattr(time_off_api, '_ApiBase__sub_domain')


def test_time_off_with_none_token():
    """
    Test TimeOff with None API token
    """
    time_off_api = TimeOff()
    
    # Set None token
    time_off_api.set_api_token(None)
    assert hasattr(time_off_api, '_ApiBase__api_token')


def test_time_off_with_empty_token():
    """
    Test TimeOff with empty API token
    """
    time_off_api = TimeOff()
    
    # Set empty token
    time_off_api.set_api_token('')
    assert hasattr(time_off_api, '_ApiBase__api_token')


def test_time_off_with_none_subdomain():
    """
    Test TimeOff with None subdomain
    """
    time_off_api = TimeOff()
    
    # Set None subdomain
    time_off_api.set_sub_domain(None)
    assert hasattr(time_off_api, '_ApiBase__sub_domain')


def test_time_off_with_empty_subdomain():
    """
    Test TimeOff with empty subdomain
    """
    time_off_api = TimeOff()
    
    # Set empty subdomain
    time_off_api.set_sub_domain('')
    assert hasattr(time_off_api, '_ApiBase__sub_domain')


def test_time_off_get_method_signature():
    """
    Test TimeOff get method signature
    """
    time_off_api = TimeOff()
    
    # Test that get method exists and is callable
    assert hasattr(time_off_api, 'get')
    assert callable(time_off_api.get)
    
    # Test that get method accepts no parameters
    import inspect
    signature = inspect.signature(time_off_api.get)
    assert len(signature.parameters) == 0


def test_time_off_check_connection_purpose():
    """
    Test TimeOff get method purpose for checking connection
    """
    time_off_api = TimeOff()
    
    # Mock successful connection check
    time_off_api._get_request = lambda url: time_off_types_response
    
    # The get method is used for checking connection
    result = time_off_api.get()
    
    # Should return valid time off types indicating successful connection
    assert result == time_off_types_response
    assert 'timeOffTypes' in result
    assert len(result['timeOffTypes']) > 0


def test_time_off_error_propagation(mocker):
    """
    Test TimeOff error propagation from underlying API base
    """
    time_off_api = TimeOff()
    time_off_api.set_api_token(api_token)
    time_off_api.set_sub_domain(sub_domain)
    
    # Test different error scenarios
    error_scenarios = [
        (mock_requests_get_401_error, InvalidTokenError),
        (mock_requests_get_403_error, NoPrivilegeError),
        (mock_requests_get_404_error, NotFoundItemError),
        (mock_requests_get_500_error, BambooHrSDKError)
    ]
    
    for mock_function, expected_error in error_scenarios:
        mock_function(mocker)
        
        with pytest.raises(expected_error):
            time_off_api.get()


def test_time_off_api_base_inheritance():
    """
    Test TimeOff properly inherits ApiBase functionality
    """
    time_off_api = TimeOff()
    
    # Test all inherited methods exist
    inherited_methods = [
        'set_api_token',
        'set_sub_domain',
        '_get_request',
        '_post_request',
        '_delete_request'
    ]
    
    for method in inherited_methods:
        assert hasattr(time_off_api, method)
        assert callable(getattr(time_off_api, method))
    
    # Test inherited attributes exist
    inherited_attributes = ['API_BASE_URL']
    
    for attribute in inherited_attributes:
        assert hasattr(time_off_api, attribute) 
