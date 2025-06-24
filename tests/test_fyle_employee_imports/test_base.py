import pytest
from datetime import datetime, timezone
from django.db.models import Q
from unittest.mock import MagicMock

from fyle_employee_imports.base import FyleEmployeeImport
from apps.orgs.models import Org, FyleCredential
from apps.fyle_hrms_mappings.models import DestinationAttribute, ExpenseAttribute
from apps.users.helpers import PlatformConnector
from tests.test_fyle_employee_imports.mock_setup import (
    mock_platform_connector,
    mock_org_objects_get,
    mock_org_objects_get_exception,
    mock_fyle_credential_objects_get,
    mock_fyle_credential_objects_get_exception,
    mock_expense_attribute_objects_filter,
    mock_destination_attribute_objects_filter,
    mock_send_failure_notification_email_base
)


def test_fyle_employee_import_init_case_1(mocker):
    """
    Test FyleEmployeeImport initialization
    Case: valid org_id
    """
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = 'https://test.fyle.tech'
    mock_org_get = mock_org_objects_get(mocker, mock_org)
    
    mock_credential = mocker.MagicMock()
    mock_credential.refresh_token = 'test_refresh_token'
    mock_credential_get = mock_fyle_credential_objects_get(mocker, mock_credential)
    
    mock_platform, mock_platform_instance = mock_platform_connector(mocker)
    
    importer = FyleEmployeeImport(org_id=1)
    
    mock_platform.assert_called_once_with('test_refresh_token', 'https://test.fyle.tech')
    assert importer.org_id == 1
    assert importer.platform_connection == mock_platform_instance


def test_fyle_employee_import_init_case_2(mocker):
    """
    Test FyleEmployeeImport initialization
    Case: Org not found
    """
    mock_org_get = mock_org_objects_get_exception(mocker)
    
    with pytest.raises(Exception, match='Org not found'):
        FyleEmployeeImport(org_id=1)


def test_fyle_employee_import_init_case_3(mocker):
    """
    Test FyleEmployeeImport initialization
    Case: FyleCredential not found
    """
    mock_org = mocker.MagicMock()
    mock_org.cluster_domain = 'https://test.fyle.tech'
    mock_org_get = mock_org_objects_get(mocker, mock_org)
    mock_credential_get = mock_fyle_credential_objects_get_exception(mocker)
    
    with pytest.raises(Exception, match='Credential not found'):
        FyleEmployeeImport(org_id=1)


def test_sync_fyle_employees_case_1(mocker):
    """
    Test sync_fyle_employees method
    Case: calls platform_connection.sync_employees
    """
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    importer.org_id = 1
    importer.platform_connection = mocker.MagicMock()
    
    importer.sync_fyle_employees()
    
    importer.platform_connection.sync_employees.assert_called_once_with(org_id=1)


def test_get_existing_departments_from_fyle_case_1(mocker):
    """
    Test get_existing_departments_from_fyle method
    Case: returns departments dict
    """
    departments_response = {
        'data': [
            {
                'id': 1,
                'display_name': 'Engineering',
                'is_enabled': True
            },
            {
                'id': 2,
                'display_name': 'Sales',
                'is_enabled': False
            }
        ]
    }
    
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    importer.platform_connection = mocker.MagicMock()
    importer.platform_connection.get_department_generator.return_value = [departments_response]
    
    result = importer.get_existing_departments_from_fyle()
    
    expected = {
        'Engineering': {'id': 1, 'is_enabled': True},
        'Sales': {'id': 2, 'is_enabled': False}
    }
    assert result == expected
    importer.platform_connection.get_department_generator.assert_called_once_with(query_params={'order': 'id.desc'})


def test_get_existing_departments_from_fyle_case_2(mocker):
    """
    Test get_existing_departments_from_fyle method
    Case: empty departments response
    """
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    importer.platform_connection = mocker.MagicMock()
    importer.platform_connection.get_department_generator.return_value = [{'data': []}]
    
    result = importer.get_existing_departments_from_fyle()
    
    assert result == {}


def test_create_fyle_department_payload_case_1(mocker):
    """
    Test create_fyle_department_payload method
    Case: existing disabled department
    """
    existing_departments = {
        'Engineering': {'id': 1, 'is_enabled': False}
    }
    new_departments = ['Engineering']
    
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    
    result = importer.create_fyle_department_payload(existing_departments, new_departments)
    
    expected = [{
        'name': 'Engineering',
        'id': 1,
        'is_enabled': True,
        'display_name': 'Engineering'
    }]
    assert result == expected


