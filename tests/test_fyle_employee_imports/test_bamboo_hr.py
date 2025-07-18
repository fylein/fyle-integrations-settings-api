import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
from django.utils import timezone

from fyle_employee_imports.bamboo_hr import BambooHrEmployeeImport
from apps.fyle_hrms_mappings.models import DestinationAttribute
from apps.bamboohr.models import BambooHr, BambooHrConfiguration
from tests.helper import dict_compare_keys
from .fixtures import (
    dummy_org_id,
    dummy_refresh_token,
    cluster_domain,
    employee_data,
    bamboohr_employees_response,
    admin_emails,
    webhook_payload,
    webhook_payload_no_email,
    supervisor_employee_data,
    fyle_employee_response,
    sync_employee_from_date,
    employee_exported_at,
    bamboohr_sdk_employees_response,
    destination_attributes,
    inactive_employee_response,
    webhook_payload_no_supervisor,
    webhook_payload_with_dept,
    employee_missing_display_name,
    expected_destination_attributes_data,
    expected_inactive_employee_data,
    expected_missing_display_name_data
)
from .mock_setup import mock_bamboohr_shared_mock


@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
def test_bamboohr_employee_import_init(mock_dependencies, create_bamboohr_full_setup):
    """
    Test BambooHrEmployeeImport initialization
    """
    employee_import = BambooHrEmployeeImport(create_bamboohr_full_setup['org'].id)
    
    assert employee_import.org_id == create_bamboohr_full_setup['org'].id
    assert employee_import.platform_connection is not None
    assert employee_import.bamboohr_sdk is not None
    assert employee_import.bamboohr is not None
    assert employee_import.bamboohr_configuration is not None


def test_get_admin_email(create_bamboohr_full_setup):
    """
    Test get_admin_email method
    """
    employee_import = BambooHrEmployeeImport(create_bamboohr_full_setup['org'].id)
    result = employee_import.get_admin_email()
    
    expected_emails = ['admin@example.com', 'manager@example.com']
    assert result == expected_emails


def test_save_employee_exported_at_time(mock_dependencies, create_bamboohr_full_setup, db):
    """
    Test save_employee_exported_at_time method with real database operations
    """
    bamboohr_setup = create_bamboohr_full_setup
    employee_import = BambooHrEmployeeImport(bamboohr_setup['org'].id)
    test_datetime = timezone.now()
    
    real_bamboohr = BambooHr.objects.filter(org=bamboohr_setup['org']).first()
    initial_exported_at = real_bamboohr.employee_exported_at
    
    employee_import.save_employee_exported_at_time(test_datetime)
    
    real_bamboohr.refresh_from_db()
    assert real_bamboohr.employee_exported_at == test_datetime
    assert real_bamboohr.employee_exported_at != initial_exported_at


def test_get_employee_exported_at(create_bamboohr_full_setup):
    """
    Test get_employee_exported_at method
    """
    employee_import = BambooHrEmployeeImport(create_bamboohr_full_setup['org'].id)
    result = employee_import.get_employee_exported_at()

    expected_timestamp = create_bamboohr_full_setup['bamboohr'].employee_exported_at
    assert result == expected_timestamp


@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
def test_sync_hrms_employees_with_incremental_sync(mock_dependencies, create_bamboohr_full_setup):
    """
    Test sync_hrms_employees method with incremental sync
    """
    employee_import = BambooHrEmployeeImport(create_bamboohr_full_setup['org'].id)
    employee_import.sync_hrms_employees(is_incremental_sync=True)

    expected_timestamp = create_bamboohr_full_setup['org'].created_at.replace(microsecond=0).isoformat()
    mock_dependencies.employees_get_all.assert_called_once_with(
        is_incremental_sync=True,
        sync_employee_from=expected_timestamp
    )


@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
def test_sync_hrms_employees_without_incremental_sync(mock_dependencies, create_bamboohr_full_setup):
    """
    Test sync_hrms_employees method without incremental sync
    """
    employee_import = BambooHrEmployeeImport(create_bamboohr_full_setup['org'].id)
    employee_import.sync_hrms_employees(is_incremental_sync=False)
    
    mock_dependencies.employees_get_all.assert_called_once_with(
        is_incremental_sync=False, 
        sync_employee_from=None
    )


