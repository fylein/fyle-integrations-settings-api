import pytest
from datetime import datetime, timezone
from django.conf import settings
from django_q.models import Schedule

from apps.bamboohr.tasks import (
    import_employees,
    update_employee,
    send_employee_email_missing_failure_notification,
    schedule_sync_employees,
    delete_sync_employee_schedule,
    schedule_failure_emails_for_employees,
    add_bamboo_hr_to_integrations,
    deactivate_bamboo_hr_integration,
    invalidate_token_and_get_response
)
from apps.integrations.models import Integration
from apps.bamboohr.models import BambooHr
from .fixtures import webhook_payload


def test_import_employees(mock_dependencies, create_org):
    """
    Test import_employees task
    """
    import_employees(create_org.id, True)
    
    mock_dependencies.bamboo_hr_employee_import.assert_called_once()
    mock_dependencies.sync_employees.assert_called_once_with(is_incremental_sync=True)


def test_import_employees_without_incremental_sync(mock_dependencies, create_org):
    """
    Test import_employees task without incremental sync
    """
    import_employees(create_org.id)
    
    mock_dependencies.bamboo_hr_employee_import.assert_called_once()
    mock_dependencies.sync_employees.assert_called_once_with(is_incremental_sync=False)


def test_update_employee(mock_dependencies, create_org):
    """
    Test update_employee task
    """
    update_employee(create_org.id, webhook_payload)
    
    mock_dependencies.bamboo_hr_employee_import.assert_called_once()
    mock_dependencies.sync_with_webhook.assert_called_once()
    
    expected_employee = {
        'id': '123',
        'firstName': 'John',
        'lastName': 'Doe', 
        'workEmail': 'john.doe@example.com',
        'status': True,
        'employeeNumber': 'EMP123'
    }
    
    call_args = mock_dependencies.sync_with_webhook.call_args[1]['employee']
    assert call_args['id'] == expected_employee['id']
    assert call_args['firstName'] == expected_employee['firstName']
    assert call_args['status'] == expected_employee['status']


def test_send_employee_email_missing_failure_notification(mock_dependencies, create_org):
    """
    Test send_employee_email_missing_failure_notification task
    """
    send_employee_email_missing_failure_notification(create_org.id)
    
    mock_dependencies.bamboo_hr_employee_import.assert_called_once()
    mock_dependencies.send_employee_email_missing_failure_notification.assert_called_once()


def test_schedule_sync_employees(mock_dependencies, create_org, db):
    """
    Test schedule_sync_employees creates correct schedules
    """
    schedule_sync_employees(create_org.id)
    
    sync_schedule = Schedule.objects.filter(
        func='apps.bamboohr.tasks.import_employees',
        args=f'{create_org.id},True'
    ).first()
    
    assert sync_schedule is not None
    assert sync_schedule.schedule_type == Schedule.MINUTES
    assert sync_schedule.minutes == 6 * 60
    
    email_schedule = Schedule.objects.filter(
        func='apps.bamboohr.tasks.send_employee_email_missing_failure_notification',
        args=f'{create_org.id}'
    ).first()
    
    assert email_schedule is not None
    assert email_schedule.schedule_type == Schedule.MINUTES
    assert email_schedule.minutes == 7 * 24 * 60


def test_delete_sync_employee_schedule(mock_dependencies, create_org, db):
    """
    Test delete_sync_employee_schedule removes schedule
    """
    schedule = Schedule.objects.create(
        func='apps.bamboohr.tasks.import_employees',
        args=f'{create_org.id},True',
        schedule_type=Schedule.MINUTES,
        minutes=6 * 60,
        next_run=datetime.now()
    )
    
    delete_sync_employee_schedule(create_org.id)
    
    assert not Schedule.objects.filter(id=schedule.id).exists()


def test_delete_sync_employee_schedule_no_schedule(mock_dependencies, create_org, db):
    """
    Test delete_sync_employee_schedule when no schedule exists
    """
    delete_sync_employee_schedule(create_org.id)
    
    schedules_count = Schedule.objects.filter(
        func='apps.bamboohr.tasks.import_employees',
        args=f'{create_org.id},True'
    ).count()
    
    assert schedules_count == 0


def test_schedule_failure_emails_for_employees(mock_dependencies, create_org, db):
    """
    Test schedule_failure_emails_for_employees creates correct schedule
    """
    schedule_failure_emails_for_employees(create_org.id)
    
    schedule = Schedule.objects.filter(
        func='apps.bamboohr.tasks.send_employee_email_missing_failure_notification',
        args=f'{create_org.id}'
    ).first()
    
    assert schedule is not None
    assert schedule.schedule_type == Schedule.MINUTES
    assert schedule.minutes == 7 * 24 * 60


def test_add_bamboo_hr_to_integrations(mock_dependencies, create_org, db):
    """
    Test add_bamboo_hr_to_integrations creates integration
    """
    add_bamboo_hr_to_integrations(create_org)
    
    integration = Integration.objects.filter(
        org_id=create_org.fyle_org_id,
        type='HRMS'
    ).first()
    
    assert integration is not None
    assert integration.is_active is True
    assert integration.org_name == create_org.name
    assert integration.tpa_id == settings.FYLE_CLIENT_ID
    assert integration.tpa_name == 'Fyle BambooHR Integration'


def test_deactivate_bamboo_hr_integration(mock_dependencies, create_org, db):
    """
    Test deactivate_bamboo_hr_integration deactivates integration
    """
    Integration.objects.create(
        org_id=create_org.fyle_org_id,
        type='HRMS',
        is_active=True,
        org_name=create_org.name,
        tpa_id=settings.FYLE_CLIENT_ID,
        tpa_name='Fyle BambooHR Integration'
    )
    
    deactivate_bamboo_hr_integration(create_org.id)
    
    integration = Integration.objects.get(
        org_id=create_org.fyle_org_id,
        type='HRMS'
    )
    
    assert integration.is_active is False
    assert integration.disconnected_at is not None


def test_deactivate_bamboo_hr_integration_not_found(mock_dependencies, create_org, db):
    """
    Test deactivate_bamboo_hr_integration when integration not found
    """
    deactivate_bamboo_hr_integration(create_org.id)
    
    integration_count = Integration.objects.filter(
        org_id=create_org.fyle_org_id,
        type='HRMS'
    ).count()
    
    assert integration_count == 0


def test_invalidate_token_and_get_response(mock_dependencies, create_org, create_bamboohr, db):
    """
    Test invalidate_token_and_get_response marks credentials as expired
    """
    response = invalidate_token_and_get_response(create_org.id)
    
    bamboohr = BambooHr.objects.get(id=create_bamboohr.id)
    assert bamboohr.is_credentials_expired is True
    
    assert response.status_code == 400
    assert response.data['message'] == 'Invalid token'
    
    integration = Integration.objects.filter(
        org_id=create_org.fyle_org_id,
        type='HRMS'
    ).first()
    
    if integration:
        assert integration.is_token_expired is True


def test_invalidate_token_and_get_response_no_bamboohr(mock_dependencies, create_org, db):
    """
    Test invalidate_token_and_get_response when no bamboohr exists
    """
    response = invalidate_token_and_get_response(create_org.id)
    
    assert response.status_code == 400
    assert response.data['message'] == 'Invalid token' 
