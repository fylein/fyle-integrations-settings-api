"""
Mock setup functions for fyle_employee_imports tests
"""

from .fixtures import (
    dummy_org_id,
    dummy_refresh_token,
    cluster_domain,
    department_generator_response,
    existing_departments_response,
    new_departments,
    department_payload,
    employee_payload,
    employee_approver_payload,
    destination_attributes,
    employee_exported_at,
    email_notification_employees,
    expense_attributes,
    employee_data,
    bamboohr_employees_response,
    admin_emails,
    webhook_payload,
    webhook_payload_no_email,
    supervisor_employee_data,
    fyle_employee_response,
    sync_employee_from_date,
    bamboohr_sdk_employees_response,
    bamboohr_configuration_data,
    bamboohr_data,
    org_created_at
)


def mock_fyle_employee_import_init(mocker):
    """
    Mock setup for FyleEmployeeImport __init__ method
    """
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = cluster_domain
    mock_org_get = mocker.patch('fyle_employee_imports.base.Org.objects.get', return_value=mock_org)
    
    mock_credential = mocker.MagicMock()
    mock_credential.refresh_token = dummy_refresh_token
    mock_credential_get = mocker.patch('fyle_employee_imports.base.FyleCredential.objects.get', return_value=mock_credential)
    
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'org_get': mock_org_get,
        'credential_get': mock_credential_get,
        'platform_connector_class': mock_platform_connector_class,
        'platform_connector': mock_platform_connector,
        'org': mock_org,
        'credential': mock_credential
    }


def mock_sync_fyle_employees(mocker):
    """
    Mock setup for sync_fyle_employees method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'platform_connector': mock_platform_connector,
        'sync_employees': mock_platform_connector.sync_employees
    }


def mock_get_existing_departments_from_fyle(mocker):
    """
    Mock setup for get_existing_departments_from_fyle method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector.get_department_generator.return_value = department_generator_response
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'platform_connector': mock_platform_connector,
        'get_department_generator': mock_platform_connector.get_department_generator,
        'department_generator_response': department_generator_response
    }


def mock_create_fyle_department_payload(mocker):
    """
    Mock setup for create_fyle_department_payload method
    """
    return {
        'existing_departments': existing_departments_response,
        'new_departments': new_departments,
        'expected_payload': department_payload
    }


def mock_post_department(mocker):
    """
    Mock setup for post_department method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'platform_connector': mock_platform_connector,
        'post_department': mock_platform_connector.post_department
    }


def mock_get_employee_and_approver_payload(mocker):
    """
    Mock setup for get_employee_and_approver_payload method
    """
    mock_expense_attribute = mocker.MagicMock()
    mock_expense_attribute.objects.filter.return_value.values_list.return_value = expense_attributes
    mock_expense_attribute_patch = mocker.patch('fyle_employee_imports.base.ExpenseAttribute', mock_expense_attribute)
    
    return {
        'expense_attribute': mock_expense_attribute,
        'expense_attribute_filter': mock_expense_attribute.objects.filter,
        'expense_attributes': expense_attributes
    }


def mock_fyle_employee_import_process(mocker):
    """
    Mock setup for fyle_employee_import method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'platform_connector': mock_platform_connector,
        'bulk_post_employees': mock_platform_connector.bulk_post_employees,
        'sync_employees': mock_platform_connector.sync_employees
    }


def mock_sync_employees(mocker):
    """
    Mock setup for sync_employees method
    """
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    mock_destination_attribute = mocker.MagicMock()
    mock_destination_attribute.objects.filter.return_value.order_by.return_value = destination_attributes
    mock_destination_attribute_patch = mocker.patch('fyle_employee_imports.base.DestinationAttribute', mock_destination_attribute)
    
    return {
        'platform_connector': mock_platform_connector,
        'sync_employees': mock_platform_connector.sync_employees,
        'destination_attribute': mock_destination_attribute,
        'destination_attribute_filter': mock_destination_attribute.objects.filter
    }


