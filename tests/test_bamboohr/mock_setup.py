"""
Mock setup functions for BambooHR tests
"""


def mock_bamboohr_sdk_invalid_token(mocker):
    """
    Mock BambooHR SDK with invalid token response
    """
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.time_off.get.return_value = {}
    mocker.patch('apps.bamboohr.views.BambooHrSDK', return_value=mock_bamboohr_sdk)
    return mock_bamboohr_sdk


def mock_bamboohr_sdk_valid_token(mocker):
    """
    Mock BambooHR SDK with valid token response
    """
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.time_off.get.return_value = {'timeOffTypes': True}
    mocker.patch('apps.bamboohr.views.BambooHrSDK', return_value=mock_bamboohr_sdk)
    return mock_bamboohr_sdk


def mock_bamboohr_shared_mock(mocker):
    """
    Shared mock setup for BambooHR tests
    Returns a dictionary of mocks that can be used with mock_dependencies
    """
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.time_off.get.return_value = {'timeOffTypes': True}
    mock_bamboohr_sdk.employee.get.return_value = {'employees': []}
    
    mocker.patch('apps.bamboohr.views.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    return {
        'bamboohr_sdk': mock_bamboohr_sdk,
        'time_off_get': mock_bamboohr_sdk.time_off.get,
        'employee_get': mock_bamboohr_sdk.employee.get,
    }


def mock_bamboohr_invalid_token_shared_mock(mocker):
    """
    Shared mock setup for BambooHR invalid token tests
    Returns a dictionary of mocks that can be used with mock_dependencies
    """
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.time_off.get.return_value = {}
    mock_bamboohr_sdk.employee.get.return_value = {'employees': []}
    
    mocker.patch('apps.bamboohr.views.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    return {
        'bamboohr_sdk': mock_bamboohr_sdk,
        'time_off_get': mock_bamboohr_sdk.time_off.get,
        'employee_get': mock_bamboohr_sdk.employee.get,
    } 
