import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock
from django.core.exceptions import ObjectDoesNotExist
from fyle_employee_imports.bamboo_hr import BambooHrEmployeeImport
from apps.bamboohr.models import BambooHrConfiguration
from tests.test_fyle_employee_imports.mock_setup import (
    mock_bamboo_hr_sdk,
    mock_org_objects_get,
    mock_fyle_credential_objects_get,
    mock_bamboo_hr_objects_filter,
    mock_bamboo_hr_configuration_objects_get,
    mock_bamboo_hr_configuration_objects_get_exception,
    mock_send_failure_notification_email,
    mock_destination_attribute_bulk_create
)


def test_bamboo_hr_employee_import_init_case_1(mocker):
    """
    Test BambooHrEmployeeImport initialization
    Case: valid org_id
    """
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = 'https://test.fyle.tech'
    mock_org_get = mock_org_objects_get(mocker, mock_org)
    
    mock_credential = mocker.MagicMock()
    mock_credential.refresh_token = 'test_refresh_token'
    mock_credential_get = mock_fyle_credential_objects_get(mocker, mock_credential)
    
    mocker.patch('fyle_employee_imports.base.PlatformConnector')
    
    mock_bamboohr = mocker.MagicMock()
    mock_bamboohr.api_token = 'test_api_token'
    mock_bamboohr.sub_domain = 'test_subdomain'
    mock_bamboohr_queryset = mocker.MagicMock()
    mock_bamboohr_queryset.first.return_value = mock_bamboohr
    mock_bamboohr_filter = mock_bamboo_hr_objects_filter(mocker, mock_bamboohr_queryset)
    
    mock_configuration = mocker.MagicMock()
    mock_configuration_get = mock_bamboo_hr_configuration_objects_get(mocker, mock_configuration)
    
    mock_sdk, mock_sdk_instance = mock_bamboo_hr_sdk(mocker)
    
    importer = BambooHrEmployeeImport(org_id=1)
    
    mock_bamboohr_filter.assert_called_once_with(org_id__in=[1])
    mock_configuration_get.assert_called_once_with(org_id__in=[1])
    mock_sdk.assert_called_once_with(api_token='test_api_token', sub_domain='test_subdomain')
    assert importer.org_id == 1
    assert importer.bamboohr == mock_bamboohr
    assert importer.bamboohr_configuration == mock_configuration
    assert importer.bamboohr_sdk == mock_sdk_instance


def test_bamboo_hr_employee_import_init_case_2(mocker):
    """
    Test BambooHrEmployeeImport initialization
    Case: BambooHR not found
    """
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = 'https://test.fyle.tech'
    mock_org_get = mock_org_objects_get(mocker, mock_org)
    
    mock_credential = mocker.MagicMock()
    mock_credential.refresh_token = 'test_refresh_token'
    mock_credential_get = mock_fyle_credential_objects_get(mocker, mock_credential)
    
    mocker.patch('fyle_employee_imports.base.PlatformConnector')
    
    mock_bamboohr_queryset = mocker.MagicMock()
    mock_bamboohr_queryset.first.return_value = None
    mock_bamboohr_filter = mock_bamboo_hr_objects_filter(mocker, mock_bamboohr_queryset)
    
    mock_configuration = mocker.MagicMock()
    mock_configuration_get = mock_bamboo_hr_configuration_objects_get(mocker, mock_configuration)
    
    mock_sdk, mock_sdk_instance = mock_bamboo_hr_sdk(mocker)
    
    with pytest.raises(AttributeError):
        BambooHrEmployeeImport(org_id=1)


