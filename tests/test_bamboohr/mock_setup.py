"""
Mock setup for bamboohr tests.
Contains all mocking patterns used across bamboohr test files.
"""

import pytest
from bamboosdk.exceptions import InvalidTokenError

from apps.bamboohr.views import BambooHrSDK


def mock_sendgrid_email_shared_mock(mocker):
    """
    Shared mock for SendGrid email operations
    """
    mock_sendgrid = mocker.patch('apps.bamboohr.email.sendgrid.SendGridAPIClient')
    mock_sg_instance = mocker.MagicMock()
    mock_sendgrid.return_value = mock_sg_instance
    
    return {
        'mock_sendgrid': mock_sendgrid,
        'mock_sg_instance': mock_sg_instance
    }


def mock_bamboohr_sdk_invalid_token_shared_mock(mocker):
    """
    Shared mock for BambooHrSDK with invalid token
    """
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.time_off.get.side_effect = InvalidTokenError('Invalid token')
    mock_bamboohr_sdk.employees.get.side_effect = InvalidTokenError('Invalid token')
    mocker.patch('apps.bamboohr.views.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    return {
        'mock_bamboohr_sdk': mock_bamboohr_sdk
    }


def mock_bamboohr_sdk_empty_response_shared_mock(mocker):
    """
    Shared mock for BambooHrSDK with empty response
    """
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.time_off.get.return_value = {'timeOffTypes': []}
    mock_bamboohr_sdk.employees.get.return_value = {'employees': []}
    mocker.patch('apps.bamboohr.views.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    return {
        'mock_bamboohr_sdk': mock_bamboohr_sdk
    }


def mock_bamboohr_connection_shared_mock(mocker):
    """
    Shared mock for BambooHrSDK with valid connection
    """
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.time_off.get.return_value = {'timeOffTypes': True}
    mock_bamboohr_sdk.employees.get.return_value = {'employees': [{'id': 1, 'name': 'Test User'}]}
    mocker.patch('apps.bamboohr.views.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    return {
        'mock_bamboohr_sdk': mock_bamboohr_sdk
    }


def mock_bamboohr_sdk_success_shared_mock(mocker):
    """
    Shared mock for BambooHrSDK with success response
    """
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.time_off.get.return_value = {'timeOffTypes': True}
    mocker.patch('apps.bamboohr.views.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    return {
        'mock_bamboohr_sdk': mock_bamboohr_sdk
    }


def mock_bamboohr_health_check_shared_mock(mocker):
    """
    Shared mock for BambooHR health check operations
    """
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.time_off.get.return_value = {'timeOffTypes': True}
    mock_bamboohr_sdk.employees.get.return_value = {'employees': [{'id': 1, 'name': 'Test User'}]}
    
    # Patch the SDK in views where it's actually used
    mocker.patch('apps.bamboohr.views.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    return {
        'mock_bamboohr_sdk': mock_bamboohr_sdk
    }


def mock_bamboohr_webhook_shared_mock(mocker):
    """
    Shared mock for BambooHR webhook operations
    """
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.time_off.get.return_value = {'timeOffTypes': True}
    
    # Patch the SDK in views where it's actually used
    mocker.patch('apps.bamboohr.views.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    # Mock async task
    mock_async_task = mocker.patch('apps.bamboohr.views.async_task')
    
    return {
        'mock_bamboohr_sdk': mock_bamboohr_sdk,
        'mock_async_task': mock_async_task
    }


def mock_bamboohr_sdk_error_response_shared_mock(mocker, error_response):
    """
    Shared mock for BambooHrSDK with error response
    """
    mock_bamboohr_sdk = mocker.MagicMock()
    if isinstance(error_response, Exception):
        mock_bamboohr_sdk.time_off.get.side_effect = error_response
    else:
        mock_bamboohr_sdk.time_off.get.return_value = error_response
    mocker.patch('apps.bamboohr.views.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    return {
        'mock_bamboohr_sdk': mock_bamboohr_sdk
    }


def mock_bamboohr_async_task_shared_mock(mocker):
    """
    Shared mock for async task operations
    """
    mock_async_task = mocker.patch('apps.bamboohr.views.async_task')
    
    return {
        'mock_async_task': mock_async_task
    } 
