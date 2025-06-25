"""
Mock setup functions for BambooHR tests
"""


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


def mock_test_post_configuration_view_case_1(mocker):
    """
    Mock setup for test_post_configuration_view_case_1
    Provides test data for configuration view
    """
    return {
        'configuration_data': {
            "additional_email_options": {},
            "emails_selected": [
                {
                    "name": "Nilesh",
                    "email": "nilesh.p@fyle.in"
                },
            ]
        }
    }


def mock_test_post_bamboohr_connection_view_case_1(mocker):
    """
    Mock setup for test_post_bamboohr_connection_view_case_1
    Provides invalid connection payload
    """
    return {
        'bamboo_connection_invalid_payload': {
            'input': {
                'api_token': 'sample_token',
            }
        }
    }


def mock_test_post_bamboohr_connection_view_case_2(mocker):
    """
    Mock setup for test_post_bamboohr_connection_view_case_2
    Provides valid connection payload
    """
    return {
        'bamboo_connection': {
            'input': {
                'api_token': 'sample_token',
                'subdomain': 'somesubdomain'
            }
        }
    }


def mock_test_post_bamboohr_connection_view_case_3(mocker):
    """
    Mock setup for test_post_bamboohr_connection_view_case_3
    Provides valid connection payload and expected response
    """
    return {
        'bamboo_connection': {
            'input': {
                'api_token': 'sample_token',
                'subdomain': 'somesubdomain'
            }
        },
        'integrations_response': {
            "org_id": "orTwovfDpEYc",
            "org_name": "Test org",
            "tpa_id": "dummy",
            "tpa_name": "Fyle BambooHR Integration",
            "type": "HRMS",
            "is_active": True,
            "is_beta": True,
            "connected_at": "2025-01-09T10:08:20.434443Z",
            "disconnected_at": None,
            "updated_at": "2025-01-09T10:08:20.434443Z"
        }
    }


def mock_test_post_bamboohr_disconnect_view_case_2(mocker):
    """
    Mock setup for test_post_bamboohr_disconnect_view_case_2
    Provides connection payload for disconnect test
    """
    return {
        'bamboo_connection': {
            'input': {
                'api_token': 'sample_token',
                'subdomain': 'somesubdomain'
            }
        }
    } 
