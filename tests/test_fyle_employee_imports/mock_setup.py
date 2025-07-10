"""
Mock setup functions for fyle_employee_imports tests
"""

from .fixtures import (
    dummy_org_id,
    dummy_refresh_token,
    cluster_domain,
    department_generator_response,
    department_payload,
    destination_attributes,
    employee_exported_at,
    email_notification_employees,
    expense_attributes,
    bamboohr_employees_response,
    admin_emails,
    webhook_payload,
    webhook_payload_no_email,
    supervisor_employee_data,
    fyle_employee_response,
    sync_employee_from_date,
    bamboohr_sdk_employees_response,
    bamboohr_configuration_data,
    org_created_at,
    mock_employees_for_departments,
    expected_departments_set,
    mock_employees_for_import,
    expected_department_payload,
    expected_disabled_department_payload,
    mock_employees_for_payload,
    expected_employee_payload_result,
    expected_approver_payload_result,
    mock_employees_for_import_process
)


def mock_test___init__(mocker):
    """
    Mock setup for __init__ method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'platform_connector': mock_platform_connector,
        'platform_connector_class': mock_platform_connector_class
    }


def mock_test_sync_fyle_employees(mocker):
    """
    Mock setup for sync_fyle_employees method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector.sync_employees = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
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
        'get_department_generator': mock_platform_connector.get_department_generator
    }


def mock_test_create_fyle_department_payload(mocker):
    """
    Mock setup for create_fyle_department_payload method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'expected_payload': expected_department_payload,
        'expected_disabled_payload': expected_disabled_department_payload
    }


def mock_test_create_fyle_department_payload_with_disabled_department(mocker):
    """
    Mock setup for create_fyle_department_payload method with disabled department
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'expected_disabled_payload': expected_disabled_department_payload
    }


def mock_test_abstract_methods_raise_not_implemented_error(mocker):
    """
    Mock setup for abstract_methods_raise_not_implemented_error method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'platform_connector': mock_platform_connector,
        'platform_connector_class': mock_platform_connector_class
    }


def mock_test_departments_to_be_imported(mocker):
    """
    Mock setup for departments_to_be_imported method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    # Create mock employees using fixture data
    mock_employees = []
    for emp_data in mock_employees_for_departments:
        mock_emp = mocker.MagicMock()
        mock_emp.detail = emp_data['detail']
        mock_employees.append(mock_emp)
    
    return {
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
    
    # Create mock employees using fixture data
    mock_employees = []
    for emp_data in mock_employees_for_import:
        mock_emp = mocker.MagicMock()
        mock_emp.detail = emp_data['detail']
        mock_employees.append(mock_emp)
    
    return {
        'mock_employees': mock_employees,
        'get_department_generator': mock_platform_connector.get_department_generator,
        'post_department': mock_platform_connector.post_department
    }


def mock_test_get_employee_and_approver_payload(mocker):
    """
    Mock setup for get_employee_and_approver_payload method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    # Create mock employees using fixture data - use real destination_id and active values
    mock_employees = []
    for emp_data in mock_employees_for_payload:
        mock_emp = mocker.MagicMock()
        mock_emp.detail = emp_data['detail']
        mock_emp.destination_id = emp_data['destination_id']
        mock_emp.active = emp_data['active']
        mock_employees.append(mock_emp)
    
    return {
        'mock_employees': mock_employees,
        'expected_employee_payload': expected_employee_payload_result,
        'expected_approver_payload': expected_approver_payload_result
    }


def mock_test_fyle_employee_import(mocker):
    """
    Mock setup for fyle_employee_import method
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


def mock_test_sync_employees(mocker):
    """
    Mock setup for sync_employees method
    """
    
    return mock_bamboohr_shared_mock(mocker)


def mock_test_send_employee_email_missing_failure_notification(mocker):
    """
    Mock setup for send_employee_email_missing_failure_notification method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'email_notification_employees': email_notification_employees
    }


def mock_bamboohr_employee_import_init(mocker):
    """
    Mock setup for BambooHrEmployeeImport initialization
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'platform_connector': mock_platform_connector,
        'platform_connector_class': mock_platform_connector_class
    }


