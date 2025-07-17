"""
Mock setup functions for BambooHR tests
"""

from .fixtures import (
    configuration_data,
    bamboo_connection_invalid_payload,
    bamboo_connection,
    bamboohr_integrations_response,
    failed_employees_data,
    admin_email_list,
    number_of_employees,
    email_template_content,
    webhook_payload,
    bamboohr_timeoff_success_response,
    bamboohr_timeoff_empty_response,
    sync_employees_request_data,
    invalid_configuration_data
)


def mock_bamboohr_shared_mock(mocker):
    """
    Shared mock setup for BambooHR tests
    Returns a dictionary of mocks that can be used with mock_dependencies
    """
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.time_off.get.return_value = bamboohr_timeoff_success_response
    mock_bamboohr_sdk.employee.get.return_value = {'employees': []}
    
    mocker.patch('apps.bamboohr.views.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    mock_request = mocker.MagicMock()
    mock_request.query_params.get.return_value = '1'
    
    mock_add_to_integrations = mocker.patch('apps.bamboohr.views.add_bamboo_hr_to_integrations')
    
    mock_delete_sync_schedule = mocker.patch('apps.bamboohr.views.delete_sync_employee_schedule')
    mock_deactivate_integration = mocker.patch('apps.bamboohr.views.deactivate_bamboo_hr_integration')
    
    return {
        'bamboohr_sdk': mock_bamboohr_sdk,
        'time_off_get': mock_bamboohr_sdk.time_off.get,
        'employee_get': mock_bamboohr_sdk.employee.get,
        'add_to_integrations': mock_add_to_integrations,
        'delete_sync_schedule': mock_delete_sync_schedule,
        'deactivate_integration': mock_deactivate_integration,
        'request_mock': mock_request,
    }


def mock_bamboohr_invalid_token_shared_mock(mocker):
    """
    Shared mock setup for BambooHR invalid token tests
    Returns a dictionary of mocks that can be used with mock_dependencies
    """
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.time_off.get.return_value = bamboohr_timeoff_empty_response
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
        'configuration_data': configuration_data
    }


def mock_test_post_configuration_view_case_2(mocker):
    """
    Mock setup for test_post_configuration_view_case_2
    Provides invalid configuration data for exception testing
    """
    return {
        'invalid_configuration_data': invalid_configuration_data
    }


def mock_test_post_bamboohr_connection_view_case_1(mocker):
    """
    Mock setup for test_post_bamboohr_connection_view_case_1
    Provides invalid connection payload
    """
    return {
        'bamboo_connection_invalid_payload': bamboo_connection_invalid_payload
    }


def mock_test_post_bamboohr_connection_view_case_2(mocker):
    """
    Mock setup for test_post_bamboohr_connection_view_case_2
    Provides valid connection payload
    """
    return {
        'bamboo_connection': bamboo_connection
    }


def mock_test_post_bamboohr_connection_view_case_3(mocker):
    """
    Mock setup for test_post_bamboohr_connection_view_case_3
    Provides valid connection payload and expected response
    """
    return {
        'bamboo_connection': bamboo_connection,
        'integrations_response': bamboohr_integrations_response
    }


def mock_test_post_bamboohr_connection_view_case_4(mocker):
    """
    Mock setup for test_post_bamboohr_connection_view_case_4
    Provides valid connection payload for empty timeOffTypes test
    """
    return {
        'bamboo_connection': bamboo_connection
    }


def mock_test_post_bamboohr_disconnect_view_case_2(mocker):
    """
    Mock setup for test_post_bamboohr_disconnect_view_case_2
    Provides connection payload for disconnect test
    """
    return {
        'bamboo_connection': bamboo_connection
    }