def test_bamboo_hr_employee_import_init_case_3(mocker):
    """
    Test BambooHrEmployeeImport initialization
    Case: configuration not found
    """
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = 'https://test.fyle.tech'
    mock_org_get = mock_org_objects_get(mocker, mock_org)
    
    mock_credential = mocker.MagicMock()
    mock_credential.refresh_token = 'test_refresh_token'
    mock_credential_get = mock_fyle_credential_objects_get(mocker, mock_credential)
    
    mocker.patch('fyle_employee_imports.base.PlatformConnector')
    
    mock_bamboohr = mocker.MagicMock()
    mock_bamboohr.api_token = 'test_api_token'
    mock_bamboohr.sub_domain = 'test_subdomain'
    mock_bamboohr_queryset = mocker.MagicMock()
    mock_bamboohr_queryset.first.return_value = mock_bamboohr
    mock_bamboohr_filter = mock_bamboo_hr_objects_filter(mocker, mock_bamboohr_queryset)
    
    mock_configuration_get = mock_bamboo_hr_configuration_objects_get_exception(mocker)
    
    mock_sdk, mock_sdk_instance = mock_bamboo_hr_sdk(mocker)
    
    with pytest.raises(Exception):
        BambooHrEmployeeImport(org_id=1)


def test_get_admin_email_case_1(mocker):
    """
    Test get_admin_email method
    Case: returns email list
    """
    mock_configuration = mocker.MagicMock()
    mock_configuration.emails_selected = [
        {'email': 'admin1@test.com', 'name': 'Admin One'},
        {'email': 'admin2@test.com', 'name': 'Admin Two'}
    ]
    
    importer = BambooHrEmployeeImport.__new__(BambooHrEmployeeImport)
    importer.bamboohr_configuration = mock_configuration
    
    result = importer.get_admin_email()
    
    expected = ['admin1@test.com', 'admin2@test.com']
    assert result == expected


def test_get_admin_email_case_2(mocker):
    """
    Test get_admin_email method
    Case: empty emails_selected
    """
    mock_configuration = mocker.MagicMock()
    mock_configuration.emails_selected = []
    
    importer = BambooHrEmployeeImport.__new__(BambooHrEmployeeImport)
    importer.bamboohr_configuration = mock_configuration
    
    result = importer.get_admin_email()
    
    assert result == []


def test_save_employee_exported_at_time_case_1(mocker):
    """
    Test save_employee_exported_at_time method
    Case: updates employee_exported_at
    """
    mock_queryset = mocker.MagicMock()
    mock_queryset.update = mocker.MagicMock()
    
    importer = BambooHrEmployeeImport.__new__(BambooHrEmployeeImport)
    importer.bamboohr_queryset = mock_queryset
    
    test_time = datetime.now(timezone.utc)
    
    importer.save_employee_exported_at_time(test_time)
    
    mock_queryset.update.assert_called_once_with(employee_exported_at=test_time)


def test_get_employee_exported_at_case_1(mocker):
    """
    Test get_employee_exported_at method
    Case: returns employee_exported_at
    """
    mock_bamboohr = mocker.MagicMock()
    mock_bamboohr.employee_exported_at = datetime.now(timezone.utc)
    
    importer = BambooHrEmployeeImport.__new__(BambooHrEmployeeImport)
    importer.bamboohr = mock_bamboohr
    
    result = importer.get_employee_exported_at()
    
    assert result == mock_bamboohr.employee_exported_at


def test_sync_hrms_employees_case_1(mocker):
    """
    Test sync_hrms_employees
    Case: incremental sync
    """
    mock_org = mocker.MagicMock()
    mock_org.created_at = datetime(2023, 1, 1, tzinfo=timezone.utc)
    mock_org_get = mock_org_objects_get(mocker, mock_org)
    
    mock_sdk = mocker.MagicMock()
    mock_sdk.employees.get_all.return_value = {'employees': []}
    
    importer = BambooHrEmployeeImport.__new__(BambooHrEmployeeImport)
    importer.org_id = 1
    importer.bamboohr_sdk = mock_sdk
    
    mocker.patch.object(importer, 'upsert_employees')
    
    importer.sync_hrms_employees(is_incremental_sync=True)
    
    expected_sync_from = '2023-01-01T00:00:00+00:00'
    mock_sdk.employees.get_all.assert_called_once_with(
        is_incremental_sync=True, 
        sync_employee_from=expected_sync_from
    )
    importer.upsert_employees.assert_called_once_with({'employees': []})