def mock_send_employee_email_missing_failure_notification(mocker):
    """
    Mock setup for send_employee_email_missing_failure_notification method
    """
    mock_destination_attribute = mocker.MagicMock()
    mock_queryset = mocker.MagicMock()
    mock_queryset.values.return_value.order_by.return_value = email_notification_employees
    mock_queryset.update.return_value = None
    mock_destination_attribute.objects.filter.return_value = mock_queryset
    mock_destination_attribute_patch = mocker.patch('fyle_employee_imports.base.DestinationAttribute', mock_destination_attribute)
    
    mock_send_email = mocker.patch('fyle_employee_imports.base.send_failure_notification_email')
    
    return {
        'destination_attribute': mock_destination_attribute,
        'destination_attribute_filter': mock_destination_attribute.objects.filter,
        'send_failure_notification_email': mock_send_email,
        'queryset': mock_queryset,
        'update': mock_queryset.update
    }


def mock_bamboohr_employee_import_init(mocker):
    """
    Mock setup for BambooHR employee import initialization
    """
    # Mock Org model
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = cluster_domain
    mock_org.created_at = org_created_at
    mock_org_get = mocker.patch('apps.orgs.models.Org.objects.get', return_value=mock_org)
    
    # Mock FyleCredential model
    mock_credential = mocker.MagicMock()
    mock_credential.refresh_token = dummy_refresh_token
    mock_credential_get = mocker.patch('apps.orgs.models.FyleCredential.objects.get', return_value=mock_credential)
    
    # Mock BambooHr model
    mock_bamboohr = mocker.MagicMock()
    mock_bamboohr.api_token = 'test_token'
    mock_bamboohr.sub_domain = 'test_domain'
    mock_bamboohr.employee_exported_at = employee_exported_at
    mock_bamboohr_queryset = mocker.MagicMock()
    mock_bamboohr_queryset.first.return_value = mock_bamboohr
    mock_bamboohr_objects = mocker.patch('apps.bamboohr.models.BambooHr.objects')
    mock_bamboohr_objects.filter.return_value = mock_bamboohr_queryset
    
    # Mock BambooHrConfiguration model
    mock_bamboohr_config = mocker.MagicMock()
    mock_bamboohr_config.emails_selected = bamboohr_configuration_data['emails_selected']
    mock_bamboohr_config_get = mocker.patch('apps.bamboohr.models.BambooHrConfiguration.objects.get', return_value=mock_bamboohr_config)
    
    # Mock BambooHrSDK - properly mock the instance methods
    mock_employees = mocker.MagicMock()
    mock_employees.get_all.return_value = bamboohr_sdk_employees_response
    mock_employees.get.return_value = supervisor_employee_data
    
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.employees = mock_employees
    mock_bamboohr_sdk_class = mocker.patch('fyle_employee_imports.bamboo_hr.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    # Mock PlatformConnector
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'org': mock_org,
        'org_get': mock_org_get,
        'credential': mock_credential,
        'credential_get': mock_credential_get,
        'bamboohr': mock_bamboohr,
        'bamboohr_objects': mock_bamboohr_objects,
        'bamboohr_queryset': mock_bamboohr_queryset,
        'bamboohr_config': mock_bamboohr_config,
        'bamboohr_config_get': mock_bamboohr_config_get,
        'bamboohr_sdk': mock_bamboohr_sdk,
        'bamboohr_sdk_class': mock_bamboohr_sdk_class,
        'employees': mock_employees,
        'platform_connector': mock_platform_connector,
        'platform_connector_class': mock_platform_connector_class
    }


def mock_get_admin_email(mocker):
    """
    Mock setup for get_admin_email method
    """
    return {
        'admin_emails': admin_emails
    }


def mock_sync_hrms_employees(mocker):
    """
    Mock setup for sync_hrms_employees method
    """
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_employees = mocker.MagicMock()
    mock_employees.get_all.return_value = bamboohr_sdk_employees_response
    mock_bamboohr_sdk.employees = mock_employees
    
    return {
        'bamboohr_sdk': mock_bamboohr_sdk,
        'employees': mock_employees
    }


