"""
Mock setup functions for fyle_employee_imports tests
"""

from .fixtures import (
    dummy_org_id,
    dummy_refresh_token,
    cluster_domain,
    expense_attribute_data,
    employee_data,
    employee_data_no_email,
    bamboohr_employees_response,
    existing_departments_response,
    department_generator_response,
    new_departments,
    department_payload,
    employee_payload,
    employee_approver_payload,
    incomplete_employees,
    bamboohr_config_data,
    admin_emails,
    webhook_payload,
    webhook_payload_no_email,
    supervisor_employee_data,
    fyle_employee_response,
    sync_employee_from_date,
    destination_attributes,
    employee_exported_at,
    email_notification_employees,
    expense_attributes,
    department_creation_payload,
    bamboohr_data,
    bamboohr_configuration_data,
    fyle_credential_data,
    department_query_params,
    employee_list_query_params,
    bamboohr_sdk_employees_response,
    incremental_sync_params,
    non_incremental_sync_params,
    org_created_at,
    mock_employees_for_departments,
    expected_departments_set,
    mock_employees_for_import,
    expected_department_payload,
    expected_disabled_department_payload,
    mock_employees_for_payload,
    expected_employee_payload_result,
    expected_approver_payload_result,
    mock_employees_for_import_process,
    inactive_employee_response,
    webhook_payload_no_supervisor,
    webhook_payload_with_dept,
    employee_missing_display_name,
    expected_destination_attributes_data,
    expected_inactive_employee_data
)

import json

def mock_test_get_employee_and_approver_payload(mocker):
    """
    Mock setup for get_employee_and_approver_payload method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    # Create mock employees with proper .detail attribute
    mock_employees = []
    for emp_data in mock_employees_for_payload:
        mock_emp = mocker.MagicMock()
        mock_emp.detail = emp_data['detail']
        mock_emp.destination_id = emp_data['destination_id']
        mock_emp.active = emp_data['active']
        mock_employees.append(mock_emp)
    
    return {
        'platform_connector': mock_platform_connector,
        'mock_employees': mock_employees,
        'expected_employee_payload': expected_employee_payload_result,
        'expected_approver_payload': expected_approver_payload_result
    }


def mock_test___init__(mocker):
    """
    Mock setup for __init__ method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'platform_connector': mock_platform_connector
    }


def mock_test_sync_fyle_employees(mocker):
    """
    Mock setup for sync_fyle_employees method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector.sync_employees.return_value = None
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'platform_connector': mock_platform_connector,
        'sync_employees': mock_platform_connector.sync_employees
    }


def mock_test_get_existing_departments_from_fyle(mocker):
    """
    Mock setup for get_existing_departments_from_fyle method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector.get_department_generator.return_value = [{'data': department_generator_response}]
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'platform_connector': mock_platform_connector,
        'get_department_generator': mock_platform_connector.get_department_generator
    }


def mock_test_create_fyle_department_payload(mocker):
    """
    Mock setup for create_fyle_department_payload method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'platform_connector': mock_platform_connector,
        'expected_payload': expected_department_payload
    }


def mock_test_create_fyle_department_payload_with_disabled_department(mocker):
    """
    Mock setup for create_fyle_department_payload with disabled department method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'platform_connector': mock_platform_connector,
        'expected_disabled_payload': expected_disabled_department_payload
    }


def mock_test_departments_to_be_imported(mocker):
    """
    Mock setup for departments_to_be_imported method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    # Create mock employees with proper .detail attribute
    mock_employees = []
    for emp_data in mock_employees_for_departments:
        mock_emp = mocker.MagicMock()
        mock_emp.detail = emp_data['detail']
        mock_employees.append(mock_emp)
    
    return {
        'platform_connector': mock_platform_connector,
        'mock_employees': mock_employees,
        'expected_departments_set': expected_departments_set
    }


def mock_test_post_department(mocker):
    """
    Mock setup for post_department method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector.post_department = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'platform_connector': mock_platform_connector,
        'post_department': mock_platform_connector.post_department
    }