def test_sync_hrms_employees_case_2(mocker):
    """
    Test sync_hrms_employees
    Case: full sync
    """
    mock_sdk = mocker.MagicMock()
    mock_sdk.employees.get_all.return_value = {'employees': []}
    
    importer = BambooHrEmployeeImport.__new__(BambooHrEmployeeImport)
    importer.bamboohr_sdk = mock_sdk
    
    mock_upsert = mocker.patch.object(importer, 'upsert_employees')
    
    importer.sync_hrms_employees(is_incremental_sync=False)
    
    mock_sdk.employees.get_all.assert_called_once_with(is_incremental_sync=False, sync_employee_from=None)
    mock_upsert.assert_called_once_with({'employees': []})


def test_sync_with_webhook_complete_employee_case_1(mocker):
    """
    Test sync_with_webhook method
    Case: complete employee with supervisor
    """
    employee = {
        'id': '123',
        'firstName': 'John',
        'lastName': 'Doe',
        'workEmail': 'john.doe@test.com',
        'supervisorEId': '456',
        'department': 'Engineering',
        'status': 'Active'
    }
    
    supervisor_response = {
        'workEmail': 'supervisor@test.com'
    }
    
    mock_fyle_employee = [{'id': '789', 'email': 'supervisor@test.com'}]
    
    importer = BambooHrEmployeeImport.__new__(BambooHrEmployeeImport)
    importer.bamboohr_sdk = mocker.MagicMock()
    importer.bamboohr_sdk.employees.get.return_value = supervisor_response
    importer.platform_connection = mocker.MagicMock()
    importer.platform_connection.get_employee_by_email.return_value = mock_fyle_employee
    
    # Mock methods
    mocker.patch.object(importer, 'get_admin_email', return_value=['admin@test.com'])
    mocker.patch.object(importer, 'get_existing_departments_from_fyle', return_value={})
    mocker.patch.object(importer, 'create_fyle_department_payload', return_value=[{'name': 'Engineering'}])
    
    importer.sync_with_webhook(employee)
    
    # Verify supervisor lookup
    importer.bamboohr_sdk.employees.get.assert_called_once_with('456')
    importer.platform_connection.get_employee_by_email.assert_called_once_with(email='supervisor@test.com')
    
    # Verify employee payload
    expected_employee_payload = [{
        'user_email': 'john.doe@test.com',
        'user_full_name': 'John Doe',
        'code': '123',
        'department_name': 'Engineering',
        'is_enabled': 'Active'
    }]
    importer.platform_connection.bulk_post_employees.assert_any_call(employees_payload=expected_employee_payload)
    
    # Verify approver payload
    expected_approver_payload = [{
        'user_email': 'john.doe@test.com',
        'approver_emails': ['supervisor@test.com']
    }]
    importer.platform_connection.bulk_post_employees.assert_any_call(employees_payload=expected_approver_payload)
    
    # Verify department creation
    importer.platform_connection.post_department.assert_called_once_with({'name': 'Engineering'})


def test_sync_with_webhook_missing_email_case_1(mocker):
    """
    Test sync_with_webhook method
    Case: employee with missing work email
    """
    employee = {
        'id': '123',
        'firstName': 'John',
        'lastName': 'Doe',
        'workEmail': None,  # Missing email
        'department': 'Engineering',
        'status': 'Active'
    }
    
    importer = BambooHrEmployeeImport.__new__(BambooHrEmployeeImport)
    importer.platform_connection = mocker.MagicMock()
    
    # Mock methods
    mocker.patch.object(importer, 'get_admin_email', return_value=['admin@test.com'])
    mock_send_email = mocker.patch('fyle_employee_imports.bamboo_hr.send_failure_notification_email')
    
    importer.sync_with_webhook(employee)
    
    # Verify failure email was sent
    mock_send_email.assert_called_once_with(
        employees=[{'name': 'John Doe', 'id': '123'}],
        number_of_employees=1,
        admin_email=['admin@test.com']
    )
    
    # Verify no employee creation
    importer.platform_connection.bulk_post_employees.assert_not_called()


