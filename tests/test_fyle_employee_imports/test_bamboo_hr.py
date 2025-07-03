import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch

from fyle_employee_imports.bamboo_hr import BambooHrEmployeeImport
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
    destination_attributes
)
from .mock_setup import mock_bamboohr_shared_mock


class TestBambooHrEmployeeImport:
    """
    Test class for BambooHrEmployeeImport functionality
    """

    @pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
    def test_bamboohr_employee_import_init(self, mock_dependencies):
        """
        Test BambooHrEmployeeImport initialization
        """
        employee_import = BambooHrEmployeeImport(dummy_org_id)
        
        assert employee_import.org_id == dummy_org_id
        assert employee_import.platform_connection == mock_dependencies.platform_connector
        assert employee_import.bamboohr == mock_dependencies.bamboohr
        assert employee_import.bamboohr_configuration == mock_dependencies.bamboohr_config
        assert employee_import.bamboohr_sdk == mock_dependencies.bamboohr_sdk
        
        mock_dependencies.org_get_bamboo.assert_called_once_with(id=dummy_org_id)
        mock_dependencies.credential_get.assert_called_once_with(org=mock_dependencies.org)
        mock_dependencies.bamboohr_objects.filter.assert_called_once_with(org_id__in=[dummy_org_id])
        mock_dependencies.bamboohr_config_get.assert_called_once_with(org_id__in=[dummy_org_id])
        mock_dependencies.bamboohr_sdk_class.assert_called_once_with(api_token='test_token', sub_domain='test_domain')

    @pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
    def test_get_admin_email(self, mock_dependencies):
        """
        Test get_admin_email method
        """
        employee_import = BambooHrEmployeeImport(dummy_org_id)
        result = employee_import.get_admin_email()
        
        expected_emails = ['admin@example.com', 'manager@example.com']
        assert result == expected_emails

    @pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
    def test_save_employee_exported_at_time(self, mock_dependencies):
        """
        Test save_employee_exported_at_time method
        """
        employee_import = BambooHrEmployeeImport(dummy_org_id)
        test_datetime = datetime.now()
        
        employee_import.save_employee_exported_at_time(test_datetime)
        
        mock_dependencies.queryset_update.assert_called_once_with(employee_exported_at=test_datetime)

    @pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
    def test_get_employee_exported_at(self, mock_dependencies):
        """
        Test get_employee_exported_at method
        """
        employee_import = BambooHrEmployeeImport(dummy_org_id)
        result = employee_import.get_employee_exported_at()
        
        assert result == employee_exported_at

    @pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
    def test_sync_hrms_employees_with_incremental_sync(self, mock_dependencies):
        """
        Test sync_hrms_employees method with incremental sync
        """
        employee_import = BambooHrEmployeeImport(dummy_org_id)
        employee_import.sync_hrms_employees(is_incremental_sync=True)
        
        mock_dependencies.employees_get_all.assert_called_once_with(
            is_incremental_sync=True, 
            sync_employee_from='2024-01-01T00:00:00+00:00'
        )

    @pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
    def test_sync_hrms_employees_without_incremental_sync(self, mock_dependencies):
        """
        Test sync_hrms_employees method without incremental sync
        """
        employee_import = BambooHrEmployeeImport(dummy_org_id)
        employee_import.sync_hrms_employees(is_incremental_sync=False)
        
        mock_dependencies.employees_get_all.assert_called_once_with(
            is_incremental_sync=False, 
            sync_employee_from=None
        )

    @pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
    def test_sync_with_webhook_with_supervisor(self, mock_dependencies):
        """
        Test sync_with_webhook method with supervisor
        """
        employee_import = BambooHrEmployeeImport(dummy_org_id)
        employee_import.sync_with_webhook(webhook_payload)
        
        mock_dependencies.employees_get.assert_called_once_with('999')
        mock_dependencies.get_employee_by_email.assert_called_once_with(email='supervisor@example.com')
        mock_dependencies.bulk_post_employees.assert_called()

    @pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
    def test_sync_with_webhook_without_email(self, mock_dependencies):
        """
        Test sync_with_webhook method without email
        """
        employee_import = BambooHrEmployeeImport(dummy_org_id)
        employee_import.sync_with_webhook(webhook_payload_no_email)
        
        mock_dependencies.send_failure_notification_email.assert_called_once_with(
            employees=[{'name': 'Bob Johnson', 'id': '789'}],
            number_of_employees=1,
            admin_email=['admin@example.com', 'manager@example.com']
        )

    @pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
    def test_sync_with_webhook_without_supervisor(self, mock_dependencies):
        """
        Test sync_with_webhook method without supervisor
        """
        webhook_payload_no_supervisor = {
            'firstName': 'Jane',
            'lastName': 'Smith',
            'workEmail': 'jane.smith@example.com',
            'status': True,
            'department': 'Marketing',
            'supervisorEId': None,
            'id': '456'
        }
        
        employee_import = BambooHrEmployeeImport(dummy_org_id)
        employee_import.sync_with_webhook(webhook_payload_no_supervisor)
        
        mock_dependencies.employees_get.assert_not_called()
        mock_dependencies.bulk_post_employees.assert_called()

    @pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
    def test_sync_with_webhook_with_department(self, mock_dependencies):
        """
        Test sync_with_webhook method with department creation
        """
        webhook_payload_with_dept = {
            'firstName': 'John',
            'lastName': 'Doe',
            'workEmail': 'john.doe@example.com',
            'status': True,
            'department': 'New Department',
            'supervisorEId': None,
            'id': '123'
        }
        
        mock_dependencies.get_existing_departments_from_fyle.return_value = {}
        
        employee_import = BambooHrEmployeeImport(dummy_org_id)
        employee_import.sync_with_webhook(webhook_payload_with_dept)
        
        mock_dependencies.get_department_generator.assert_called_once()
        mock_dependencies.post_department.assert_called_once()

    @pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
    def test_sync_with_webhook_supervisor_without_fyle_employee(self, mock_dependencies):
        """
        Test sync_with_webhook method with supervisor but no Fyle employee found
        """
        mock_dependencies.get_employee_by_email.return_value = []
        
        employee_import = BambooHrEmployeeImport(dummy_org_id)
        employee_import.sync_with_webhook(webhook_payload)
        
        mock_dependencies.employees_get.assert_called_once_with('999')
        mock_dependencies.get_employee_by_email.assert_called_once_with(email='supervisor@example.com')
        mock_dependencies.bulk_post_employees.assert_called()

    @pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
    def test_upsert_employees(self, mock_dependencies):
        """
        Test upsert_employees method
        """
        employee_import = BambooHrEmployeeImport(dummy_org_id)
        result = employee_import.upsert_employees(bamboohr_employees_response)
        
        expected_attributes = [
            {
                'attribute_type': 'EMPLOYEE',
                'value': 'John Doe',
                'destination_id': '123',
                'detail': {
                    'email': 'john.doe@example.com',
                    'department_name': 'Engineering',
                    'full_name': 'John Doe',
                    'approver_emails': ['supervisor@example.com']
                },
                'active': True
            },
            {
                'attribute_type': 'EMPLOYEE',
                'value': 'Jane Smith',
                'destination_id': '456',
                'detail': {
                    'email': 'jane.smith@example.com',
                    'department_name': 'Marketing',
                    'full_name': 'Jane Smith',
                    'approver_emails': [None]
                },
                'active': True
            },
            {
                'attribute_type': 'EMPLOYEE',
                'value': 'Bob Johnson',
                'destination_id': '789',
                'detail': {
                    'email': None,
                    'department_name': 'Sales',
                    'full_name': 'Bob Johnson',
                    'approver_emails': [None]
                },
                'active': True
            }
        ]
        
        mock_dependencies.bulk_create_or_update_destination_attributes.assert_called_once_with(
            attributes=expected_attributes,
            attribute_type='EMPLOYEE',
            org_id=dummy_org_id,
            update=True
        )
        
        assert result == []

    @pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
    def test_upsert_employees_with_missing_display_name(self, mock_dependencies):
        """
        Test upsert_employees method with missing display name
        """
        employees_response_missing_display_name = {
            'employees': [
                {
                    'id': '123',
                    'firstName': 'John',
                    'lastName': 'Doe',
                    'workEmail': 'john.doe@example.com',
                    'status': 'Active',
                    'department': 'Engineering',
                    'supervisorEmail': 'supervisor@example.com',
                    'displayName': None
                }
            ]
        }
        
        employee_import = BambooHrEmployeeImport(dummy_org_id)
        result = employee_import.upsert_employees(employees_response_missing_display_name)
        
        expected_attributes = [
            {
                'attribute_type': 'EMPLOYEE',
                'value': 'John Doe',
                'destination_id': '123',
                'detail': {
                    'email': 'john.doe@example.com',
                    'department_name': 'Engineering',
                    'full_name': 'John Doe',
                    'approver_emails': ['supervisor@example.com']
                },
                'active': True
            }
        ]
        
        mock_dependencies.bulk_create_or_update_destination_attributes.assert_called_once_with(
            attributes=expected_attributes,
            attribute_type='EMPLOYEE',
            org_id=dummy_org_id,
            update=True
        )
        
        assert result == []

    @pytest.mark.shared_mocks(lambda mocker: mock_bamboohr_shared_mock(mocker))
    def test_upsert_employees_with_inactive_status(self, mock_dependencies):
        """
        Test upsert_employees method with inactive employee status
        """
        employees_response_inactive = {
            'employees': [
                {
                    'id': '123',
                    'firstName': 'John',
                    'lastName': 'Doe',
                    'workEmail': 'john.doe@example.com',
                    'status': 'Inactive',
                    'department': 'Engineering',
                    'supervisorEmail': 'supervisor@example.com',
                    'displayName': 'John Doe'
                }
            ]
        }
        
        employee_import = BambooHrEmployeeImport(dummy_org_id)
        result = employee_import.upsert_employees(employees_response_inactive)
        
        expected_attributes = [
            {
                'attribute_type': 'EMPLOYEE',
                'value': 'John Doe',
                'destination_id': '123',
                'detail': {
                    'email': 'john.doe@example.com',
                    'department_name': 'Engineering',
                    'full_name': 'John Doe',
                    'approver_emails': ['supervisor@example.com']
                },
                'active': False
            }
        ]
        
        mock_dependencies.bulk_create_or_update_destination_attributes.assert_called_once_with(
            attributes=expected_attributes,
            attribute_type='EMPLOYEE',
            org_id=dummy_org_id,
            update=True
        )
        
        assert result == []