@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
def test_sync_with_webhook_with_supervisor(mock_dependencies, create_bamboohr_full_setup):
    """
    Test sync_with_webhook method with supervisor
    """
    employee_import = BambooHrEmployeeImport(create_bamboohr_full_setup['org'].id)
    employee_import.sync_with_webhook(webhook_payload)
    
    mock_dependencies.employees_get.assert_called_once_with('999')
    mock_dependencies.get_employee_by_email.assert_called_once_with(email='supervisor@example.com')
    mock_dependencies.bulk_post_employees.assert_called()


@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
def test_sync_with_webhook_without_email(mock_dependencies, create_bamboohr_full_setup):
    """
    Test sync_with_webhook method without email
    """
    employee_import = BambooHrEmployeeImport(create_bamboohr_full_setup['org'].id)
    employee_import.sync_with_webhook(webhook_payload_no_email)

    mock_dependencies.send_failure_notification_email.assert_called_once_with(
        employees=[{'name': 'Bob Johnson', 'id': '789'}],
        number_of_employees=1,
        admin_email=['admin@example.com', 'manager@example.com']
    )


@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
def test_sync_with_webhook_without_supervisor(mock_dependencies, create_bamboohr_full_setup):
    """
    Test sync_with_webhook method without supervisor
    """
    employee_import = BambooHrEmployeeImport(create_bamboohr_full_setup['org'].id)
    # This should not raise any exceptions and should complete successfully
    employee_import.sync_with_webhook(webhook_payload_no_supervisor)
    
    # Verify that employees_get was not called (no supervisor to look up)
    mock_dependencies.employees_get.assert_not_called()


@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
def test_sync_with_webhook_with_department(mock_dependencies, create_bamboohr_full_setup):
    """
    Test sync_with_webhook method with department creation
    """
    mock_dependencies.get_existing_departments_from_fyle.return_value = {}
    
    employee_import = BambooHrEmployeeImport(create_bamboohr_full_setup['org'].id)
    # This should not raise any exceptions and should complete successfully
    employee_import.sync_with_webhook(webhook_payload_with_dept)


@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
def test_sync_with_webhook_supervisor_without_fyle_employee(mock_dependencies, create_bamboohr_full_setup):
    """
    Test sync_with_webhook method with supervisor but no Fyle employee found
    """
    mock_dependencies.get_employee_by_email.return_value = []
    
    employee_import = BambooHrEmployeeImport(create_bamboohr_full_setup['org'].id)
    # This should not raise any exceptions and should complete successfully
    employee_import.sync_with_webhook(webhook_payload)


@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
def test_upsert_employees(mock_dependencies, create_bamboohr_full_setup):
    """
    Test upsert_employees method
    """
    employee_import = BambooHrEmployeeImport(create_bamboohr_full_setup['org'].id)
    result = employee_import.upsert_employees(bamboohr_employees_response)
    
    # Verify actual database records were created
    destination_attributes = DestinationAttribute.objects.filter(
        attribute_type='EMPLOYEE',
        org_id=create_bamboohr_full_setup['org'].id
    )
    
    assert destination_attributes.count() == 3
    
    # Verify employee records using dictionary comparison
    for expected_employee in expected_destination_attributes_data:
        actual_employee = destination_attributes.get(destination_id=expected_employee['destination_id'])
        
        actual_data = {
            'attribute_type': actual_employee.attribute_type,
            'value': actual_employee.value,
            'destination_id': actual_employee.destination_id,
            'detail': actual_employee.detail,
            'active': actual_employee.active
        }
        
        assert dict_compare_keys(expected_employee, actual_data) == [], f'Employee {expected_employee["destination_id"]} data mismatch'
    
    assert result == []