def test_sync_with_webhook_no_supervisor_case_1(mocker):
    """
    Test sync_with_webhook method
    Case: employee without supervisor
    """
    employee = {
        'id': '123',
        'firstName': 'John',
        'lastName': 'Doe',
        'workEmail': 'john.doe@test.com',
        'supervisorEId': None,  # No supervisor
        'department': 'Engineering',
        'status': 'Active'
    }
    
    importer = BambooHrEmployeeImport.__new__(BambooHrEmployeeImport)
    importer.bamboohr_sdk = mocker.MagicMock()
    importer.platform_connection = mocker.MagicMock()
    
    # Mock methods
    mocker.patch.object(importer, 'get_admin_email', return_value=['admin@test.com'])
    mocker.patch.object(importer, 'get_existing_departments_from_fyle', return_value={})
    mocker.patch.object(importer, 'create_fyle_department_payload', return_value=[{'name': 'Engineering'}])
    
    importer.sync_with_webhook(employee)
    
    # Verify no supervisor lookup
    importer.bamboohr_sdk.employees.get.assert_not_called()
    
    # Verify only employee payload (no approver payload)
    expected_employee_payload = [{
        'user_email': 'john.doe@test.com',
        'user_full_name': 'John Doe',
        'code': '123',
        'department_name': 'Engineering',
        'is_enabled': 'Active'
    }]
    importer.platform_connection.bulk_post_employees.assert_called_once_with(employees_payload=expected_employee_payload)


def test_sync_with_webhook_supervisor_not_found_case_1(mocker):
    """
    Test sync_with_webhook method
    Case: supervisor not found in Fyle
    """
    employee = {
        'id': '123',
        'firstName': 'John',
        'lastName': 'Doe',
        'workEmail': 'john.doe@test.com',
        'supervisorEId': '456',
        'department': 'Engineering',
        'status': 'Active'
    }
    
    supervisor_response = {
        'workEmail': 'supervisor@test.com'
    }
    
    importer = BambooHrEmployeeImport.__new__(BambooHrEmployeeImport)
    importer.bamboohr_sdk = mocker.MagicMock()
    importer.bamboohr_sdk.employees.get.return_value = supervisor_response
    importer.platform_connection = mocker.MagicMock()
    importer.platform_connection.get_employee_by_email.return_value = []  # Supervisor not found
    
    # Mock methods
    mocker.patch.object(importer, 'get_admin_email', return_value=['admin@test.com'])
    mocker.patch.object(importer, 'get_existing_departments_from_fyle', return_value={})
    mocker.patch.object(importer, 'create_fyle_department_payload', return_value=[{'name': 'Engineering'}])
    
    importer.sync_with_webhook(employee)
    
    # Verify supervisor lookup
    importer.bamboohr_sdk.employees.get.assert_called_once_with('456')
    importer.platform_connection.get_employee_by_email.assert_called_once_with(email='supervisor@test.com')
    
    # Verify only employee payload (no approver payload since supervisor not found)
    expected_employee_payload = [{
        'user_email': 'john.doe@test.com',
        'user_full_name': 'John Doe',
        'code': '123',
        'department_name': 'Engineering',
        'is_enabled': 'Active'
    }]
    importer.platform_connection.bulk_post_employees.assert_called_once_with(employees_payload=expected_employee_payload)


def test_sync_with_webhook_no_department_case_1(mocker):
    """
    Test sync_with_webhook method
    Case: employee without department
    """
    employee = {
        'id': '123',
        'firstName': 'John',
        'lastName': 'Doe',
        'workEmail': 'john.doe@test.com',
        'department': None,
        'status': 'Active'
    }
    
    importer = BambooHrEmployeeImport.__new__(BambooHrEmployeeImport)
    importer.platform_connection = mocker.MagicMock()
    
    # Mock methods
    mocker.patch.object(importer, 'get_admin_email', return_value=['admin@test.com'])
    
    importer.sync_with_webhook(employee)
    
    # Verify employee payload with empty department
    expected_employee_payload = [{
        'user_email': 'john.doe@test.com',
        'user_full_name': 'John Doe',
        'code': '123',
        'department_name': '',
        'is_enabled': 'Active'
    }]
    importer.platform_connection.bulk_post_employees.assert_called_once_with(employees_payload=expected_employee_payload)
    
    # Verify no department creation
    importer.platform_connection.post_department.assert_not_called()