def mock_test_import_departments(mocker):
    """
    Mock setup for import_departments method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector.get_department_generator.return_value = [{'data': department_generator_response}]
    mock_platform_connector.post_department = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    # Create mock employees with proper .detail attribute
    mock_employees = []
    for emp_data in mock_employees_for_import:
        mock_emp = mocker.MagicMock()
        mock_emp.detail = emp_data['detail']
        mock_employees.append(mock_emp)
    
    return {
        'platform_connector': mock_platform_connector,
        'mock_employees': mock_employees,
        'get_department_generator': mock_platform_connector.get_department_generator,
        'post_department': mock_platform_connector.post_department
    }


def mock_test_fyle_employee_import(mocker):
    """
    Mock setup for fyle_employee_import method
    """
    shared_mocks = mock_bamboohr_shared_mock(mocker)
    
    # Create mock employees with proper .detail attribute
    mock_employees = []
    for emp_data in mock_employees_for_import_process:
        mock_emp = mocker.MagicMock()
        mock_emp.detail = emp_data['detail']
        mock_employees.append(mock_emp)
    
    shared_mocks.update({
        'mock_employees': mock_employees
    })
    
    return shared_mocks


def mock_test_sync_employees(mocker):
    """
    Mock setup for sync_employees method
    """
    shared_mocks = mock_bamboohr_shared_mock(mocker)
    
    # Create mock employees with proper .detail attribute
    mock_employees = []
    for emp_data in mock_employees_for_import:
        mock_emp = mocker.MagicMock()
        mock_emp.detail = emp_data['detail']
        mock_employees.append(mock_emp)
    
    shared_mocks.update({
        'mock_employees': mock_employees,
        'expected_department_payload': expected_department_payload
    })
    
    return shared_mocks


def mock_test_send_employee_email_missing_failure_notification_database_operations(mocker):
    """
    Mock setup for send_employee_email_missing_failure_notification database operations
    """
    mock_sendgrid_client = mocker.patch('sendgrid.SendGridAPIClient')
    mock_send_failure_notification = mocker.patch('apps.bamboohr.email.send_failure_notification_email')
    
    return {
        'sendgrid_client': mock_sendgrid_client,
        'send_failure_notification': mock_send_failure_notification
    }


def mock_test_get_departments(mocker):
    """
    Mock setup for get_departments method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'platform_connector': mock_platform_connector,
        'mock_employees': mock_employees_for_departments,
        'expected_departments': expected_departments_set
    }


