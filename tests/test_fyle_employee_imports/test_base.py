import pytest
from datetime import datetime
from django.db.models import Q

from fyle_employee_imports.base import FyleEmployeeImport
from fyle_employee_imports.bamboo_hr import BambooHrEmployeeImport
from apps.fyle_hrms_mappings.models import ExpenseAttribute, DestinationAttribute
from apps.bamboohr.email import send_failure_notification_email
from .fixtures import (
    dummy_org_id,
    dummy_refresh_token,
    cluster_domain,
    existing_departments_response,
    new_departments,
    department_payload,
    expected_department_payload,
    expected_disabled_department_payload
)
from .mock_setup import (
    mock_test_sync_fyle_employees,
    mock_test_get_existing_departments_from_fyle,
    mock_test_create_fyle_department_payload,
    mock_test_create_fyle_department_payload_with_disabled_department,
    mock_test_departments_to_be_imported,
    mock_test_post_department,
    mock_test_import_departments,
    mock_test_fyle_employee_import,
    mock_test_sync_employees,
    mock_test_get_employee_and_approver_payload,
    mock_test___init__
)


def test___init__(mock_dependencies, create_org):
    """
    Test __init__ method
    """
    employee_import = FyleEmployeeImport(create_org.id)
    
    assert employee_import.org_id == create_org.id
    assert employee_import.platform_connection == mock_dependencies.platform_connector


@pytest.mark.shared_mocks(lambda mocker: mock_test_sync_fyle_employees(mocker))
def test_sync_fyle_employees(mock_dependencies, create_org):
    """
    Test sync_fyle_employees method
    """
    employee_import = FyleEmployeeImport(create_org.id)
    employee_import.sync_fyle_employees()
    
    mock_dependencies.sync_employees.assert_called_once_with(org_id=create_org.id)


@pytest.mark.shared_mocks(lambda mocker: mock_test_get_existing_departments_from_fyle(mocker))
def test_get_existing_departments_from_fyle(mock_dependencies, create_org):
    """
    Test get_existing_departments_from_fyle method
    """
    employee_import = FyleEmployeeImport(create_org.id)
    result = employee_import.get_existing_departments_from_fyle()
    
    expected_departments = existing_departments_response
    assert result == expected_departments
    
    mock_dependencies.get_department_generator.assert_called_once_with(
        query_params={'order': 'id.desc'}
    )


@pytest.mark.shared_mocks(lambda mocker: mock_test_create_fyle_department_payload(mocker))
def test_create_fyle_department_payload(mock_dependencies, create_org):
    """
    Test create_fyle_department_payload method
    """
    employee_import = FyleEmployeeImport(create_org.id)
    result = employee_import.create_fyle_department_payload(
        existing_departments_response, 
        new_departments
    )
    
    assert result == mock_dependencies.expected_payload


def test_create_fyle_department_payload_with_disabled_department(mock_dependencies, create_org):
    """
    Test create_fyle_department_payload method with disabled department
    """
    employee_import = FyleEmployeeImport(create_org.id)
    result = employee_import.create_fyle_department_payload(
        existing_departments_response, 
        ['Marketing']
    )
    
    assert result == mock_dependencies.expected_disabled_payload


def test_departments_to_be_imported(mock_dependencies, create_org):
    """
    Test departments_to_be_imported method
    """
    employee_import = FyleEmployeeImport(create_org.id)
    result = employee_import.departments_to_be_imported(mock_dependencies.mock_employees)
    
    assert set(result) == set(mock_dependencies.expected_departments_set)


def test_post_department(mock_dependencies, create_org):
    """
    Test post_department method
    """
    employee_import = FyleEmployeeImport(create_org.id)
    employee_import.post_department(department_payload)
    
    assert mock_dependencies.post_department.call_count == len(department_payload)
    for department in department_payload:
        mock_dependencies.post_department.assert_any_call(department)