def test_upsert_employees_case_1(mocker):
    """
    Test upsert_employees method
    Case: successful employee upsert
    """
    employees_data = {
        'employees': [
            {
                'id': 1,
                'firstName': 'John',
                'lastName': 'Doe',
                'workEmail': 'john.doe@example.com',
                'jobTitle': 'Software Engineer',
                'department': 'Engineering',
                'supervisor': 'Jane Smith'
            }
        ]
    }
    
    importer = BambooHrEmployeeImport.__new__(BambooHrEmployeeImport)
    importer.org_id = 1
    
    # Mock DestinationAttribute bulk create
    mock_bulk_create = mock_destination_attribute_bulk_create(mocker)
    
    # Mock send_failure_notification_email
    mock_send_email = mock_send_failure_notification_email(mocker)
    
    importer.upsert_employees(employees_data)
    
    # Verify bulk_create called with correct data
    mock_bulk_create.assert_called_once()
    call_kwargs = mock_bulk_create.call_args[1]  # Keyword arguments
    
    # Verify employee data structure
    attributes = call_kwargs['attributes']
    assert len(attributes) == 1
    employee = attributes[0]
    assert employee['value'] == 'John Doe'  # display_name
    assert employee['detail']['full_name'] == 'John Doe'
    assert employee['detail']['email'] == 'john.doe@example.com'
    assert employee['detail']['department_name'] == 'Engineering'
    assert employee['detail']['approver_emails'] == [None]  # supervisorEmail is None
    assert employee['attribute_type'] == 'EMPLOYEE'
    assert employee['destination_id'] == 1  # The actual value is int, not string


def test_upsert_employees_no_display_name_case_1(mocker):
    """
    Test upsert_employees method
    Case: employee without display name (uses firstName + lastName)
    """
    employees = {
        'employees': [
            {
                'id': '123',
                'firstName': 'John',
                'lastName': 'Doe',
                'displayName': None,  # Will use firstName + lastName
                'workEmail': 'john.doe@test.com',
                'department': 'Engineering',
                'status': 'Active',
                'supervisorEmail': 'supervisor@test.com'
            }
        ]
    }
    
    importer = BambooHrEmployeeImport.__new__(BambooHrEmployeeImport)
    importer.org_id = 1
    
    # Mock DestinationAttribute.bulk_create_or_update_destination_attributes
    mock_bulk_create = mocker.patch('fyle_employee_imports.bamboo_hr.DestinationAttribute.bulk_create_or_update_destination_attributes')
    
    result = importer.upsert_employees(employees)
    
    # Verify bulk_create was called with correct attributes
    expected_attributes = [
        {
            'attribute_type': 'EMPLOYEE',
            'value': 'John Doe',  # firstName + lastName
            'destination_id': '123',
            'detail': {
                'email': 'john.doe@test.com',
                'department_name': 'Engineering',
                'full_name': 'John Doe',
                'approver_emails': ['supervisor@test.com']
            },
            'active': True
        }
    ]
    
    mock_bulk_create.assert_called_once_with(
        attributes=expected_attributes,
        attribute_type='EMPLOYEE',
        org_id=1,
        update=True
    )
    assert result == []


def test_upsert_employees_empty_list_case_1(mocker):
    """
    Test upsert_employees method
    Case: empty employees list
    """
    employees = {'employees': []}
    
    importer = BambooHrEmployeeImport.__new__(BambooHrEmployeeImport)
    importer.org_id = 1
    
    # Mock DestinationAttribute.bulk_create_or_update_destination_attributes
    mock_bulk_create = mocker.patch('fyle_employee_imports.bamboo_hr.DestinationAttribute.bulk_create_or_update_destination_attributes')
    
    result = importer.upsert_employees(employees)
    
    # Verify bulk_create was called with empty attributes
    mock_bulk_create.assert_called_once_with(
        attributes=[],
        attribute_type='EMPLOYEE',
        org_id=1,
        update=True
    )
    assert result == [] 
