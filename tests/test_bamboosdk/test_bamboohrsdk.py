import pytest
from bamboosdk.bamboohrsdk import BambooHrSDK
from bamboosdk.api.employee import Employee
from bamboosdk.api.webhook import Webhook
from bamboosdk.api.time_off import TimeOff
from .fixtures import (
    api_token,
    sub_domain,
    invalid_api_token,
    invalid_sub_domain
)


def test_bamboo_hr_sdk_initialization():
    """
    Test BambooHrSDK initialization
    """
    sdk = BambooHrSDK(api_token, sub_domain)
    
    assert sdk._BambooHrSDK__api_token == api_token
    assert sdk._BambooHrSDK__sub_domain == sub_domain
    assert isinstance(sdk.employees, Employee)
    assert isinstance(sdk.webhook, Webhook)
    assert isinstance(sdk.time_off, TimeOff)


def test_bamboo_hr_sdk_api_token_setting():
    """
    Test BambooHrSDK API token setting
    """
    sdk = BambooHrSDK(api_token, sub_domain)
    
    # Access the private attribute through the correct class
    assert hasattr(sdk.employees, '_ApiBase__api_token')
    assert hasattr(sdk.webhook, '_ApiBase__api_token')
    assert hasattr(sdk.time_off, '_ApiBase__api_token')


def test_bamboo_hr_sdk_sub_domain_setting():
    """
    Test BambooHrSDK sub domain setting
    """
    sdk = BambooHrSDK(api_token, sub_domain)
    
    # Access the private attribute through the correct class
    assert hasattr(sdk.employees, '_ApiBase__sub_domain')
    assert hasattr(sdk.webhook, '_ApiBase__sub_domain')
    assert hasattr(sdk.time_off, '_ApiBase__sub_domain')


def test_bamboo_hr_sdk_headers_setting():
    """
    Test BambooHrSDK headers setting
    """
    sdk = BambooHrSDK(api_token, sub_domain)
    
    assert sdk.employees.headers is not None
    assert sdk.webhook.headers is not None
    assert sdk.time_off.headers is not None
    
    assert 'Accept' in sdk.employees.headers
    assert 'content-type' in sdk.employees.headers
    assert 'authorization' in sdk.employees.headers
    
    assert sdk.employees.headers['Accept'] == 'application/json'
    assert sdk.employees.headers['content-type'] == 'application/json'
    assert 'Basic' in sdk.employees.headers['authorization']


def test_bamboo_hr_sdk_set_api_token():
    """
    Test BambooHrSDK set_api_token method
    """
    sdk = BambooHrSDK(api_token, sub_domain)
    
    new_api_token = 'new_test_token'
    sdk._BambooHrSDK__api_token = new_api_token
    sdk.set_api_token()
    
    # Verify the method exists and was called
    assert hasattr(sdk, 'set_api_token')
    assert callable(sdk.set_api_token)


def test_bamboo_hr_sdk_set_sub_domain():
    """
    Test BambooHrSDK set_sub_domain method
    """
    sdk = BambooHrSDK(api_token, sub_domain)
    
    new_sub_domain = 'new_test_subdomain'
    sdk._BambooHrSDK__sub_domain = new_sub_domain
    sdk.set_sub_domain()
    
    # Verify the method exists and was called
    assert hasattr(sdk, 'set_sub_domain')
    assert callable(sdk.set_sub_domain)


def test_bamboo_hr_sdk_with_invalid_token():
    """
    Test BambooHrSDK initialization with invalid token
    """
    sdk = BambooHrSDK(invalid_api_token, sub_domain)
    
    assert sdk._BambooHrSDK__api_token == invalid_api_token
    assert sdk._BambooHrSDK__sub_domain == sub_domain


def test_bamboo_hr_sdk_with_invalid_sub_domain():
    """
    Test BambooHrSDK initialization with invalid sub domain
    """
    sdk = BambooHrSDK(api_token, invalid_sub_domain)
    
    assert sdk._BambooHrSDK__api_token == api_token
    assert sdk._BambooHrSDK__sub_domain == invalid_sub_domain


def test_bamboo_hr_sdk_with_empty_token():
    """
    Test BambooHrSDK initialization with empty token
    """
    empty_token = ''
    sdk = BambooHrSDK(empty_token, sub_domain)
    
    assert sdk._BambooHrSDK__api_token == empty_token
    assert sdk._BambooHrSDK__sub_domain == sub_domain


def test_bamboo_hr_sdk_with_empty_sub_domain():
    """
    Test BambooHrSDK initialization with empty sub domain
    """
    empty_sub_domain = ''
    sdk = BambooHrSDK(api_token, empty_sub_domain)
    
    assert sdk._BambooHrSDK__api_token == api_token
    assert sdk._BambooHrSDK__sub_domain == empty_sub_domain


def test_bamboo_hr_sdk_api_instances():
    """
    Test BambooHrSDK API instances are properly created
    """
    sdk = BambooHrSDK(api_token, sub_domain)
    
    assert hasattr(sdk, 'employees')
    assert hasattr(sdk, 'webhook')
    assert hasattr(sdk, 'time_off')
    
    assert callable(getattr(sdk.employees, 'get_all', None))
    assert callable(getattr(sdk.employees, 'get', None))
    assert callable(getattr(sdk.webhook, 'post', None))
    assert callable(getattr(sdk.webhook, 'delete', None))
    assert callable(getattr(sdk.time_off, 'get', None))


def test_bamboo_hr_sdk_multiple_instances():
    """
    Test creating multiple BambooHrSDK instances
    """
    sdk1 = BambooHrSDK(api_token, sub_domain)
    sdk2 = BambooHrSDK('another_token', 'another_domain')
    
    assert sdk1._BambooHrSDK__api_token != sdk2._BambooHrSDK__api_token
    assert sdk1._BambooHrSDK__sub_domain != sdk2._BambooHrSDK__sub_domain
    
    # Verify instances are different
    assert sdk1.employees != sdk2.employees
    assert sdk1.webhook != sdk2.webhook
    assert sdk1.time_off != sdk2.time_off 
