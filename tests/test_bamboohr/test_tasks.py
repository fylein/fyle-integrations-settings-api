import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from django_q.models import Schedule
from rest_framework.response import Response
from rest_framework.views import status

from apps.bamboohr.tasks import (
    import_employees, update_employee, send_employee_email_missing_failure_notification,
    schedule_sync_employees, delete_sync_employee_schedule, schedule_failure_emails_for_employees,
    add_bamboo_hr_to_integrations, deactivate_bamboo_hr_integration, invalidate_token_and_get_response
)
from apps.bamboohr.models import BambooHr
from apps.integrations.models import Integration
from apps.orgs.models import Org


@pytest.mark.django_db
class TestBambooHrTasks:
    def test_import_employees(self, mocker):
        """Test import_employees task"""
        mock_importer = mocker.patch('apps.bamboohr.tasks.BambooHrEmployeeImport')
        mock_instance = mock_importer.return_value
        
        import_employees(org_id=1, is_incremental_sync=True)
        
        mock_importer.assert_called_once_with(org_id=1)
        mock_instance.sync_employees.assert_called_once_with(is_incremental_sync=True)

    def test_update_employee(self, mocker):
        """Test update_employee task"""
        mock_importer = mocker.patch('apps.bamboohr.tasks.BambooHrEmployeeImport')
        mock_instance = mock_importer.return_value
        
        payload = {
            'employees': [{
                'id': 123,
                'fields': {
                    'firstName': {'value': 'John'},
                    'lastName': {'value': 'Doe'},
                    'status': {'value': 'Active'}
                }
            }]
        }
        
        update_employee(org_id=1, payload=payload)
        
        mock_importer.assert_called_once_with(org_id=1)
        mock_instance.sync_with_webhook.assert_called_once()
        call_args = mock_instance.sync_with_webhook.call_args[1]['employee']
        assert call_args['id'] == 123
        assert call_args['firstName'] == 'John'
        assert call_args['lastName'] == 'Doe'
        assert call_args['status'] is True

    def test_send_employee_email_missing_failure_notification(self, mocker):
        """Test send_employee_email_missing_failure_notification task"""
        mock_importer = mocker.patch('apps.bamboohr.tasks.BambooHrEmployeeImport')
        mock_instance = mock_importer.return_value
        
        send_employee_email_missing_failure_notification(org_id=1)
        
        mock_importer.assert_called_once_with(org_id=1)
        mock_instance.send_employee_email_missing_failure_notification.assert_called_once()

    def test_schedule_sync_employees(self, mocker):
        """Test schedule_sync_employees task"""
        mock_schedule = mocker.patch('apps.bamboohr.tasks.Schedule.objects.update_or_create')
        mock_schedule_failure = mocker.patch('apps.bamboohr.tasks.schedule_failure_emails_for_employees')
        
        schedule_sync_employees(org_id=1)
        
        mock_schedule.assert_called_once()
        call_args = mock_schedule.call_args[1]
        assert call_args['func'] == 'apps.bamboohr.tasks.import_employees'
        assert call_args['args'] == '1,True'
        assert call_args['defaults']['schedule_type'] == Schedule.MINUTES
        assert call_args['defaults']['minutes'] == 6 * 60
        
        mock_schedule_failure.assert_called_once_with(1)

    def test_delete_sync_employee_schedule(self, mocker):
        """Test delete_sync_employee_schedule task"""
        mock_schedule = mocker.patch('apps.bamboohr.tasks.Schedule.objects.filter')
        mock_schedule_instance = MagicMock()
        mock_schedule.return_value.first.return_value = mock_schedule_instance
        
        delete_sync_employee_schedule(org_id=1)
        
        mock_schedule.assert_called_once_with(
            func='apps.bamboohr.tasks.import_employees',
            args='1,True'
        )
        mock_schedule_instance.delete.assert_called_once()

    def test_delete_sync_employee_schedule_no_schedule(self, mocker):
        """Test delete_sync_employee_schedule when no schedule exists"""
        mock_schedule = mocker.patch('apps.bamboohr.tasks.Schedule.objects.filter')
        mock_schedule.return_value.first.return_value = None
        
        delete_sync_employee_schedule(org_id=1)
        
        mock_schedule.assert_called_once_with(
            func='apps.bamboohr.tasks.import_employees',
            args='1,True'
        )

    def test_schedule_failure_emails_for_employees(self, mocker):
        """Test schedule_failure_emails_for_employees task"""
        mock_schedule = mocker.patch('apps.bamboohr.tasks.Schedule.objects.update_or_create')
        
        schedule_failure_emails_for_employees(org_id=1)
        
        mock_schedule.assert_called_once()
        call_args = mock_schedule.call_args[1]
        assert call_args['func'] == 'apps.bamboohr.tasks.send_employee_email_missing_failure_notification'
        assert call_args['args'] == '1'
        assert call_args['defaults']['schedule_type'] == Schedule.MINUTES
        assert call_args['defaults']['minutes'] == 7 * 24 * 60

    def test_add_bamboo_hr_to_integrations(self, mocker):
        """Test add_bamboo_hr_to_integrations task"""
        mock_logger = mocker.patch('apps.bamboohr.tasks.logger')
        mock_integration = mocker.patch('apps.bamboohr.tasks.Integration.objects.update_or_create')
        
        org = MagicMock()
        org.fyle_org_id = 'test_org_id'
        org.name = 'Test Org'
        
        add_bamboo_hr_to_integrations(org)
        
        mock_logger.info.assert_called_once()
        mock_integration.assert_called_once_with(
            org_id='test_org_id',
            type='HRMS',
            defaults={
                'is_active': True,
                'org_name': 'Test Org',
                'tpa_id': mocker.ANY,  # settings.FYLE_CLIENT_ID
                'tpa_name': 'Fyle BambooHR Integration'
            }
        )

    def test_deactivate_bamboo_hr_integration(self, mocker):
        """Test deactivate_bamboo_hr_integration task"""
        mock_logger = mocker.patch('apps.bamboohr.tasks.logger')
        mock_org = mocker.patch('apps.bamboohr.tasks.Org.objects.get')
        mock_integration = mocker.patch('apps.bamboohr.tasks.Integration.objects.filter')
        
        org = MagicMock()
        org.fyle_org_id = 'test_org_id'
        org.name = 'Test Org'
        mock_org.return_value = org
        
        integration_instance = MagicMock()
        mock_integration.return_value.first.return_value = integration_instance
        
        deactivate_bamboo_hr_integration(org_id=1)
        
        mock_org.assert_called_once_with(id=1)
        mock_integration.assert_called_once_with(org_id='test_org_id', type='HRMS')
        assert integration_instance.is_active is False
        assert integration_instance.disconnected_at is not None
        integration_instance.save.assert_called_once()
        mock_logger.info.assert_called_once()

    def test_deactivate_bamboo_hr_integration_not_found(self, mocker):
        """Test deactivate_bamboo_hr_integration when integration not found"""
        mock_logger = mocker.patch('apps.bamboohr.tasks.logger')
        mock_org = mocker.patch('apps.bamboohr.tasks.Org.objects.get')
        mock_integration = mocker.patch('apps.bamboohr.tasks.Integration.objects.filter')
        
        org = MagicMock()
        org.fyle_org_id = 'test_org_id'
        org.name = 'Test Org'
        mock_org.return_value = org
        
        mock_integration.return_value.first.return_value = None
        
        deactivate_bamboo_hr_integration(org_id=1)
        
        mock_logger.error.assert_called_once()

    def test_invalidate_token_and_get_response(self, mocker):
        """Test invalidate_token_and_get_response task"""
        mock_logger = mocker.patch('apps.bamboohr.tasks.logger')
        mock_bamboohr = mocker.patch('apps.bamboohr.tasks.BambooHr.objects.filter')
        mock_org = mocker.patch('apps.bamboohr.tasks.Org.objects.get')
        mock_integration = mocker.patch('apps.bamboohr.tasks.Integration.objects.filter')
        
        bamboohr_instance = MagicMock()
        mock_bamboohr.return_value.first.return_value = bamboohr_instance
        
        org = MagicMock()
        org.fyle_org_id = 'test_org_id'
        org.name = 'Test Org'
        mock_org.return_value = org
        
        response = invalidate_token_and_get_response(org_id=1)
        
        assert bamboohr_instance.is_credentials_expired is True
        bamboohr_instance.save.assert_called_once()
        mock_org.assert_called_once_with(id=1)
        mock_logger.info.assert_called_once()
        mock_integration.assert_called_once_with(org_id='test_org_id', type='HRMS')
        mock_integration.return_value.update.assert_called_once()
        
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['message'] == 'Invalid token'

    def test_invalidate_token_and_get_response_no_bamboohr(self, mocker):
        """Test invalidate_token_and_get_response when no bamboohr instance exists"""
        mock_logger = mocker.patch('apps.bamboohr.tasks.logger')
        mock_bamboohr = mocker.patch('apps.bamboohr.tasks.BambooHr.objects.filter')
        mock_org = mocker.patch('apps.bamboohr.tasks.Org.objects.get')
        mock_integration = mocker.patch('apps.bamboohr.tasks.Integration.objects.filter')
        
        mock_bamboohr.return_value.first.return_value = None
        
        org = MagicMock()
        org.fyle_org_id = 'test_org_id'
        org.name = 'Test Org'
        mock_org.return_value = org
        
        response = invalidate_token_and_get_response(org_id=1)
        
        mock_org.assert_called_once_with(id=1)
        mock_logger.info.assert_called_once()
        mock_integration.assert_called_once_with(org_id='test_org_id', type='HRMS')
        mock_integration.return_value.update.assert_called_once()
        
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['message'] == 'Invalid token'