def mock_test_import_employees(mocker):
    """
    Mock setup for import_employees method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'platform_connector': mock_platform_connector,
        'mock_employees': mock_employees_for_import,
        'expected_department_payload': expected_department_payload,
        'expected_disabled_department_payload': expected_disabled_department_payload
    }


def mock_test_import_employees_process(mocker):
    """
    Mock setup for import_employees_process method
    """
    shared_mocks = mock_bamboohr_shared_mock(mocker)
    
    mock_employees = []
    for emp_data in mock_employees_for_import_process:
        mock_emp = mocker.MagicMock()
        mock_emp.detail = emp_data['detail']
        mock_employees.append(mock_emp)
    
    shared_mocks.update({
        'mock_employees': mock_employees
    })
    
    return shared_mocks


def mock_bamboohr_shared_mock(mocker):
    """
    Shared mock setup for BambooHR tests
    Returns a dictionary of mocks that can be used with mock_dependencies
    """
    # Mock the BambooHR SDK completely to prevent HTTP calls
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.employees.get_all.return_value = bamboohr_employees_response
    mock_bamboohr_sdk.employees.get.return_value = supervisor_employee_data
    # Mock both import paths for BambooHR SDK
    mock_bamboohr_sdk_class = mocker.patch('bamboosdk.bamboohrsdk.BambooHrSDK', return_value=mock_bamboohr_sdk)
    mock_bamboohr_sdk_class2 = mocker.patch('fyle_employee_imports.bamboo_hr.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    # Mock the underlying BambooHR API calls to prevent actual HTTP requests
    mock_bamboohr_api_response = mocker.MagicMock()
    mock_bamboohr_api_response.status_code = 200
    mock_bamboohr_api_response.json.return_value = bamboohr_employees_response
    mock_bamboohr_api_response.text = json.dumps(bamboohr_employees_response)
    mock_bamboohr_requests_post = mocker.patch('bamboosdk.api.api_base.requests.post', return_value=mock_bamboohr_api_response)
    mock_bamboohr_requests_get = mocker.patch('bamboosdk.api.api_base.requests.get', return_value=mock_bamboohr_api_response)
    
    # Mock SendGrid to prevent email sending
    mock_sendgrid_client = mocker.patch('sendgrid.SendGridAPIClient')
    mock_sendgrid_client.return_value.send.return_value = None

    # Mock requests library to prevent all HTTP calls
    mock_requests_response = mocker.MagicMock()
    mock_requests_response.status_code = 200
    mock_requests_response.json.return_value = {
        'data': fyle_employee_response,
        'count': len(fyle_employee_response) if fyle_employee_response else 0,
        'offset': 0,
        'limit': 1000
    }
    mock_requests_response.text = '{"data": [], "count": 0, "offset": 0, "limit": 1000}'
    mock_requests_request = mocker.patch('requests.request', return_value=mock_requests_response)

    # Mock the Platform class directly to prevent HTTP calls
    mock_platform = mocker.MagicMock()
    mock_platform.v1.admin.employees.list.return_value = {'data': fyle_employee_response}
    mock_platform.v1.admin.employees.invite_bulk.return_value = None
    mock_platform.v1.admin.departments.list_all.return_value = [{'data': department_generator_response}]
    mock_platform.v1.admin.departments.post.return_value = None
    mock_platform_class = mocker.patch('fyle.platform.Platform', return_value=mock_platform)

    # Create a mock platform connector with all necessary methods
    mock_platform_connector = mocker.MagicMock()
    
    # Mock the connection object to prevent real HTTP calls
    mock_connection = mocker.MagicMock()
    mock_connection.v1.admin.employees.list.return_value = {'data': fyle_employee_response}
    mock_connection.v1.admin.employees.invite_bulk.return_value = None
    mock_connection.v1.admin.departments.list_all.return_value = [{'data': department_generator_response}]
    mock_connection.v1.admin.departments.post.return_value = None
    mock_platform_connector.connection = mock_connection
    
    # Mock only the methods that should be called directly
    mock_platform_connector.get_employee_by_email.return_value = fyle_employee_response
    mock_platform_connector.get_department_generator.return_value = [{'data': department_generator_response}]
    mock_platform_connector.post_department.return_value = None
    mock_platform_connector.bulk_post_employees.return_value = None
    mock_platform_connector.sync_employees.return_value = None
    
    # Simplest approach: Mock the PlatformConnector constructor to return our mock
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    # Also mock the database queries that BambooHrEmployeeImport.__init__ makes
    mock_bamboohr_queryset = mocker.MagicMock()
    mock_bamboohr_model = mocker.MagicMock()
    mock_bamboohr_model.api_token = 'test_token'
    mock_bamboohr_model.sub_domain = 'test_domain'
    mock_bamboohr_model.employee_exported_at = employee_exported_at
    mock_bamboohr_queryset.first.return_value = mock_bamboohr_model
    mocker.patch('fyle_employee_imports.bamboo_hr.BambooHr.objects.filter', return_value=mock_bamboohr_queryset)
    
    mock_bamboohr_config = mocker.MagicMock()
    mock_bamboohr_config.emails_selected = bamboohr_config_data['emails_selected']
    mocker.patch('fyle_employee_imports.bamboo_hr.BambooHrConfiguration.objects.get', return_value=mock_bamboohr_config)

    mock_email_notification = mocker.patch('apps.bamboohr.email.send_failure_notification_email')
    mock_email_notification.return_value = None
    
    # Also mock the send_failure_notification_email function directly
    mock_send_failure_notification_email = mocker.patch('fyle_employee_imports.bamboo_hr.send_failure_notification_email')
    mock_send_failure_notification_email.return_value = None

    # Mock get_existing_departments_from_fyle method on the FyleEmployeeImport class
    mock_get_existing_departments_from_fyle = mocker.patch(
        'fyle_employee_imports.base.FyleEmployeeImport.get_existing_departments_from_fyle',
        return_value=existing_departments_response
    )

    return {
        'bamboohr_sdk': mock_bamboohr_sdk,
        'platform_connector': mock_platform_connector,
        'email_notification': mock_email_notification,
        'send_failure_notification_email': mock_send_failure_notification_email,
        'get_employee_by_email': mock_platform_connector.get_employee_by_email,
        'get_existing_departments_from_fyle': mock_get_existing_departments_from_fyle,
        'get_department_generator': mock_platform_connector.get_department_generator,
        'post_department': mock_platform_connector.post_department,
        'bulk_post_employees': mock_platform_connector.bulk_post_employees,
        'sync_employees': mock_platform_connector.sync_employees,
        'employees_get': mock_bamboohr_sdk.employees.get,
        'employees_get_all': mock_bamboohr_sdk.employees.get_all,
        'expected_departments_set': expected_departments_set,
        'mock_employees': mock_employees_for_departments
    }


def mock_test_sync_hrms_employees(mocker):
    """
    Mock setup for sync_hrms_employees method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.employees.get_all.return_value = bamboohr_employees_response
    mock_bamboohr_sdk_class = mocker.patch('fyle_employee_imports.bamboo_hr.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    mock_fyle_employee_import = mocker.patch('fyle_employee_imports.bamboo_hr.FyleEmployeeImport')
    mock_fyle_employee_import.return_value.import_employees.return_value = None
    
    return {
        'platform_connector': mock_platform_connector,
        'bamboohr_sdk': mock_bamboohr_sdk,
        'fyle_employee_import': mock_fyle_employee_import
    }


def mock_test_sync_with_webhook(mocker):
    """
    Mock setup for sync_with_webhook method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.employees.get.return_value = supervisor_employee_data
    mock_bamboohr_sdk_class = mocker.patch('fyle_employee_imports.bamboo_hr.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    return {
        'platform_connector': mock_platform_connector,
        'bamboohr_sdk': mock_bamboohr_sdk,
        'webhook_payload': webhook_payload
    }


def mock_test_sync_with_webhook_without_email(mocker):
    """
    Mock setup for sync_with_webhook without email test
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.employees.get.return_value = supervisor_employee_data
    mock_bamboohr_sdk_class = mocker.patch('fyle_employee_imports.bamboo_hr.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    return {
        'platform_connector': mock_platform_connector,
        'bamboohr_sdk': mock_bamboohr_sdk,
        'webhook_payload': webhook_payload_no_email
    }


def mock_test_sync_with_webhook_without_supervisor(mocker):
    """
    Mock setup for sync_with_webhook without supervisor test
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.employees.get.return_value = None
    mock_bamboohr_sdk_class = mocker.patch('fyle_employee_imports.bamboo_hr.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    return {
        'platform_connector': mock_platform_connector,
        'bamboohr_sdk': mock_bamboohr_sdk,
        'webhook_payload': webhook_payload
    }


def mock_test_sync_with_webhook_with_department(mocker):
    """
    Mock setup for sync_with_webhook with department test
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.employees.get.return_value = supervisor_employee_data
    mock_bamboohr_sdk_class = mocker.patch('fyle_employee_imports.bamboo_hr.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    return {
        'platform_connector': mock_platform_connector,
        'bamboohr_sdk': mock_bamboohr_sdk,
        'webhook_payload': webhook_payload
    }


def mock_test_sync_with_webhook_supervisor_without_fyle_employee(mocker):
    """
    Mock setup for sync_with_webhook supervisor without fyle employee test
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector.connection.v1.admin.employees.list.return_value = {'data': []}
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.employees.get.return_value = supervisor_employee_data
    mock_bamboohr_sdk_class = mocker.patch('fyle_employee_imports.bamboo_hr.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    return {
        'platform_connector': mock_platform_connector,
        'bamboohr_sdk': mock_bamboohr_sdk,
        'webhook_payload': webhook_payload
    }


def mock_test_upsert_employees(mocker):
    """
    Mock setup for upsert_employees test
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'platform_connector': mock_platform_connector
    }


