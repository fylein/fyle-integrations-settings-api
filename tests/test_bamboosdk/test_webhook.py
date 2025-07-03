import pytest
from bamboosdk.api.webhook import Webhook
from bamboosdk.exceptions import (
    BambooHrSDKError,
    NoPrivilegeError,
    NotFoundItemError,
    InvalidTokenError
)
from .fixtures import (
    api_token,
    sub_domain,
    webhook_id,
    webhook_payload,
    webhook_creation_response,
    webhook_deletion_response
)
from .mock_setup import (
    mock_webhook_post_success,
    mock_webhook_delete_success,
    mock_requests_post_401_error,
    mock_requests_post_403_error,
    mock_requests_post_404_error,
    mock_requests_post_500_error,
    mock_requests_delete_401_error,
    mock_requests_delete_403_error,
    mock_requests_delete_404_error,
    mock_requests_delete_500_error
)


def test_webhook_initialization():
    """
    Test Webhook class initialization
    """
    webhook_api = Webhook()
    
    assert webhook_api.POST_WEBHOOK == '/v1/webhooks/'
    assert webhook_api.DELETE_WEBHOOK == '/v1/webhooks/{}'
    assert webhook_api._ApiBase__api_token is None
    assert webhook_api._ApiBase__sub_domain is None
    assert webhook_api.headers is None


def test_webhook_post_success(mocker):
    """
    Test Webhook post method with success response
    """
    webhook_api = Webhook()
    webhook_api.set_api_token(api_token)
    webhook_api.set_sub_domain(sub_domain)
    
    mock_webhook_post_success(mocker)
    
    result = webhook_api.post(webhook_payload)
    
    assert result == webhook_creation_response


def test_webhook_post_401_error(mocker):
    """
    Test Webhook post method with 401 error
    """
    webhook_api = Webhook()
    webhook_api.set_api_token(api_token)
    webhook_api.set_sub_domain(sub_domain)
    
    mock_requests_post_401_error(mocker)
    
    with pytest.raises(InvalidTokenError):
        webhook_api.post(webhook_payload)


def test_webhook_post_403_error(mocker):
    """
    Test Webhook post method with 403 error
    """
    webhook_api = Webhook()
    webhook_api.set_api_token(api_token)
    webhook_api.set_sub_domain(sub_domain)
    
    mock_requests_post_403_error(mocker)
    
    with pytest.raises(NoPrivilegeError):
        webhook_api.post(webhook_payload)


def test_webhook_post_404_error(mocker):
    """
    Test Webhook post method with 404 error
    """
    webhook_api = Webhook()
    webhook_api.set_api_token(api_token)
    webhook_api.set_sub_domain(sub_domain)
    
    mock_requests_post_404_error(mocker)
    
    with pytest.raises(NotFoundItemError):
        webhook_api.post(webhook_payload)


def test_webhook_post_500_error(mocker):
    """
    Test Webhook post method with 500 error
    """
    webhook_api = Webhook()
    webhook_api.set_api_token(api_token)
    webhook_api.set_sub_domain(sub_domain)
    
    mock_requests_post_500_error(mocker)
    
    with pytest.raises(BambooHrSDKError):
        webhook_api.post(webhook_payload)


def test_webhook_delete_success(mocker):
    """
    Test Webhook delete method with success response
    """
    webhook_api = Webhook()
    webhook_api.set_api_token(api_token)
    webhook_api.set_sub_domain(sub_domain)
    
    mock_webhook_delete_success(mocker)
    
    result = webhook_api.delete(webhook_id)
    
    assert result == webhook_deletion_response


def test_webhook_delete_401_error(mocker):
    """
    Test Webhook delete method with 401 error
    """
    webhook_api = Webhook()
    webhook_api.set_api_token(api_token)
    webhook_api.set_sub_domain(sub_domain)
    
    mock_requests_delete_401_error(mocker)
    
    with pytest.raises(InvalidTokenError):
        webhook_api.delete(webhook_id)


def test_webhook_delete_403_error(mocker):
    """
    Test Webhook delete method with 403 error
    """
    webhook_api = Webhook()
    webhook_api.set_api_token(api_token)
    webhook_api.set_sub_domain(sub_domain)
    
    mock_requests_delete_403_error(mocker)
    
    with pytest.raises(NoPrivilegeError):
        webhook_api.delete(webhook_id)


def test_webhook_delete_404_error(mocker):
    """
    Test Webhook delete method with 404 error
    """
    webhook_api = Webhook()
    webhook_api.set_api_token(api_token)
    webhook_api.set_sub_domain(sub_domain)
    
    mock_requests_delete_404_error(mocker)
    
    with pytest.raises(NotFoundItemError):
        webhook_api.delete(webhook_id)


def test_webhook_delete_500_error(mocker):
    """
    Test Webhook delete method with 500 error
    """
    webhook_api = Webhook()
    webhook_api.set_api_token(api_token)
    webhook_api.set_sub_domain(sub_domain)
    
    mock_requests_delete_500_error(mocker)
    
    with pytest.raises(BambooHrSDKError):
        webhook_api.delete(webhook_id)