def mock_sync_with_webhook(mocker):
    """
    Mock setup for sync_with_webhook method
    """
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_employees = mocker.MagicMock()
    mock_employees.get.return_value = supervisor_employee_data
    mock_bamboohr_sdk.employees = mock_employees
    
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector.get_employee_by_email.return_value = fyle_employee_response
    mock_platform_connector.get_existing_departments_from_fyle.return_value = existing_departments_response
    mock_platform_connector.create_fyle_department_payload.return_value = department_payload
    
    mock_send_failure_notification_email = mocker.patch('apps.bamboohr.email.send_failure_notification_email')
    
    return {
        'bamboohr_sdk': mock_bamboohr_sdk,
        'employees': mock_employees,
        'platform_connector': mock_platform_connector,
        'send_failure_notification_email': mock_send_failure_notification_email
    }


def mock_upsert_employees(mocker):
    """
    Mock setup for upsert_employees method
    """
    mock_destination_attribute = mocker.patch('apps.fyle_hrms_mappings.models.DestinationAttribute')
    mock_destination_attribute.bulk_create_or_update_destination_attributes.return_value = None
    
    return {
        'destination_attribute': mock_destination_attribute
    }


def mock_save_employee_exported_at_time(mocker):
    """
    Mock setup for save_employee_exported_at_time method
    """
    mock_bamboohr_queryset = mocker.MagicMock()
    mock_bamboohr_queryset.update.return_value = None
    
    return {
        'bamboohr_queryset': mock_bamboohr_queryset,
        'update': mock_bamboohr_queryset.update
    }


# Shared mock functions for integration tests
def mock_base_shared_mock(mocker):
    """
    Shared mock setup for FyleEmployeeImport base class
    """
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = cluster_domain
    mock_org_get = mocker.patch('fyle_employee_imports.base.Org.objects.get', return_value=mock_org)
    
    mock_credential = mocker.MagicMock()
    mock_credential.refresh_token = dummy_refresh_token
    mock_credential_get = mocker.patch('fyle_employee_imports.base.FyleCredential.objects.get', return_value=mock_credential)
    
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector.get_department_generator.return_value = department_generator_response
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    mock_destination_attribute = mocker.MagicMock()
    mock_destination_attribute.objects.filter.return_value.order_by.return_value = destination_attributes
    mock_destination_attribute_patch = mocker.patch('fyle_employee_imports.base.DestinationAttribute', mock_destination_attribute)
    
    mock_expense_attribute = mocker.MagicMock()
    mock_expense_attribute.objects.filter.return_value.values_list.return_value = expense_attributes
    mock_expense_attribute_patch = mocker.patch('fyle_employee_imports.base.ExpenseAttribute', mock_expense_attribute)
    
    return {
        'org_get': mock_org_get,
        'credential_get': mock_credential_get,
        'platform_connector_class': mock_platform_connector_class,
        'platform_connector': mock_platform_connector,
        'destination_attribute': mock_destination_attribute,
        'expense_attribute': mock_expense_attribute,
        'sync_employees': mock_platform_connector.sync_employees,
        'get_department_generator': mock_platform_connector.get_department_generator,
        'bulk_post_employees': mock_platform_connector.bulk_post_employees,
        'post_department': mock_platform_connector.post_department
    }


