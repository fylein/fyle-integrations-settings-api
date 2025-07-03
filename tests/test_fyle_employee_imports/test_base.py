import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch

from fyle_employee_imports.base import FyleEmployeeImport
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
    expense_attributes
)


class TestFyleEmployeeImport:
    """
    Test class for FyleEmployeeImport base functionality
    """

    def test_fyle_employee_import_init(self, mock_dependencies):
        """
        Test FyleEmployeeImport initialization
        """
        with patch('fyle_employee_imports.base.Org.objects.get') as mock_org_get, \
             patch('fyle_employee_imports.base.FyleCredential.objects.get') as mock_credential_get, \
             patch('fyle_employee_imports.base.PlatformConnector') as mock_platform_connector_class:
            
            mock_org = MagicMock()
            mock_org.cluster_domain = cluster_domain
            mock_org_get.return_value = mock_org
            
            mock_credential = MagicMock()
            mock_credential.refresh_token = dummy_refresh_token
            mock_credential_get.return_value = mock_credential
            
            mock_platform_connector = MagicMock()
            mock_platform_connector_class.return_value = mock_platform_connector
            
            employee_import = FyleEmployeeImport(dummy_org_id)
            
            assert employee_import.org_id == dummy_org_id
            assert employee_import.platform_connection == mock_platform_connector
            
            mock_org_get.assert_called_once_with(id=dummy_org_id)
            mock_credential_get.assert_called_once_with(org=mock_org)
            mock_platform_connector_class.assert_called_once_with(dummy_refresh_token, cluster_domain)

    def test_sync_fyle_employees(self, mock_dependencies):
        """
        Test sync_fyle_employees method
        """
        with patch('fyle_employee_imports.base.Org.objects.get'), \
             patch('fyle_employee_imports.base.FyleCredential.objects.get'), \
             patch('fyle_employee_imports.base.PlatformConnector') as mock_platform_connector_class:
            
            mock_platform_connector = MagicMock()
            mock_platform_connector_class.return_value = mock_platform_connector
            
            employee_import = FyleEmployeeImport(dummy_org_id)
            employee_import.sync_fyle_employees()
            
            mock_platform_connector.sync_employees.assert_called_once_with(org_id=dummy_org_id)

    def test_get_existing_departments_from_fyle(self, mock_dependencies):
        """
        Test get_existing_departments_from_fyle method
        """
        with patch('fyle_employee_imports.base.Org.objects.get'), \
             patch('fyle_employee_imports.base.FyleCredential.objects.get'), \
             patch('fyle_employee_imports.base.PlatformConnector') as mock_platform_connector_class:
            
            mock_platform_connector = MagicMock()
            mock_platform_connector.get_department_generator.return_value = [{'data': department_generator_response}]
            mock_platform_connector_class.return_value = mock_platform_connector
            
            employee_import = FyleEmployeeImport(dummy_org_id)
            result = employee_import.get_existing_departments_from_fyle()
            
            expected_departments = existing_departments_response
            assert result == expected_departments
            
            mock_platform_connector.get_department_generator.assert_called_once_with(
                query_params={'order': 'id.desc'}
            )

    def test_create_fyle_department_payload(self, mock_dependencies):
        """
        Test create_fyle_department_payload method
        """
        with patch('fyle_employee_imports.base.Org.objects.get'), \
             patch('fyle_employee_imports.base.FyleCredential.objects.get'), \
             patch('fyle_employee_imports.base.PlatformConnector'):
            
            employee_import = FyleEmployeeImport(dummy_org_id)
            result = employee_import.create_fyle_department_payload(
                existing_departments_response, 
                new_departments
            )
            
            expected_payload = [
                {
                    'name': 'Sales',
                    'display_name': 'Sales'
                },
                {
                    'name': 'HR',
                    'display_name': 'HR'
                }
            ]
            
            assert result == expected_payload

    def test_create_fyle_department_payload_with_disabled_department(self, mock_dependencies):
        """
        Test create_fyle_department_payload method with disabled department
        """
        with patch('fyle_employee_imports.base.Org.objects.get'), \
             patch('fyle_employee_imports.base.FyleCredential.objects.get'), \
             patch('fyle_employee_imports.base.PlatformConnector'):
            
            employee_import = FyleEmployeeImport(dummy_org_id)
            result = employee_import.create_fyle_department_payload(
                existing_departments_response, 
                ['Marketing']
            )
            
            expected_payload = [
                {
                    'name': 'Marketing',
                    'id': 'dept_456',
                    'is_enabled': True,
                    'display_name': 'Marketing'
                }
            ]
            
            assert result == expected_payload

    def test_departments_to_be_imported(self, mock_dependencies):
        """
        Test departments_to_be_imported method
        """
        with patch('fyle_employee_imports.base.Org.objects.get'), \
             patch('fyle_employee_imports.base.FyleCredential.objects.get'), \
             patch('fyle_employee_imports.base.PlatformConnector'):
            
            mock_employees = [
                MagicMock(detail={'department_name': 'Engineering'}),
                MagicMock(detail={'department_name': 'Marketing'}),
                MagicMock(detail={'department_name': 'Engineering'}),
                MagicMock(detail={'department_name': None})
            ]
            
            employee_import = FyleEmployeeImport(dummy_org_id)
            result = employee_import.departments_to_be_imported(mock_employees)
            
            assert set(result) == {'Engineering', 'Marketing'}

    def test_post_department(self, mock_dependencies):
        """
        Test post_department method
        """
        with patch('fyle_employee_imports.base.Org.objects.get'), \
             patch('fyle_employee_imports.base.FyleCredential.objects.get'), \
             patch('fyle_employee_imports.base.PlatformConnector') as mock_platform_connector_class:
            
            mock_platform_connector = MagicMock()
            mock_platform_connector_class.return_value = mock_platform_connector
            
            employee_import = FyleEmployeeImport(dummy_org_id)
            employee_import.post_department(department_payload)
            
            assert mock_platform_connector.post_department.call_count == len(department_payload)
            for department in department_payload:
                mock_platform_connector.post_department.assert_any_call(department)

    def test_import_departments(self, mock_dependencies):
        """
        Test import_departments method
        """
        with patch('fyle_employee_imports.base.Org.objects.get'), \
             patch('fyle_employee_imports.base.FyleCredential.objects.get'), \
             patch('fyle_employee_imports.base.PlatformConnector') as mock_platform_connector_class:
            
            mock_platform_connector = MagicMock()
            mock_platform_connector.get_department_generator.return_value = [{'data': department_generator_response}]
            mock_platform_connector_class.return_value = mock_platform_connector
            
            mock_employees = [
                MagicMock(detail={'department_name': 'Sales'}),
                MagicMock(detail={'department_name': 'HR'})
            ]
            
            employee_import = FyleEmployeeImport(dummy_org_id)
            employee_import.import_departments(mock_employees)
            
            mock_platform_connector.get_department_generator.assert_called_once()
            mock_platform_connector.post_department.assert_called()

    def test_get_employee_and_approver_payload(self, mock_dependencies):
        """
        Test get_employee_and_approver_payload method
        """
        with patch('fyle_employee_imports.base.Org.objects.get'), \
             patch('fyle_employee_imports.base.FyleCredential.objects.get'), \
             patch('fyle_employee_imports.base.PlatformConnector'), \
             patch('fyle_employee_imports.base.ExpenseAttribute.objects.filter') as mock_expense_filter:
            
            mock_expense_filter.return_value.values_list.return_value = ['supervisor@example.com']
            
            mock_employees = [
                MagicMock(
                    detail={
                        'email': 'john.doe@example.com',
                        'full_name': 'John Doe',
                        'department_name': 'Engineering',
                        'approver_emails': ['supervisor@example.com']
                    },
                    destination_id='123',
                    active=True
                ),
                MagicMock(
                    detail={
                        'email': None,
                        'full_name': 'Bob Johnson',
                        'department_name': 'Sales',
                        'approver_emails': []
                    },
                    destination_id='789',
                    active=True
                )
            ]
            
            employee_import = FyleEmployeeImport(dummy_org_id)
            emp_payload, approver_payload = employee_import.get_employee_and_approver_payload(mock_employees)
            
            assert len(emp_payload) == 1
            assert emp_payload[0]['user_email'] == 'john.doe@example.com'
            assert emp_payload[0]['user_full_name'] == 'John Doe'
            assert emp_payload[0]['code'] == '123'
            assert emp_payload[0]['department_name'] == 'Engineering'
            assert emp_payload[0]['is_enabled'] is True
            
            assert len(approver_payload) == 1
            assert approver_payload[0]['user_email'] == 'john.doe@example.com'
            assert approver_payload[0]['approver_emails'] == ['supervisor@example.com']

    def test_fyle_employee_import_process(self, mock_dependencies):
        """
        Test fyle_employee_import method
        """
        with patch('fyle_employee_imports.base.Org.objects.get'), \
             patch('fyle_employee_imports.base.FyleCredential.objects.get'), \
             patch('fyle_employee_imports.base.PlatformConnector') as mock_platform_connector_class, \
             patch('fyle_employee_imports.base.ExpenseAttribute.objects.filter'), \
             patch.object(FyleEmployeeImport, 'get_employee_exported_at') as mock_get_exported_at, \
             patch.object(FyleEmployeeImport, 'save_employee_exported_at_time') as mock_save_exported_at:
            
            mock_platform_connector = MagicMock()
            mock_platform_connector_class.return_value = mock_platform_connector
            mock_get_exported_at.return_value = employee_exported_at
            
            mock_employees = [
                MagicMock(
                    detail={
                        'email': 'john.doe@example.com',
                        'full_name': 'John Doe',
                        'department_name': 'Engineering',
                        'approver_emails': ['supervisor@example.com']
                    },
                    destination_id='123',
                    active=True
                )
            ]
            
            employee_import = FyleEmployeeImport(dummy_org_id)
            employee_import.fyle_employee_import(mock_employees)
            
            mock_platform_connector.bulk_post_employees.assert_called()
            mock_platform_connector.sync_employees.assert_called_once_with(org_id=dummy_org_id)
            mock_save_exported_at.assert_called_once()

    def test_sync_employees(self, mock_dependencies):
        """
        Test sync_employees method
        """
        with patch('fyle_employee_imports.base.Org.objects.get'), \
             patch('fyle_employee_imports.base.FyleCredential.objects.get'), \
             patch('fyle_employee_imports.base.PlatformConnector') as mock_platform_connector_class, \
             patch('fyle_employee_imports.base.DestinationAttribute.objects.filter') as mock_dest_filter, \
             patch.object(FyleEmployeeImport, 'sync_hrms_employees') as mock_sync_hrms, \
             patch.object(FyleEmployeeImport, 'get_employee_exported_at') as mock_get_exported_at, \
             patch.object(FyleEmployeeImport, 'import_departments') as mock_import_deps, \
             patch.object(FyleEmployeeImport, 'fyle_employee_import') as mock_fyle_import:
            
            mock_platform_connector = MagicMock()
            mock_platform_connector_class.return_value = mock_platform_connector
            mock_get_exported_at.return_value = employee_exported_at
            mock_dest_filter.return_value.order_by.return_value = destination_attributes
            
            employee_import = FyleEmployeeImport(dummy_org_id)
            employee_import.sync_employees(is_incremental_sync=True)
            
            mock_platform_connector.sync_employees.assert_called_once_with(org_id=dummy_org_id)
            mock_sync_hrms.assert_called_once_with(is_incremental_sync=True)
            mock_import_deps.assert_called_once()
            mock_fyle_import.assert_called_once()

    def test_send_employee_email_missing_failure_notification(self, mock_dependencies):
        """
        Test send_employee_email_missing_failure_notification method
        """
        with patch('fyle_employee_imports.base.Org.objects.get'), \
             patch('fyle_employee_imports.base.FyleCredential.objects.get'), \
             patch('fyle_employee_imports.base.PlatformConnector'), \
             patch('fyle_employee_imports.base.DestinationAttribute.objects.filter') as mock_dest_filter, \
             patch('fyle_employee_imports.base.send_failure_notification_email') as mock_send_email, \
             patch.object(FyleEmployeeImport, 'get_admin_email') as mock_get_admin_email:
            
            # Create a mock queryset that can be chained
            mock_queryset = MagicMock()
            mock_values_queryset = MagicMock()
            mock_ordered_queryset = MagicMock()
            
            # Set up the queryset chain: filter -> values -> order_by
            mock_dest_filter.return_value = mock_queryset
            mock_queryset.values.return_value = mock_values_queryset
            mock_values_queryset.order_by.return_value = mock_ordered_queryset
            
            # Mock the iteration and update methods
            mock_ordered_queryset.__iter__.return_value = iter(email_notification_employees)
            mock_ordered_queryset.update.return_value = None
            
            mock_get_admin_email.return_value = ['admin@example.com']
            
            employee_import = FyleEmployeeImport(dummy_org_id)
            employee_import.send_employee_email_missing_failure_notification()
            
            mock_send_email.assert_called_once_with(
                employees=[{'name': 'Bob Johnson', 'id': '789'}],
                number_of_employees=1,
                admin_email=['admin@example.com']
            )
            mock_ordered_queryset.update.assert_called_once_with(is_failure_email_sent=True)

    def test_send_employee_email_missing_failure_notification_no_employees(self, mock_dependencies):
        """
        Test send_employee_email_missing_failure_notification method with no employees
        """
        with patch('fyle_employee_imports.base.Org.objects.get'), \
             patch('fyle_employee_imports.base.FyleCredential.objects.get'), \
             patch('fyle_employee_imports.base.PlatformConnector'), \
             patch('fyle_employee_imports.base.DestinationAttribute.objects.filter') as mock_dest_filter, \
             patch('fyle_employee_imports.base.send_failure_notification_email') as mock_send_email, \
             patch.object(FyleEmployeeImport, 'get_admin_email') as mock_get_admin_email:
            
            # Create a mock queryset that can be chained
            mock_queryset = MagicMock()
            mock_values_queryset = MagicMock()
            mock_ordered_queryset = MagicMock()
            
            # Set up the queryset chain: filter -> values -> order_by
            mock_dest_filter.return_value = mock_queryset
            mock_queryset.values.return_value = mock_values_queryset
            mock_values_queryset.order_by.return_value = mock_ordered_queryset
            
            # Mock the iteration to return empty list
            mock_ordered_queryset.__iter__.return_value = iter([])
            
            employee_import = FyleEmployeeImport(dummy_org_id)
            employee_import.send_employee_email_missing_failure_notification()
            
            mock_send_email.assert_not_called()
            mock_ordered_queryset.update.assert_not_called()

    def test_abstract_methods_raise_not_implemented_error(self, mock_dependencies):
        """
        Test that abstract methods raise NotImplementedError
        """
        with patch('fyle_employee_imports.base.Org.objects.get'), \
             patch('fyle_employee_imports.base.FyleCredential.objects.get'), \
             patch('fyle_employee_imports.base.PlatformConnector'):
            
            employee_import = FyleEmployeeImport(dummy_org_id)
            
            with pytest.raises(NotImplementedError):
                employee_import.sync_hrms_employees(True)
            
            with pytest.raises(NotImplementedError):
                employee_import.get_admin_email()
            
            with pytest.raises(NotImplementedError):
                employee_import.set_employee_exported_at()
            
            with pytest.raises(NotImplementedError):
                employee_import.get_employee_exported_at()
            
            with pytest.raises(NotImplementedError):
                employee_import.save_employee_exported_at_time(datetime.now()) 
