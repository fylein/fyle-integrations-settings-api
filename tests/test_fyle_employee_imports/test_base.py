import pytest
from datetime import datetime

from fyle_employee_imports.base import FyleEmployeeImport
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
# Mock imports are now automatic based on test function names


def test___init__(mock_dependencies):
    """
    Test __init__ method
    """
    employee_import = FyleEmployeeImport(dummy_org_id)
    
    assert employee_import.org_id == dummy_org_id
    assert employee_import.platform_connection == mock_dependencies.platform_connector
    
    mock_dependencies.org_get.assert_called_once_with(id=dummy_org_id)
    mock_dependencies.credential_get.assert_called_once_with(org=mock_dependencies.org)
    mock_dependencies.platform_connector_class.assert_called_once_with(dummy_refresh_token, cluster_domain)


def test_sync_fyle_employees(mock_dependencies):
    """
    Test sync_fyle_employees method
    """
    employee_import = FyleEmployeeImport(dummy_org_id)
    employee_import.sync_fyle_employees()
    
    mock_dependencies.sync_employees.assert_called_once_with(org_id=dummy_org_id)


def test_get_existing_departments_from_fyle(mock_dependencies):
    """
    Test get_existing_departments_from_fyle method
    """
    employee_import = FyleEmployeeImport(dummy_org_id)
    result = employee_import.get_existing_departments_from_fyle()
    
    expected_departments = existing_departments_response
    assert result == expected_departments
    
    mock_dependencies.get_department_generator.assert_called_once_with(
        query_params={'order': 'id.desc'}
    )


def test_create_fyle_department_payload(mock_dependencies):
    """
    Test create_fyle_department_payload method
    """
    employee_import = FyleEmployeeImport(dummy_org_id)
    result = employee_import.create_fyle_department_payload(
        existing_departments_response, 
        new_departments
    )
    
    assert result == mock_dependencies.expected_payload


def test_create_fyle_department_payload_with_disabled_department(mock_dependencies):
    """
    Test create_fyle_department_payload method with disabled department
    """
    employee_import = FyleEmployeeImport(dummy_org_id)
    result = employee_import.create_fyle_department_payload(
        existing_departments_response, 
        ['Marketing']
    )
    
    assert result == mock_dependencies.expected_disabled_payload


def test_departments_to_be_imported(mock_dependencies):
    """
    Test departments_to_be_imported method
    """
    employee_import = FyleEmployeeImport(dummy_org_id)
    result = employee_import.departments_to_be_imported(mock_dependencies.mock_employees)
    
    assert set(result) == set(mock_dependencies.expected_departments_set)


def test_post_department(mock_dependencies):
    """
    Test post_department method
    """
    employee_import = FyleEmployeeImport(dummy_org_id)
    employee_import.post_department(department_payload)
    
    assert mock_dependencies.post_department.call_count == len(department_payload)
    for department in department_payload:
        mock_dependencies.post_department.assert_any_call(department)


def test_import_departments(mock_dependencies):
    """
    Test import_departments method
    """
    employee_import = FyleEmployeeImport(dummy_org_id)
    employee_import.import_departments(mock_dependencies.mock_employees)
    
    mock_dependencies.get_department_generator.assert_called_once()
    mock_dependencies.post_department.assert_called()


def test_get_employee_and_approver_payload(mock_dependencies):
    """
    Test get_employee_and_approver_payload method
    """
    employee_import = FyleEmployeeImport(dummy_org_id)
    emp_payload, approver_payload = employee_import.get_employee_and_approver_payload(mock_dependencies.mock_employees)
    
    assert emp_payload == mock_dependencies.expected_employee_payload
    assert approver_payload == mock_dependencies.expected_approver_payload


def test_fyle_employee_import(mock_dependencies):
    """
    Test fyle_employee_import method
    """
    employee_import = FyleEmployeeImport(dummy_org_id)
    employee_import.fyle_employee_import(mock_dependencies.mock_employees)
    
    assert mock_dependencies.bulk_post_employees.call_count == 2
    mock_dependencies.sync_employees.assert_called_once()


def test_sync_employees(mock_dependencies):
    """
    Test sync_employees method
    """
    employee_import = FyleEmployeeImport(dummy_org_id)
    employee_import.sync_employees(is_incremental_sync=True)


def test_abstract_methods_raise_not_implemented_error(mock_dependencies):
    """
    Test abstract methods raise NotImplementedError
    """
    employee_import = FyleEmployeeImport(dummy_org_id)
    
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


def test_send_employee_email_missing_failure_notification_database_operations(mock_dependencies, create_destination_attributes):
    """
    Test send_employee_email_missing_failure_notification method with real database operations
    """
    # Get the employee with missing email from the fixture
    employee_missing_email = create_destination_attributes[1]  # Jane Smith with missing email
    org_id = employee_missing_email.org_id
    
    employee_import = FyleEmployeeImport(org_id)
    employee_import.send_employee_email_missing_failure_notification()
    
    # Verify that is_failure_email_sent was updated for the employee with missing email
    employee_missing_email.refresh_from_db()
    assert employee_missing_email.is_failure_email_sent is True
    
    # Verify that send_failure_notification_email was called
    mock_dependencies.send_failure_notification_email.assert_called_once() 