def mock_test_upsert_employees_with_missing_display_name(mocker):
    """
    Mock setup for upsert_employees with missing display name test
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'platform_connector': mock_platform_connector,
        'mock_employees': employee_missing_display_name,
        'expected_result': expected_inactive_employee_data
    }


def mock_test_upsert_employees_with_inactive_status(mocker):
    """
    Mock setup for upsert_employees with inactive status test
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'platform_connector': mock_platform_connector,
        'mock_employees': inactive_employee_response,
        'expected_result': expected_inactive_employee_data
    }


def mock_test_get_admin_email(mocker):
    """
    Mock setup for get_admin_email test
    """
    mock_bamboohr_configuration = mocker.MagicMock()
    mock_bamboohr_configuration.return_value = bamboohr_configuration_data
    mock_bamboohr_configuration_class = mocker.patch('fyle_employee_imports.bamboo_hr.BambooHrConfiguration', return_value=mock_bamboohr_configuration)
    
    return {
        'bamboohr_configuration': mock_bamboohr_configuration,
        'expected_admin_emails': admin_emails
    }


def mock_test_get_employee_exported_at(mocker):
    """
    Mock setup for get_employee_exported_at test
    """
    mock_bamboohr_get = mocker.patch('fyle_employee_imports.bamboo_hr.BambooHr.objects.get')
    mock_bamboohr_get.return_value.employee_exported_at = employee_exported_at
    
    return {
        'bamboohr_get': mock_bamboohr_get,
        'expected_exported_at': employee_exported_at
    }


def mock_test_bamboohr_employee_import_init(mocker):
    """
    Mock setup for BambooHrEmployeeImport initialization
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'platform_connector': mock_platform_connector
    }


def mock_test_sync_hrms_employees_with_incremental_sync(mocker):
    """
    Mock setup for sync_hrms_employees with incremental sync test
    """
    shared_mocks = mock_bamboohr_shared_mock(mocker)
    
    return shared_mocks


def mock_test_sync_hrms_employees_without_incremental_sync(mocker):
    """
    Mock setup for sync_hrms_employees without incremental sync test
    """
    shared_mocks = mock_bamboohr_shared_mock(mocker)
    
    return shared_mocks


def mock_test_sync_with_webhook_with_supervisor(mocker):
    """
    Mock setup for sync_with_webhook with supervisor test
    """
    shared_mocks = mock_bamboohr_shared_mock(mocker)
    
    return shared_mocks