def test_create_fyle_department_payload_case_2(mocker):
    """
    Test create_fyle_department_payload method
    Case: new department
    """
    existing_departments = {}
    new_departments = ['Engineering']
    
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    
    result = importer.create_fyle_department_payload(existing_departments, new_departments)
    
    expected = [{
        'name': 'Engineering',
        'display_name': 'Engineering'
    }]
    assert result == expected


def test_create_fyle_department_payload_case_3(mocker):
    """
    Test create_fyle_department_payload method
    Case: existing enabled department (no action needed)
    """
    existing_departments = {
        'Engineering': {'id': 1, 'is_enabled': True}
    }
    new_departments = ['Engineering']
    
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    
    result = importer.create_fyle_department_payload(existing_departments, new_departments)
    
    assert result == []


def test_departments_to_be_imported_case_1(mocker):
    """
    Test departments_to_be_imported method
    Case: employees with departments
    """
    mock_employee1 = mocker.MagicMock()
    mock_employee1.detail = {'department_name': 'Engineering'}
    mock_employee2 = mocker.MagicMock()
    mock_employee2.detail = {'department_name': 'Sales'}
    mock_employee3 = mocker.MagicMock()
    mock_employee3.detail = {'department_name': 'Engineering'}  # Duplicate
    
    hrms_employees = [mock_employee1, mock_employee2, mock_employee3]
    
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    
    result = importer.departments_to_be_imported(hrms_employees)
    
    expected = {'Engineering', 'Sales'}
    assert set(result) == expected


def test_departments_to_be_imported_case_2(mocker):
    """
    Test departments_to_be_imported method
    Case: employees without departments
    """
    mock_employee1 = mocker.MagicMock()
    mock_employee1.detail = {'department_name': None}
    mock_employee2 = mocker.MagicMock()
    mock_employee2.detail = {'department_name': ''}
    
    hrms_employees = [mock_employee1, mock_employee2]
    
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    
    result = importer.departments_to_be_imported(hrms_employees)
    
    assert result == []


def test_post_department_case_1(mocker):
    """
    Test post_department method
    Case: posts multiple departments
    """
    departments_payload = [
        {'name': 'Engineering', 'display_name': 'Engineering'},
        {'name': 'Sales', 'display_name': 'Sales'}
    ]
    
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    importer.platform_connection = mocker.MagicMock()
    
    importer.post_department(departments_payload)
    
    assert importer.platform_connection.post_department.call_count == 2
    importer.platform_connection.post_department.assert_any_call({'name': 'Engineering', 'display_name': 'Engineering'})
    importer.platform_connection.post_department.assert_any_call({'name': 'Sales', 'display_name': 'Sales'})


def test_import_departments_case_1(mocker):
    """
    Test import_departments method
    Case: imports departments successfully
    """
    mock_employee1 = mocker.MagicMock()
    mock_employee1.detail = {'department_name': 'Engineering'}
    mock_employee2 = mocker.MagicMock()
    mock_employee2.detail = {'department_name': 'Sales'}
    
    hrms_employees = [mock_employee1, mock_employee2]
    
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    importer.platform_connection = mocker.MagicMock()
    
    # Mock methods
    mock_get_departments = mocker.patch.object(importer, 'get_existing_departments_from_fyle', return_value={})
    mock_create_payload = mocker.patch.object(importer, 'create_fyle_department_payload', return_value=[
        {'name': 'Engineering', 'display_name': 'Engineering'},
        {'name': 'Sales', 'display_name': 'Sales'}
    ])
    mock_post_department = mocker.patch.object(importer, 'post_department')
    
    importer.import_departments(hrms_employees)
    
    mock_get_departments.assert_called_once()
    # Check that create_fyle_department_payload was called with the correct departments (order doesn't matter)
    mock_create_payload.assert_called_once()
    call_args = mock_create_payload.call_args[0]
    assert call_args[0] == {}  # existing_departments
    assert set(call_args[1]) == {'Engineering', 'Sales'}  # new_departments
    mock_post_department.assert_called_once_with([
        {'name': 'Engineering', 'display_name': 'Engineering'},
        {'name': 'Sales', 'display_name': 'Sales'}
    ])


