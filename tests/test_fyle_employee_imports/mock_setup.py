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
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = cluster_domain
    mock_org_get = mocker.patch('fyle_employee_imports.base.Org.objects.get', return_value=mock_org)
    
    mock_credential = mocker.MagicMock()
    mock_credential.refresh_token = dummy_refresh_token
    mock_credential_get = mocker.patch('fyle_employee_imports.base.FyleCredential.objects.get', return_value=mock_credential)
    
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'org': mock_org,
        'org_get': mock_org_get,
        'credential': mock_credential,
        'credential_get': mock_credential_get,
        'platform_connector': mock_platform_connector,
        'platform_connector_class': mock_platform_connector_class
    }


def mock_test_sync_fyle_employees(mocker):
    """
    Mock setup for sync_fyle_employees method
    """
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = cluster_domain
    mock_org_get = mocker.patch('fyle_employee_imports.base.Org.objects.get', return_value=mock_org)
    
    mock_credential = mocker.MagicMock()
    mock_credential.refresh_token = dummy_refresh_token
    mock_credential_get = mocker.patch('fyle_employee_imports.base.FyleCredential.objects.get', return_value=mock_credential)
    
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
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = cluster_domain
    mock_org_get = mocker.patch('fyle_employee_imports.base.Org.objects.get', return_value=mock_org)
    
    mock_credential = mocker.MagicMock()
    mock_credential.refresh_token = dummy_refresh_token
    mock_credential_get = mocker.patch('fyle_employee_imports.base.FyleCredential.objects.get', return_value=mock_credential)
    
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
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = cluster_domain
    mock_org_get = mocker.patch('fyle_employee_imports.base.Org.objects.get', return_value=mock_org)
    
    mock_credential = mocker.MagicMock()
    mock_credential.refresh_token = dummy_refresh_token
    mock_credential_get = mocker.patch('fyle_employee_imports.base.FyleCredential.objects.get', return_value=mock_credential)
    
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
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = cluster_domain
    mock_org_get = mocker.patch('fyle_employee_imports.base.Org.objects.get', return_value=mock_org)
    
    mock_credential = mocker.MagicMock()
    mock_credential.refresh_token = dummy_refresh_token
    mock_credential_get = mocker.patch('fyle_employee_imports.base.FyleCredential.objects.get', return_value=mock_credential)
    
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    return {
        'expected_disabled_payload': expected_disabled_department_payload
    }