@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
def test_upsert_employees_with_missing_display_name(mock_dependencies, create_bamboohr_full_setup):
    """
    Test upsert_employees method with missing display name
    """
    employee_import = BambooHrEmployeeImport(create_bamboohr_full_setup['org'].id)
    result = employee_import.upsert_employees(employee_missing_display_name)
    
    # Verify actual database record was created
    destination_attributes = DestinationAttribute.objects.filter(
        attribute_type='EMPLOYEE',
        org_id=create_bamboohr_full_setup['org'].id,
        destination_id='555'
    )
    
    assert destination_attributes.count() == 1
    
    # Verify missing display name employee using dictionary comparison
    missing_employee = destination_attributes.first()
    actual_data = {
        'attribute_type': missing_employee.attribute_type,
        'value': missing_employee.value,
        'destination_id': missing_employee.destination_id,
        'detail': missing_employee.detail,
        'active': missing_employee.active
    }
    
    assert dict_compare_keys(expected_missing_display_name_data, actual_data) == [], 'Missing display name employee data mismatch'
    
    assert result == []


@pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
def test_upsert_employees_with_inactive_status(mock_dependencies, create_bamboohr_full_setup):
    """
    Test upsert_employees method with inactive employee status
    """
    employee_import = BambooHrEmployeeImport(create_bamboohr_full_setup['org'].id)
    employee_import.upsert_employees(inactive_employee_response)
    
    # Verify actual database record was created for inactive employee
    destination_attributes = DestinationAttribute.objects.filter(
        attribute_type='EMPLOYEE',
        org_id=create_bamboohr_full_setup['org'].id,
        destination_id='999'
    )
    
    assert destination_attributes.count() == 1
    
    # Verify inactive employee using dictionary comparison
    inactive_employee = destination_attributes.first()
    actual_data = {
        'attribute_type': inactive_employee.attribute_type,
        'value': inactive_employee.value,
        'destination_id': inactive_employee.destination_id,
        'detail': inactive_employee.detail,
        'active': inactive_employee.active
    }
    
    assert dict_compare_keys(expected_inactive_employee_data[0], actual_data) == [], 'Inactive employee data mismatch'


def test_upsert_employees_database_operations(mock_dependencies, create_bamboohr_full_setup):
    """
    Test upsert_employees method with real database operations - verifies DestinationAttribute creation
    """
    bamboohr_setup = create_bamboohr_full_setup
    employee_import = BambooHrEmployeeImport(bamboohr_setup['org'].id)
    
    employee_import.upsert_employees(bamboohr_employees_response)
    
    created_attributes = DestinationAttribute.objects.filter(
        org_id=bamboohr_setup['org'].id,
        attribute_type='EMPLOYEE'
    ).order_by('destination_id')
    
    assert created_attributes.count() == 3
    
    # Verify all created employees using dictionary comparison
    for expected_employee in expected_destination_attributes_data:
        actual_employee = created_attributes.filter(destination_id=expected_employee['destination_id']).first()
        
        actual_data = {
            'attribute_type': actual_employee.attribute_type,
            'value': actual_employee.value,
            'destination_id': actual_employee.destination_id,
            'detail': actual_employee.detail,
            'active': actual_employee.active
        }
        
        assert dict_compare_keys(expected_employee, actual_data) == [], f'Database employee {expected_employee["destination_id"]} data mismatch'


def test_upsert_employees_inactive_status_database_operations(mock_dependencies, create_bamboohr_full_setup):
    """
    Test upsert_employees method with inactive employee - verifies database operations
    """
    bamboohr_setup = create_bamboohr_full_setup
    employee_import = BambooHrEmployeeImport(bamboohr_setup['org'].id)
    
    employee_import.upsert_employees(inactive_employee_response)
    
    inactive_employee = DestinationAttribute.objects.filter(
        org_id=bamboohr_setup['org'].id,
        attribute_type='EMPLOYEE',
        destination_id='999'
    ).first()
    
    assert inactive_employee is not None
    
    # Verify inactive employee using dictionary comparison
    actual_data = {
        'attribute_type': inactive_employee.attribute_type,
        'value': inactive_employee.value,
        'destination_id': inactive_employee.destination_id,
        'detail': inactive_employee.detail,
        'active': inactive_employee.active
    }
    
    assert dict_compare_keys(expected_inactive_employee_data[0], actual_data) == [], 'Database inactive employee data mismatch'