def test_get_employee_and_approver_payload_case_1(mocker):
    """
    Test get_employee_and_approver_payload method
    Case: employees with complete data
    """
    mock_employee1 = mocker.MagicMock()
    mock_employee1.detail = {
        'email': 'john.doe@test.com',
        'full_name': 'John Doe',
        'department_name': 'Engineering',
        'approver_emails': ['supervisor@test.com']
    }
    mock_employee1.destination_id = '123'
    mock_employee1.active = True
    
    mock_employee2 = mocker.MagicMock()
    mock_employee2.detail = {
        'email': 'jane.smith@test.com',
        'full_name': 'Jane Smith',
        'department_name': 'Sales',
        'approver_emails': ['manager@test.com']
    }
    mock_employee2.destination_id = '456'
    mock_employee2.active = True
    
    hrms_employees = [mock_employee1, mock_employee2]
    
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    importer.org_id = 1
    
    # Mock ExpenseAttribute query for existing approver emails
    mock_expense_attr = mock_expense_attribute_objects_filter(mocker)
    mock_values_list = mocker.MagicMock()
    mock_values_list.values_list.return_value = ['supervisor@test.com']
    mock_expense_attr.return_value = mock_values_list
    
    employee_payload, employee_approver_payload = importer.get_employee_and_approver_payload(hrms_employees)
    
    # Verify employee payload
    expected_employee_payload = [
        {
            'user_email': 'john.doe@test.com',
            'user_full_name': 'John Doe',
            'code': '123',
            'department_name': 'Engineering',
            'is_enabled': True
        },
        {
            'user_email': 'jane.smith@test.com',
            'user_full_name': 'Jane Smith',
            'code': '456',
            'department_name': 'Sales',
            'is_enabled': True
        }
    ]
    assert employee_payload == expected_employee_payload
    
    # Verify employee approver payload (only John's approver since supervisor@test.com exists)
    expected_approver_payload = [
        {
            'user_email': 'john.doe@test.com',
            'approver_emails': ['supervisor@test.com']
        }
    ]
    assert employee_approver_payload == expected_approver_payload
    
    # Verify ExpenseAttribute query
    mock_expense_attr.assert_called_once_with(
        org_id=1,
        attribute_type='EMPLOYEE',
        value__in=['supervisor@test.com', 'manager@test.com']
    )


def test_get_employee_and_approver_payload_case_2(mocker):
    """
    Test get_employee_and_approver_payload method
    Case: employees with missing emails
    """
    mock_employee1 = mocker.MagicMock()
    mock_employee1.detail = {
        'email': None,
        'full_name': 'John Doe',
        'department_name': 'Engineering',
        'approver_emails': ['supervisor@test.com']
    }
    mock_employee1.destination_id = '123'
    mock_employee1.active = True
    
    mock_employee2 = mocker.MagicMock()
    mock_employee2.detail = {
        'email': 'jane.smith@test.com',
        'full_name': 'Jane Smith',
        'department_name': 'Sales',
        'approver_emails': ['manager@test.com']
    }
    mock_employee2.destination_id = '456'
    mock_employee2.active = True
    
    hrms_employees = [mock_employee1, mock_employee2]
    
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    importer.org_id = 1
    
    # Mock ExpenseAttribute query for existing approver emails
    mock_expense_attr = mock_expense_attribute_objects_filter(mocker)
    mock_values_list = mocker.MagicMock()
    mock_values_list.values_list.return_value = ['manager@test.com']
    mock_expense_attr.return_value = mock_values_list
    
    employee_payload, employee_approver_payload = importer.get_employee_and_approver_payload(hrms_employees)
    
    # Verify employee payload (only Jane since John has no email)
    expected_employee_payload = [
        {
            'user_email': 'jane.smith@test.com',
            'user_full_name': 'Jane Smith',
            'code': '456',
            'department_name': 'Sales',
            'is_enabled': True
        }
    ]
    assert employee_payload == expected_employee_payload
    
    # Verify employee approver payload (only Jane's approver)
    expected_approver_payload = [
        {
            'user_email': 'jane.smith@test.com',
            'approver_emails': ['manager@test.com']
        }
    ]
    assert employee_approver_payload == expected_approver_payload


def test_get_employee_and_approver_payload_case_3(mocker):
    """
    Test get_employee_and_approver_payload method
    Case: employees with no approver emails
    """
    mock_employee1 = mocker.MagicMock()
    mock_employee1.detail = {
        'email': 'john.doe@test.com',
        'full_name': 'John Doe',
        'department_name': 'Engineering',
        'approver_emails': None
    }
    mock_employee1.destination_id = '123'
    mock_employee1.active = True
    
    hrms_employees = [mock_employee1]
    
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    importer.org_id = 1
    
    # Mock ExpenseAttribute query for existing approver emails
    mock_expense_attr = mock_expense_attribute_objects_filter(mocker)
    mock_values_list = mocker.MagicMock()
    mock_values_list.values_list.return_value = []
    mock_expense_attr.return_value = mock_values_list
    
    employee_payload, employee_approver_payload = importer.get_employee_and_approver_payload(hrms_employees)
    
    # Verify employee payload
    expected_employee_payload = [
        {
            'user_email': 'john.doe@test.com',
            'user_full_name': 'John Doe',
            'code': '123',
            'department_name': 'Engineering',
            'is_enabled': True
        }
    ]
    assert employee_payload == expected_employee_payload
    
    # Verify employee approver payload (empty since no approver emails)
    assert employee_approver_payload == []