def mock_test_abstract_methods_raise_not_implemented_error(mocker):
    """
    Mock setup for abstract_methods_raise_not_implemented_error method
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
        'org': mock_org,
        'org_get': mock_org_get,
        'credential': mock_credential,
        'credential_get': mock_credential_get,
        'platform_connector': mock_platform_connector,
        'platform_connector_class': mock_platform_connector_class
    }


def mock_test_departments_to_be_imported(mocker):
    """
    Mock setup for departments_to_be_imported method
    """
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = cluster_domain
    mock_org_get = mocker.patch('fyle_employee_imports.base.Org.objects.get', return_value=mock_org)
    
    mock_credential = mocker.MagicMock()
    mock_credential.refresh_token = dummy_refresh_token
    mock_credential_get = mocker.patch('fyle_employee_imports.base.FyleCredential.objects.get', return_value=mock_credential)
    
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
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = cluster_domain
    mock_org_get = mocker.patch('fyle_employee_imports.base.Org.objects.get', return_value=mock_org)
    
    mock_credential = mocker.MagicMock()
    mock_credential.refresh_token = dummy_refresh_token
    mock_credential_get = mocker.patch('fyle_employee_imports.base.FyleCredential.objects.get', return_value=mock_credential)
    
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
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = cluster_domain
    mock_org_get = mocker.patch('fyle_employee_imports.base.Org.objects.get', return_value=mock_org)
    
    mock_credential = mocker.MagicMock()
    mock_credential.refresh_token = dummy_refresh_token
    mock_credential_get = mocker.patch('fyle_employee_imports.base.FyleCredential.objects.get', return_value=mock_credential)
    
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
        'get_department_generator': mock_platform_connector.get_department_generator,
        'post_department': mock_platform_connector.post_department,
        'mock_employees': mock_employees
    }


def mock_test_get_employee_and_approver_payload(mocker):
    """
    Mock setup for get_employee_and_approver_payload method
    """
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = cluster_domain
    mock_org_get = mocker.patch('fyle_employee_imports.base.Org.objects.get', return_value=mock_org)
    
    mock_credential = mocker.MagicMock()
    mock_credential.refresh_token = dummy_refresh_token
    mock_credential_get = mocker.patch('fyle_employee_imports.base.FyleCredential.objects.get', return_value=mock_credential)
    
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    mock_expense_attribute = mocker.MagicMock()
    expense_email_values = [email for email, category in expense_attributes]
    mock_expense_attribute.objects.filter.return_value.values_list.return_value = expense_email_values
    mock_expense_attribute_patch = mocker.patch('fyle_employee_imports.base.ExpenseAttribute', mock_expense_attribute)
    
    # Create mock employees using fixture data
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
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = cluster_domain
    mock_org_get = mocker.patch('fyle_employee_imports.base.Org.objects.get', return_value=mock_org)
    
    mock_credential = mocker.MagicMock()
    mock_credential.refresh_token = dummy_refresh_token
    mock_credential_get = mocker.patch('fyle_employee_imports.base.FyleCredential.objects.get', return_value=mock_credential)
    
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector.bulk_post_employees = mocker.MagicMock()
    mock_platform_connector.sync_employees = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    mock_expense_attribute = mocker.MagicMock()
    expense_email_values = [email for email, category in expense_attributes]
    mock_expense_attribute.objects.filter.return_value.values_list.return_value = expense_email_values
    mock_expense_attribute_patch = mocker.patch('fyle_employee_imports.base.ExpenseAttribute', mock_expense_attribute)
    
    # Create mock employees using fixture data
    mock_employees = []
    for emp_data in mock_employees_for_import_process:
        mock_emp = mocker.MagicMock()
        mock_emp.detail = emp_data['detail']
        mock_emp.destination_id = emp_data['destination_id']
        mock_emp.active = emp_data['active']
        mock_employees.append(mock_emp)
    
    # Mock abstract methods called within fyle_employee_import
    mock_get_employee_exported_at = mocker.patch(
        'fyle_employee_imports.base.FyleEmployeeImport.get_employee_exported_at', 
        return_value=employee_exported_at
    )
    mock_save_employee_exported_at_time = mocker.patch(
        'fyle_employee_imports.base.FyleEmployeeImport.save_employee_exported_at_time'
    )
    
    return {
        'bulk_post_employees': mock_platform_connector.bulk_post_employees,
        'sync_employees': mock_platform_connector.sync_employees,
        'mock_employees': mock_employees,
        'expense_attribute': mock_expense_attribute,
        'get_employee_exported_at': mock_get_employee_exported_at,
        'save_employee_exported_at_time': mock_save_employee_exported_at_time
    }


def mock_test_sync_employees(mocker):
    """
    Mock setup for sync_employees method
    """
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = cluster_domain
    mock_org_get = mocker.patch('fyle_employee_imports.base.Org.objects.get', return_value=mock_org)
    
    mock_credential = mocker.MagicMock()
    mock_credential.refresh_token = dummy_refresh_token
    mock_credential_get = mocker.patch('fyle_employee_imports.base.FyleCredential.objects.get', return_value=mock_credential)
    
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector.get_department_generator.return_value = [{'data': department_generator_response}]
    mock_platform_connector.post_department = mocker.MagicMock()
    mock_platform_connector.bulk_post_employees = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    # Create mock employees that return empty list to avoid database access
    mock_employees = []
    for emp_data in mock_employees_for_departments:
        mock_emp = mocker.MagicMock()
        mock_emp.detail = emp_data['detail']
        mock_employees.append(mock_emp)
    
    # Mock DestinationAttribute to avoid database access
    mock_dest_attrs = []
    for attr_data in destination_attributes:
        mock_attr = mocker.MagicMock()
        mock_attr.detail = attr_data['detail']
        mock_attr.destination_id = attr_data['destination_id']
        mock_attr.active = attr_data['active']
        mock_dest_attrs.append(mock_attr)
    
    mock_destination_attribute = mocker.MagicMock()
    mock_destination_attribute.objects.filter.return_value.order_by.return_value = mock_dest_attrs
    mock_destination_attribute_patch = mocker.patch('fyle_employee_imports.base.DestinationAttribute', mock_destination_attribute)
    
    # Mock ExpenseAttribute for get_employee_and_approver_payload
    mock_expense_attribute = mocker.MagicMock()
    expense_email_values = [email for email, category in expense_attributes]
    mock_expense_attribute.objects.filter.return_value.values_list.return_value = expense_email_values
    mock_expense_attribute_patch = mocker.patch('fyle_employee_imports.base.ExpenseAttribute', mock_expense_attribute)
    
    # Mock abstract methods called within sync_employees
    mock_sync_hrms_employees = mocker.patch(
        'fyle_employee_imports.base.FyleEmployeeImport.sync_hrms_employees',
        return_value=mock_employees
    )
    mock_get_employee_exported_at = mocker.patch(
        'fyle_employee_imports.base.FyleEmployeeImport.get_employee_exported_at',
        return_value=employee_exported_at
    )
    mock_save_employee_exported_at_time = mocker.patch(
        'fyle_employee_imports.base.FyleEmployeeImport.save_employee_exported_at_time'
    )
    
    return {}


def mock_test_send_employee_email_missing_failure_notification(mocker):
    """
    Mock setup for send_employee_email_missing_failure_notification method
    """
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = cluster_domain
    mock_org_get = mocker.patch('fyle_employee_imports.base.Org.objects.get', return_value=mock_org)
    
    mock_credential = mocker.MagicMock()
    mock_credential.refresh_token = dummy_refresh_token
    mock_credential_get = mocker.patch('fyle_employee_imports.base.FyleCredential.objects.get', return_value=mock_credential)
    
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    # Mock DestinationAttribute for method functionality
    mock_destination_attribute = mocker.MagicMock()
    mock_queryset = mocker.MagicMock()
    mock_queryset_values = mocker.MagicMock()
    mock_queryset_final = mocker.MagicMock()
    
    mock_queryset_final.update.return_value = None
    mock_queryset_final.__iter__.return_value = iter(email_notification_employees)
    mock_queryset_final.__len__.return_value = len(email_notification_employees)
    
    mock_queryset_values.order_by.return_value = mock_queryset_final
    mock_queryset.values.return_value = mock_queryset_values
    mock_destination_attribute.objects.filter.return_value = mock_queryset
    mock_destination_attribute_patch = mocker.patch('fyle_employee_imports.base.DestinationAttribute', mock_destination_attribute)
    
    mock_send_email = mocker.patch('fyle_employee_imports.base.send_failure_notification_email')
    
    # Mock abstract method called within the method
    mock_get_admin_email = mocker.patch(
        'fyle_employee_imports.base.FyleEmployeeImport.get_admin_email',
        return_value=admin_emails[0]
    )
    
    return {}


# BambooHR specific mock functions
def mock_bamboohr_employee_import_init(mocker):
    """
    Mock setup for BambooHR employee import initialization
    """
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = cluster_domain
    mock_org.created_at = org_created_at
    mock_org_get = mocker.patch('fyle_employee_imports.base.Org.objects.get', return_value=mock_org)
    mock_org_get_bamboo = mocker.patch('fyle_employee_imports.bamboo_hr.Org.objects.get', return_value=mock_org)
    
    mock_credential = mocker.MagicMock()
    mock_credential.refresh_token = dummy_refresh_token
    mock_credential_get = mocker.patch('fyle_employee_imports.base.FyleCredential.objects.get', return_value=mock_credential)
    
    mock_bamboohr = mocker.MagicMock()
    mock_bamboohr.api_token = 'test_token'
    mock_bamboohr.sub_domain = 'test_domain'
    mock_bamboohr.employee_exported_at = employee_exported_at
    mock_bamboohr_queryset = mocker.MagicMock()
    mock_bamboohr_queryset.first.return_value = mock_bamboohr
    mock_bamboohr_objects = mocker.patch('apps.bamboohr.models.BambooHr.objects')
    mock_bamboohr_objects.filter.return_value = mock_bamboohr_queryset
    
    mock_bamboohr_config = mocker.MagicMock()
    mock_bamboohr_config.emails_selected = bamboohr_configuration_data['emails_selected']
    mock_bamboohr_config_get = mocker.patch('apps.bamboohr.models.BambooHrConfiguration.objects.get', return_value=mock_bamboohr_config)
    
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
        'platform_connector': mock_platform_connector,
        'platform_connector_class': mock_platform_connector_class,
        'org_get_bamboo': mock_org_get_bamboo
    }


def mock_bamboohr_shared_mock(mocker):
    """
    Comprehensive mock setup for BambooHR employee import tests
    """
    # Mock Org model
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = cluster_domain
    mock_org.created_at = org_created_at
    mock_org_get = mocker.patch('fyle_employee_imports.base.Org.objects.get', return_value=mock_org)
    mock_org_get_bamboo = mocker.patch('fyle_employee_imports.bamboo_hr.Org.objects.get', return_value=mock_org)
    
    # Mock FyleCredential model
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
    
    # Mock BambooHrSDK
    mock_employees = mocker.MagicMock()
    mock_employees.get_all.return_value = bamboohr_sdk_employees_response
    mock_employees.get.return_value = supervisor_employee_data
    
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk.employees = mock_employees
    mock_bamboohr_sdk_class = mocker.patch('fyle_employee_imports.bamboo_hr.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    # Mock PlatformConnector
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector.get_employee_by_email.return_value = fyle_employee_response
    mock_platform_connector.get_existing_departments_from_fyle.return_value = {'Engineering': {'id': 'dept_123', 'is_enabled': True}}
    mock_platform_connector.create_fyle_department_payload.return_value = department_payload
    mock_platform_connector.get_department_generator.return_value = [{'data': department_generator_response}]
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    # Mock DestinationAttribute
    mock_destination_attribute = mocker.patch('fyle_employee_imports.bamboo_hr.DestinationAttribute')
    mock_destination_attribute.bulk_create_or_update_destination_attributes.return_value = None
    
    # Mock send_failure_notification_email
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


def mock_test_save_employee_exported_at_time(mocker):
    """
    Mock setup for testing save_employee_exported_at_time with real database operations
    """
    # Mock external services but allow database operations
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk_class = mocker.patch('fyle_employee_imports.bamboo_hr.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    # Don't mock BambooHr.objects to allow real database operations
    
    return {
        'platform_connector': mock_platform_connector,
        'platform_connector_class': mock_platform_connector_class,
        'bamboohr_sdk': mock_bamboohr_sdk,
        'bamboohr_sdk_class': mock_bamboohr_sdk_class
    }


def mock_test_upsert_employees_database_operations(mocker):
    """
    Mock setup for testing upsert_employees with real database operations
    """
    # Mock external services but allow database operations
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk_class = mocker.patch('fyle_employee_imports.bamboo_hr.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    # Don't mock DestinationAttribute to allow real database operations
    # Don't mock BambooHr or BambooHrConfiguration to allow real database operations
    
    return {
        'platform_connector': mock_platform_connector,
        'platform_connector_class': mock_platform_connector_class,
        'bamboohr_sdk': mock_bamboohr_sdk,
        'bamboohr_sdk_class': mock_bamboohr_sdk_class
    }


def mock_test_upsert_employees_inactive_status_database_operations(mocker):
    """
    Mock setup for testing upsert_employees with inactive employee - real database operations
    """
    # Mock external services but allow database operations
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    mock_bamboohr_sdk = mocker.MagicMock()
    mock_bamboohr_sdk_class = mocker.patch('fyle_employee_imports.bamboo_hr.BambooHrSDK', return_value=mock_bamboohr_sdk)
    
    # Don't mock DestinationAttribute to allow real database operations
    
    return {
        'platform_connector': mock_platform_connector,
        'platform_connector_class': mock_platform_connector_class,
        'bamboohr_sdk': mock_bamboohr_sdk,
        'bamboohr_sdk_class': mock_bamboohr_sdk_class
    }


def mock_test_send_employee_email_missing_failure_notification_database_operations(mocker):
    """
    Mock setup for testing send_employee_email_missing_failure_notification with real database operations
    """
    # Mock external services but allow database operations
    mock_platform_connector = mocker.MagicMock()
    mock_platform_connector_class = mocker.patch('fyle_employee_imports.base.PlatformConnector', return_value=mock_platform_connector)
    
    mock_send_failure_notification_email = mocker.patch('fyle_employee_imports.base.send_failure_notification_email')
    
    # Mock the abstract method get_admin_email to prevent NotImplementedError
    mock_get_admin_email = mocker.patch('fyle_employee_imports.base.FyleEmployeeImport.get_admin_email', return_value='admin@example.com')
    
    # Don't mock DestinationAttribute to allow real database operations
    
    return {
        'platform_connector': mock_platform_connector,
        'platform_connector_class': mock_platform_connector_class,
        'send_failure_notification_email': mock_send_failure_notification_email,
        'get_admin_email': mock_get_admin_email
    } 