def mock_bamboohr_shared_mock(mocker):
    """
    Comprehensive mock setup for BambooHR employee import tests
    """
    # Mock Org model - patch at the import locations
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = cluster_domain
    mock_org.created_at = org_created_at
    mock_org_get = mocker.patch('fyle_employee_imports.base.Org.objects.get', return_value=mock_org)
    mock_org_get_bamboo = mocker.patch('fyle_employee_imports.bamboo_hr.Org.objects.get', return_value=mock_org)
    
    # Mock FyleCredential model - patch at the base import location
    mock_credential = mocker.MagicMock()
    mock_credential.refresh_token = dummy_refresh_token
    mock_credential_get = mocker.patch('fyle_employee_imports.base.FyleCredential.objects.get', return_value=mock_credential)
    
    # Mock BambooHr model
    mock_bamboohr = mocker.MagicMock()
    mock_bamboohr.api_token = 'test_token'
    mock_bamboohr.sub_domain = 'test_domain'
    mock_bamboohr.employee_exported_at = employee_exported_at
    mock_bamboohr_queryset = mocker.MagicMock()
    mock_bamboohr_queryset.first.return_value = mock_bamboohr
    mock_queryset_update = mocker.MagicMock()
    mock_bamboohr_queryset.update = mock_queryset_update
    mock_bamboohr_objects = mocker.patch('apps.bamboohr.models.BambooHr.objects')
    mock_bamboohr_objects.filter.return_value = mock_bamboohr_queryset
    
    # Mock BambooHrConfiguration model
    mock_bamboohr_config = mocker.MagicMock()
    mock_bamboohr_config.emails_selected = bamboohr_configuration_data['emails_selected']
    mock_bamboohr_config_get = mocker.patch('apps.bamboohr.models.BambooHrConfiguration.objects.get', return_value=mock_bamboohr_config)
    
    # Mock BambooHrSDK - Create a complete mock for the SDK at the import location
    mock_employees = mocker.MagicMock()
    mock_employees.get_all.return_value = bamboohr_sdk_employees_response
    mock_employees.get.return_value = supervisor_employee_data
    
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.employees = mock_employees
    # Patch the SDK at the location where it's imported in bamboo_hr.py
    mock_bamboohr_sdk_class = mocker.patch('fyle_employee_imports.bamboo_hr.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    # Mock PlatformConnector
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector.get_employee_by_email.return_value = fyle_employee_response
    mock_platform_connector.get_existing_departments_from_fyle.return_value = {'Engineering': {'id': 'dept_123', 'is_enabled': True}}
    mock_platform_connector.create_fyle_department_payload.return_value = department_payload
    mock_platform_connector.get_department_generator.return_value = [{'data': department_generator_response}]
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    # Mock DestinationAttribute - patch it at the import location
    mock_destination_attribute = mocker.patch('fyle_employee_imports.bamboo_hr.DestinationAttribute')
    mock_destination_attribute.bulk_create_or_update_destination_attributes.return_value = None
    
    # Mock send_failure_notification_email - patch it at the import location
    mock_send_failure_notification_email = mocker.patch('fyle_employee_imports.bamboo_hr.send_failure_notification_email')
    
    # Mock User model
    mock_user = mocker.patch('apps.users.models.User')
    
    return {
        'org': mock_org,
        'org_get': mock_org_get,
        'credential': mock_credential,
        'credential_get': mock_credential_get,
        'bamboohr': mock_bamboohr,
        'bamboohr_objects': mock_bamboohr_objects,
        'bamboohr_queryset': mock_bamboohr_queryset,
        'queryset_update': mock_queryset_update,
        'bamboohr_config': mock_bamboohr_config,
        'bamboohr_config_get': mock_bamboohr_config_get,
        'bamboohr_sdk': mock_bamboohr_sdk,
        'bamboohr_sdk_class': mock_bamboohr_sdk_class,
        'employees': mock_employees,
        'employees_get_all': mock_employees.get_all,
        'employees_get': mock_employees.get,
        'platform_connector': mock_platform_connector,
        'platform_connector_class': mock_platform_connector_class,
        'get_employee_by_email': mock_platform_connector.get_employee_by_email,
        'get_existing_departments_from_fyle': mock_platform_connector.get_existing_departments_from_fyle,
        'create_fyle_department_payload': mock_platform_connector.create_fyle_department_payload,
        'get_department_generator': mock_platform_connector.get_department_generator,
        'post_department': mock_platform_connector.post_department,
        'bulk_post_employees': mock_platform_connector.bulk_post_employees,
        'sync_employees': mock_platform_connector.sync_employees,
        'destination_attribute': mock_destination_attribute,
        'bulk_create_or_update_destination_attributes': mock_destination_attribute.bulk_create_or_update_destination_attributes,
        'send_failure_notification_email': mock_send_failure_notification_email,
        'user': mock_user,
        'org_get_bamboo': mock_org_get_bamboo
    } 