def test_fyle_employee_import_case_1(mocker):
    """
    Test fyle_employee_import method
    Case: with employee and approver payloads
    """
    mock_employee1 = mocker.MagicMock()
    mock_employee1.detail = {
        'email': 'john.doe@test.com',
        'full_name': 'John Doe',
        'department_name': 'Engineering',
        'approver_emails': ['supervisor@test.com']
    }
    mock_employee1.destination_id = '123'
    mock_employee1.active = True
    
    hrms_employees = [mock_employee1]
    
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    importer.org_id = 1
    importer.platform_connection = mocker.MagicMock()
    
    # Mock methods
    mocker.patch.object(importer, 'get_employee_and_approver_payload', return_value=(
        [{'user_email': 'john.doe@test.com'}],
        [{'user_email': 'john.doe@test.com', 'approver_emails': ['supervisor@test.com']}]
    ))
    mocker.patch.object(importer, 'get_employee_exported_at', return_value=datetime(2023, 1, 1, tzinfo=timezone.utc))
    mock_save_time = mocker.patch.object(importer, 'save_employee_exported_at_time')
    
    importer.fyle_employee_import(hrms_employees)
    
    # Verify bulk_post_employees called twice (once for employees, once for approvers)
    assert importer.platform_connection.bulk_post_employees.call_count == 2
    importer.platform_connection.bulk_post_employees.assert_any_call(employees_payload=[{'user_email': 'john.doe@test.com'}])
    importer.platform_connection.bulk_post_employees.assert_any_call(employees_payload=[{'user_email': 'john.doe@test.com', 'approver_emails': ['supervisor@test.com']}])
    
    # Verify sync_employees called
    importer.platform_connection.sync_employees.assert_called_once_with(org_id=1)
    
    # Verify save_employee_exported_at_time called with current time
    mock_save_time.assert_called_once()
    # Check that it was called with a datetime argument (either positional or keyword)
    call_args = mock_save_time.call_args
    assert len(call_args[0]) > 0 or 'employee_exported_at' in call_args[1]


def test_fyle_employee_import_case_2(mocker):
    """
    Test fyle_employee_import method
    Case: empty employee payload
    """
    hrms_employees = []
    
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    importer.org_id = 1
    importer.platform_connection = mocker.MagicMock()
    
    # Mock methods
    mocker.patch.object(importer, 'get_employee_and_approver_payload', return_value=([], []))
    mocker.patch.object(importer, 'get_employee_exported_at', return_value=datetime(2023, 1, 1, tzinfo=timezone.utc))
    mock_save_time = mocker.patch.object(importer, 'save_employee_exported_at_time')
    
    importer.fyle_employee_import(hrms_employees)
    
    # Verify no bulk_post_employees calls
    importer.platform_connection.bulk_post_employees.assert_not_called()
    
    # Verify sync_employees called
    importer.platform_connection.sync_employees.assert_called_once_with(org_id=1)
    
    # Verify save_employee_exported_at_time called with original time
    mock_save_time.assert_called_once_with(employee_exported_at=datetime(2023, 1, 1, tzinfo=timezone.utc))


def test_sync_employees_case_1(mocker):
    """
    Test sync_employees method
    Case: full sync process
    """
    mock_employee1 = mocker.MagicMock()
    mock_employee1.detail = {'department_name': 'Engineering'}
    
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    importer.org_id = 1
    importer.platform_connection = mocker.MagicMock()
    
    # Mock methods
    mock_sync_fyle = mocker.patch.object(importer, 'sync_fyle_employees')
    mock_sync_hrms = mocker.patch.object(importer, 'sync_hrms_employees')
    mocker.patch.object(importer, 'get_employee_exported_at', return_value=datetime(2023, 1, 1, tzinfo=timezone.utc))
    mock_import_dept = mocker.patch.object(importer, 'import_departments')
    mock_fyle_import = mocker.patch.object(importer, 'fyle_employee_import')
    
    # Mock DestinationAttribute query
    mock_dest_attr = mock_destination_attribute_objects_filter(mocker)
    mock_dest_attr.return_value.order_by.return_value = [mock_employee1]
    
    importer.sync_employees(is_incremental_sync=True)
    
    # Verify sync methods called
    mock_sync_fyle.assert_called_once()
    mock_sync_hrms.assert_called_once_with(is_incremental_sync=True)
    
    # Verify DestinationAttribute query
    mock_dest_attr.assert_called_once_with(
        attribute_type='EMPLOYEE',
        org_id=1,
        updated_at__gte=datetime(2023, 1, 1, tzinfo=timezone.utc)
    )
    
    # Verify import methods called
    mock_import_dept.assert_called_once_with([mock_employee1])
    mock_fyle_import.assert_called_once_with([mock_employee1])