def mock_bamboohr_shared_mock(mocker):
    """
    Shared mock setup for BambooHR employee import tests
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector.get_department_generator.return_value = [{'data': department_generator_response}]
    mock_platform_connector.post_department = mocker.MagicMock()
    mock_platform_connector.bulk_post_employees = mocker.MagicMock()
    mock_platform_connector.get_employee_by_email.return_value = fyle_employee_response
    mock_platform_connector.sync_employees = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.employees.get_all.return_value = bamboohr_sdk_employees_response
    mock_bamboohr_sdk.employees.get.return_value = supervisor_employee_data
    mock_bamboohr_sdk_class = mocker.patch('fyle_employee_imports.bamboo_hr.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    mock_bulk_create_or_update = mocker.patch('apps.fyle_hrms_mappings.models.DestinationAttribute.bulk_create_or_update_destination_attributes')
    
    mock_send_notification_email = mocker.patch('fyle_employee_imports.bamboo_hr.send_failure_notification_email')
    
    mock_sendgrid_client = mocker.MagicMock()
    mock_sendgrid_api = mocker.patch('apps.bamboohr.email.sendgrid.SendGridAPIClient', return_value=mock_sendgrid_client)
    
    return {
        'platform_connector': mock_platform_connector,
        'platform_connector_class': mock_platform_connector_class,
        'bamboohr_sdk': mock_bamboohr_sdk,
        'bamboohr_sdk_class': mock_bamboohr_sdk_class,
        'get_existing_departments_from_fyle': mocker.MagicMock(),
        'get_employee_by_email': mock_platform_connector.get_employee_by_email,
        'bulk_create_or_update_destination_attributes': mock_bulk_create_or_update,
        'sync_employees': mock_platform_connector.sync_employees,
        'get_department_generator': mock_platform_connector.get_department_generator,
        'post_department': mock_platform_connector.post_department,
        'bulk_post_employees': mock_platform_connector.bulk_post_employees,
        'send_failure_notification_email': mock_send_notification_email,
        'employees_get_all': mock_bamboohr_sdk.employees.get_all,
        'employees_get': mock_bamboohr_sdk.employees.get,
        'sendgrid_client': mock_sendgrid_client,
        'sendgrid_api': mock_sendgrid_api
    }


def mock_test_save_employee_exported_at_time(mocker):
    """
    Mock setup for save_employee_exported_at_time method
    """
    return {
        'employee_exported_at': employee_exported_at
    }


def mock_test_upsert_employees_database_operations(mocker):
    """
    Mock setup for upsert_employees database operations
    """
    return {
        'bamboohr_employees_response': bamboohr_employees_response
    }


def mock_test_upsert_employees_inactive_status_database_operations(mocker):
    """
    Mock setup for upsert_employees inactive status database operations
    """
    return {
        'bamboohr_employees_response': bamboohr_employees_response
    }


def mock_test_send_employee_email_missing_failure_notification_database_operations(mocker):
    """
    Mock setup for send_employee_email_missing_failure_notification database operations
    """
    
    shared_mocks = mock_bamboohr_shared_mock(mocker)
    
    shared_mocks.update({
        'admin_emails': admin_emails
    })
    
    return shared_mocks


def mock_test_sync_with_webhook_without_email(mocker):
    """
    Mock setup for sync_with_webhook without email test
    """
    return {}


def mock_test_sync_with_webhook_without_supervisor(mocker):
    """
    Mock setup for sync_with_webhook without supervisor test
    """
    return {}


def mock_test_sync_with_webhook_with_department(mocker):
    """
    Mock setup for sync_with_webhook with department test
    """
    return {}


def mock_test_sync_with_webhook_supervisor_without_fyle_employee(mocker):
    """
    Mock setup for sync_with_webhook supervisor without fyle employee test
    """
    return {}


def mock_test_upsert_employees_with_missing_display_name(mocker):
    """
    Mock setup for upsert_employees with missing display name test
    """
    return {}


def mock_test_upsert_employees_with_inactive_status(mocker):
    """
    Mock setup for upsert_employees with inactive status test
    """
    return {}


def mock_test_get_admin_email(mocker):
    """
    Mock setup for get_admin_email test
    """
    return {}


def mock_test_get_employee_exported_at(mocker):
    """
    Mock setup for get_employee_exported_at test
    """
    return {}


def mock_test_sync_hrms_employees_with_incremental_sync(mocker):
    """
    Mock setup for sync_hrms_employees with incremental sync test
    """
    return {}


def mock_test_sync_hrms_employees_without_incremental_sync(mocker):
    """
    Mock setup for sync_hrms_employees without incremental sync test
    """
    return {}


def mock_test_sync_with_webhook_with_supervisor(mocker):
    """
    Mock setup for sync_with_webhook with supervisor test
    """
    return {}


def mock_test_upsert_employees(mocker):
    """
    Mock setup for upsert_employees test
    """
    return {}