def test_webhook_url_formatting():
    """
    Test Webhook URL formatting
    """
    webhook_api = Webhook()
    
    # Test DELETE_WEBHOOK URL formatting
    expected_url = f'/v1/webhooks/{webhook_id}'
    actual_url = webhook_api.DELETE_WEBHOOK.format(webhook_id)
    
    assert actual_url == expected_url


def test_webhook_inheritance():
    """
    Test Webhook inheritance from ApiBase
    """
    webhook_api = Webhook()
    
    # Test that Webhook inherits from ApiBase
    assert hasattr(webhook_api, 'set_api_token')
    assert hasattr(webhook_api, 'set_sub_domain')
    assert hasattr(webhook_api, '_get_request')
    assert hasattr(webhook_api, '_post_request')
    assert hasattr(webhook_api, '_delete_request')
    assert hasattr(webhook_api, 'API_BASE_URL')
    
    # Test Webhook-specific attributes
    assert hasattr(webhook_api, 'POST_WEBHOOK')
    assert hasattr(webhook_api, 'DELETE_WEBHOOK')
    assert hasattr(webhook_api, 'post')
    assert hasattr(webhook_api, 'delete')


def test_webhook_post_with_empty_payload(mocker):
    """
    Test Webhook post method with empty payload
    """
    webhook_api = Webhook()
    webhook_api.set_api_token(api_token)
    webhook_api.set_sub_domain(sub_domain)
    
    mock_webhook_post_success(mocker)
    
    result = webhook_api.post({})
    
    assert result == webhook_creation_response


def test_webhook_post_with_none_payload(mocker):
    """
    Test Webhook post method with None payload
    """
    webhook_api = Webhook()
    webhook_api.set_api_token(api_token)
    webhook_api.set_sub_domain(sub_domain)
    
    mock_webhook_post_success(mocker)
    
    result = webhook_api.post(None)
    
    assert result == webhook_creation_response


def test_webhook_delete_with_none_id(mocker):
    """
    Test Webhook delete method with None ID
    """
    webhook_api = Webhook()
    webhook_api.set_api_token(api_token)
    webhook_api.set_sub_domain(sub_domain)
    
    mock_webhook_delete_success(mocker)
    
    result = webhook_api.delete(None)
    
    assert result == webhook_deletion_response


def test_webhook_delete_with_empty_string_id(mocker):
    """
    Test Webhook delete method with empty string ID
    """
    webhook_api = Webhook()
    webhook_api.set_api_token(api_token)
    webhook_api.set_sub_domain(sub_domain)
    
    mock_webhook_delete_success(mocker)
    
    result = webhook_api.delete('')
    
    assert result == webhook_deletion_response


def test_webhook_post_with_complex_payload(mocker):
    """
    Test Webhook post method with complex payload
    """
    webhook_api = Webhook()
    webhook_api.set_api_token(api_token)
    webhook_api.set_sub_domain(sub_domain)
    
    mock_webhook_post_success(mocker)
    
    complex_payload = {
        'name': 'Complex Webhook',
        'url': 'https://complex.example.com/webhook',
        'format': 'json',
        'frequency': {
            'hour': 2,
            'minute': 30
        },
        'limit': 50,
        'postFields': {
            'employee': ['id', 'firstName', 'lastName', 'workEmail', 'department', 'supervisorEmail'],
            'timeOff': ['id', 'type', 'start', 'end', 'status']
        },
        'monitorFields': ['firstName', 'lastName', 'workEmail'],
        'includeChildTables': True
    }
    
    result = webhook_api.post(complex_payload)
    
    assert result == webhook_creation_response


def test_webhook_url_constants():
    """
    Test Webhook URL constants
    """
    webhook_api = Webhook()
    
    # Test POST_WEBHOOK constant
    assert webhook_api.POST_WEBHOOK == '/v1/webhooks/'
    assert webhook_api.POST_WEBHOOK.endswith('/')
    
    # Test DELETE_WEBHOOK constant
    assert webhook_api.DELETE_WEBHOOK == '/v1/webhooks/{}'
    assert '{}' in webhook_api.DELETE_WEBHOOK
    assert webhook_api.DELETE_WEBHOOK.startswith('/v1/webhooks/')


def test_webhook_method_calls():
    """
    Test Webhook method calls without actual API requests
    """
    webhook_api = Webhook()
    
    # Mock the underlying methods to avoid actual API calls
    webhook_api._post_request = lambda url, payload: webhook_creation_response
    webhook_api._delete_request = lambda url: webhook_deletion_response
    
    # Test post method
    post_result = webhook_api.post(webhook_payload)
    assert post_result == webhook_creation_response
    
    # Test delete method
    delete_result = webhook_api.delete(webhook_id)
    assert delete_result == webhook_deletion_response 