def test_import_departments(mock_dependencies, create_org):
    """
    Test import_departments method
    """
    employee_import = FyleEmployeeImport(create_org.id)
    employee_import.import_departments(mock_dependencies.mock_employees)
    
    mock_dependencies.get_department_generator.assert_called_once()
    mock_dependencies.post_department.assert_called()


def test_get_employee_and_approver_payload(mock_dependencies, create_org, create_expense_attribute):
    """
    Test get_employee_and_approver_payload method
    """
    employee_import = FyleEmployeeImport(create_org.id)
    emp_payload, approver_payload = employee_import.get_employee_and_approver_payload(mock_dependencies.mock_employees)

    assert emp_payload == mock_dependencies.expected_employee_payload
    assert approver_payload == mock_dependencies.expected_approver_payload


def test_fyle_employee_import(mock_dependencies, create_bamboohr_full_setup):
    """
    Test fyle_employee_import method
    """
    employee_import = BambooHrEmployeeImport(create_bamboohr_full_setup['org'].id)
    employee_import.fyle_employee_import(mock_dependencies.mock_employees)
    
    mock_dependencies.bulk_post_employees.assert_called()
    mock_dependencies.sync_employees.assert_called_once_with(org_id=create_bamboohr_full_setup['org'].id)


def test_sync_employees(mock_dependencies, create_bamboohr_full_setup):
    """
    Test sync_employees method
    """
    employee_import = BambooHrEmployeeImport(create_bamboohr_full_setup['org'].id)
    employee_import.sync_employees(is_incremental_sync=True)
    
    mock_dependencies.sync_employees.assert_called_with(org_id=create_bamboohr_full_setup['org'].id)


def test_abstract_methods_raise_not_implemented_error(mock_dependencies, create_org):
    """
    Test abstract methods raise NotImplementedError
    """
    employee_import = FyleEmployeeImport(create_org.id)
    
    with pytest.raises(NotImplementedError):
        employee_import.sync_hrms_employees(is_incremental_sync=True)
    
    with pytest.raises(NotImplementedError):
        employee_import.get_admin_email()
    
    with pytest.raises(NotImplementedError):
        employee_import.set_employee_exported_at()
    
    with pytest.raises(NotImplementedError):
        employee_import.get_employee_exported_at()
    
    with pytest.raises(NotImplementedError):
        employee_import.save_employee_exported_at_time(employee_exported_at=datetime.now())


def test_send_employee_email_missing_failure_notification(mock_dependencies, create_org):
    """
    Test send_employee_email_missing_failure_notification method
    """
    employee_import = FyleEmployeeImport(create_org.id)
    employee_import.send_employee_email_missing_failure_notification()


def test_send_employee_email_missing_failure_notification_database_operations(mock_dependencies, create_destination_attributes, create_bamboohr_full_setup, create_employee_missing_email):
    """
    Test send_employee_email_missing_failure_notification method with real database operations
    """
    org_id = create_bamboohr_full_setup['org'].id
    
    employees_with_missing_emails = DestinationAttribute.objects.filter(
        Q(detail__email=None),
        attribute_type='EMPLOYEE',
        org_id=org_id,
        is_failure_email_sent=False
    ).values('detail__full_name', 'destination_id')
    
    assert create_employee_missing_email.org_id == org_id
    
    employee_import = BambooHrEmployeeImport(org_id)
    
    employee_import.send_employee_email_missing_failure_notification()
    
    updated_employees = DestinationAttribute.objects.filter(
        Q(detail__email=None),
        attribute_type='EMPLOYEE',
        org_id=org_id,
        is_failure_email_sent=True  # Should be True after the method call
    ).values('detail__full_name', 'destination_id')
    
    assert len(updated_employees) >= 1, "At least one employee should have been marked as having received notification"
    
    updated_employee = DestinationAttribute.objects.get(destination_id='999', org_id=org_id)
    assert updated_employee.is_failure_email_sent is True
    
    jane_smith = DestinationAttribute.objects.get(destination_id='456', org_id=org_id)
    assert jane_smith.is_failure_email_sent is True 