def test_send_employee_email_missing_failure_notification_case_1(mocker):
    """
    Test send_employee_email_missing_failure_notification method
    Case: sends notification email for missing employees
    """
    # Mock the database query to return employees with missing emails
    mock_dest_attr = mock_destination_attribute_objects_filter(mocker)
    mock_queryset = mocker.MagicMock()
    mock_values = mocker.MagicMock()
    mock_order_by = mocker.MagicMock()
    mock_update = mocker.MagicMock()
    
    # Set up the mock chain
    mock_dest_attr.return_value = mock_queryset
    mock_queryset.values.return_value = mock_values
    mock_values.order_by.return_value = mock_order_by
    mock_order_by.update = mock_update
    
    # Mock the query result
    mock_order_by.__iter__ = lambda x: iter([
        {'detail__full_name': 'John Doe', 'destination_id': '123'},
        {'detail__full_name': 'Jane Smith', 'destination_id': '456'}
    ])
    mock_order_by.__len__ = lambda x: 2
    
    # Mock the email function
    mock_send_email = mock_send_failure_notification_email_base(mocker)
    
    # Mock get_admin_email method
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    importer.org_id = 1
    mocker.patch.object(importer, 'get_admin_email', return_value=['admin@test.com'])
    
    importer.send_employee_email_missing_failure_notification()
    
    # Verify the query was called correctly
    mock_dest_attr.assert_called_once_with(
        mocker.ANY,  # Q(detail__email=None)
        attribute_type='EMPLOYEE',
        org_id=1,
        is_failure_email_sent=False
    )
    
    # Verify email was sent
    mock_send_email.assert_called_once_with(
        employees=[
            {'name': 'John Doe', 'id': '123'},
            {'name': 'Jane Smith', 'id': '456'}
        ],
        number_of_employees=2,
        admin_email=['admin@test.com']
    )
    
    # Verify update was called
    mock_update.assert_called_once_with(is_failure_email_sent=True)


def test_send_employee_email_missing_failure_notification_case_2(mocker):
    """
    Test send_employee_email_missing_failure_notification method
    Case: no missing employees (empty list)
    """
    mock_employees = []
    
    mock_dest_attr = mock_destination_attribute_objects_filter(mocker)
    mock_send_email = mock_send_failure_notification_email_base(mocker)
    
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    importer.org_id = 1
    
    importer.send_employee_email_missing_failure_notification()
    
    mock_send_email.assert_not_called()


def test_abstract_methods_case_1(mocker):
    """
    Test abstract methods raise NotImplementedError
    Case: sync_hrms_employees
    """
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    
    with pytest.raises(NotImplementedError, match='Implement sync_hrms_employees\\(\\) in the child class'):
        importer.sync_hrms_employees(is_incremental_sync=True)


def test_abstract_methods_case_2(mocker):
    """
    Test abstract methods raise NotImplementedError
    Case: get_admin_email
    """
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    
    with pytest.raises(NotImplementedError, match='Implement get_admin_email\\(\\) in the child class'):
        importer.get_admin_email()


def test_abstract_methods_case_3(mocker):
    """
    Test abstract methods raise NotImplementedError
    Case: set_employee_exported_at
    """
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    
    with pytest.raises(NotImplementedError, match='Implement set_employee_exported_at\\(\\) in the child class'):
        importer.set_employee_exported_at()


def test_abstract_methods_case_4(mocker):
    """
    Test abstract methods raise NotImplementedError
    Case: get_employee_exported_at
    """
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    
    with pytest.raises(NotImplementedError, match='Implement get_employee_exported_at\\(\\) in the child class'):
        importer.get_employee_exported_at()


def test_abstract_methods_case_5(mocker):
    """
    Test abstract methods raise NotImplementedError
    Case: save_employee_exported_at_time
    """
    importer = FyleEmployeeImport.__new__(FyleEmployeeImport)
    
    with pytest.raises(NotImplementedError, match='Implement save_hrms\\(\\) in the child class'):
        importer.save_employee_exported_at_time(datetime.now()) 