def mock_test_send_failure_notification_email(mocker):
    """
    Mock setup for test_send_failure_notification_email
    Mocks file operations and SendGrid client
    """
    mock_open = mocker.patch('builtins.open')
    mock_sendgrid_client = mocker.MagicMock()
    mock_sendgrid_api = mocker.patch('apps.bamboohr.email.sendgrid.SendGridAPIClient', return_value=mock_sendgrid_client)
    
    # Mock settings
    mocker.patch('apps.bamboohr.email.settings.SENDGRID_EMAIL', 'admin@example.com')
    mocker.patch('apps.bamboohr.email.settings.SENDGRID_API_KEY', 'test_api_key')
    
    return {
        'open': mock_open,
        'sendgrid_client': mock_sendgrid_client,
        'sendgrid_api': mock_sendgrid_api,
        'failed_employees_data': failed_employees_data,
        'admin_email_list': admin_email_list,
        'number_of_employees': number_of_employees
    }


def mock_test_import_employees(mocker):
    """
    Mock setup for test_import_employees
    Mocks BambooHrEmployeeImport
    """
    mock_bamboo_hr_importer = mocker.MagicMock()
    mock_bamboo_hr_employee_import = mocker.patch(
        'apps.bamboohr.tasks.BambooHrEmployeeImport',
        return_value=mock_bamboo_hr_importer
    )
    
    return {
        'bamboo_hr_employee_import': mock_bamboo_hr_employee_import,
        'sync_employees': mock_bamboo_hr_importer.sync_employees
    }


def mock_test_import_employees_without_incremental_sync(mocker):
    """
    Mock setup for test_import_employees_without_incremental_sync
    Mocks BambooHrEmployeeImport
    """
    mock_bamboo_hr_importer = mocker.MagicMock()
    mock_bamboo_hr_employee_import = mocker.patch(
        'apps.bamboohr.tasks.BambooHrEmployeeImport',
        return_value=mock_bamboo_hr_importer
    )
    
    return {
        'bamboo_hr_employee_import': mock_bamboo_hr_employee_import,
        'sync_employees': mock_bamboo_hr_importer.sync_employees
    }


def mock_test_update_employee(mocker):
    """
    Mock setup for test_update_employee
    Mocks BambooHrEmployeeImport
    """
    mock_bamboo_hr_importer = mocker.MagicMock()
    mock_bamboo_hr_employee_import = mocker.patch(
        'apps.bamboohr.tasks.BambooHrEmployeeImport',
        return_value=mock_bamboo_hr_importer
    )
    
    return {
        'bamboo_hr_employee_import': mock_bamboo_hr_employee_import,
        'sync_with_webhook': mock_bamboo_hr_importer.sync_with_webhook,
        'webhook_payload': webhook_payload
    }


def mock_test_send_employee_email_missing_failure_notification(mocker):
    """
    Mock setup for test_send_employee_email_missing_failure_notification
    Mocks BambooHrEmployeeImport
    """
    mock_bamboo_hr_importer = mocker.MagicMock()
    mock_bamboo_hr_employee_import = mocker.patch(
        'apps.bamboohr.tasks.BambooHrEmployeeImport',
        return_value=mock_bamboo_hr_importer
    )
    
    return {
        'bamboo_hr_employee_import': mock_bamboo_hr_employee_import,
        'send_employee_email_missing_failure_notification': mock_bamboo_hr_importer.send_employee_email_missing_failure_notification
    }


def mock_test_webhook_callback_view(mocker):
    """
    Mock setup for test_webhook_callback_view
    Mocks async_task
    """
    mock_async_task = mocker.patch('apps.bamboohr.views.async_task')
    
    return {
        'async_task': mock_async_task,
        'webhook_payload': webhook_payload
    }


def mock_test_sync_employees_view(mocker):
    """
    Mock setup for test_sync_employees_view
    Mocks async_task
    """
    mock_async_task = mocker.patch('apps.bamboohr.views.async_task')
    
    return {
        'async_task': mock_async_task,
        'sync_employees_request_data': sync_employees_request_data
    } 
