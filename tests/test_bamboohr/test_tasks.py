import pytest
from apps.bamboohr.tasks import (
    import_employees,
    schedule_sync_employees,
    delete_sync_employee_schedule,
    schedule_failure_emails_for_employees,
    add_bamboo_hr_to_integrations,
    deactivate_bamboo_hr_integration,
    invalidate_token_and_get_response
)
from apps.bamboohr.models import BambooHr
from apps.integrations.models import Integration
from apps.orgs.models import Org
from django_q.models import Schedule
from admin_settings import settings


def test_import_employees_case_1(mocker, add_org, db):
    """
    Test import_employees task
    Case: calls sync_employees with incremental sync
    """
    mock_importer = mocker.patch('apps.bamboohr.tasks.BambooHrEmployeeImport')
    mock_instance = mock_importer.return_value
    
    import_employees(org_id=add_org.id, is_incremental_sync=True)
    
    mock_importer.assert_called_once_with(org_id=add_org.id)
    mock_instance.sync_employees.assert_called_once_with(is_incremental_sync=True)


def test_import_employees_case_2(mocker, add_org, db):
    """
    Test import_employees task
    Case: calls sync_employees without incremental sync
    """
    mock_importer = mocker.patch('apps.bamboohr.tasks.BambooHrEmployeeImport')
    mock_instance = mock_importer.return_value
    
    import_employees(org_id=add_org.id, is_incremental_sync=False)

    mock_importer.assert_called_once_with(org_id=add_org.id)
    mock_instance.sync_employees.assert_called_once_with(is_incremental_sync=False)


def test_schedule_sync_employees_case_1(mocker, add_org, db):
    """
    Test schedule_sync_employees task
    Case: creates schedule and failure emails
    """
    mock_schedule_failure = mocker.patch('apps.bamboohr.tasks.schedule_failure_emails_for_employees')
    
    schedule_sync_employees(org_id=add_org.id)
    
    # Verify schedule was created
    schedule = Schedule.objects.filter(
        func='apps.bamboohr.tasks.import_employees',
        args=f'{add_org.id},True'
    ).first()
    assert schedule is not None
    assert schedule.schedule_type == Schedule.MINUTES
    assert schedule.minutes == 6 * 60
    
    mock_schedule_failure.assert_called_once_with(add_org.id)


def test_delete_sync_employee_schedule_case_1(mocker, add_org, db):
    """
    Test delete_sync_employee_schedule task
    Case: deletes existing schedule
    """
    # Create a schedule first
    schedule = Schedule.objects.create(
        func='apps.bamboohr.tasks.import_employees',
        args=f'{add_org.id},True',
        schedule_type=Schedule.MINUTES,
        minutes=6 * 60
    )
    
    delete_sync_employee_schedule(org_id=add_org.id)
    
    # Verify schedule was deleted
    assert Schedule.objects.filter(
        func='apps.bamboohr.tasks.import_employees',
        args=f'{add_org.id},True'
    ).exists() is False


def test_delete_sync_employee_schedule_case_2(mocker, add_org, db):
    """
    Test delete_sync_employee_schedule task
    Case: no schedule exists to delete
    """
    delete_sync_employee_schedule(org_id=add_org.id)
    
    # Verify no schedule exists
    assert Schedule.objects.filter(
        func='apps.bamboohr.tasks.import_employees',
        args=f'{add_org.id},True'
    ).exists() is False


def test_schedule_failure_emails_for_employees_case_1(mocker, add_org, db):
    """
    Test schedule_failure_emails_for_employees task
    Case: schedules failure emails
    """
    schedule_failure_emails_for_employees(org_id=add_org.id)
    
    # Verify schedule was created
    schedule = Schedule.objects.filter(
        func='apps.bamboohr.tasks.send_employee_email_missing_failure_notification',
        args=str(add_org.id)
    ).first()
    assert schedule is not None
    assert schedule.schedule_type == Schedule.MINUTES
    assert schedule.minutes == 7 * 24 * 60


def test_add_bamboo_hr_to_integrations_case_1(mocker, add_org, db):
    """
    Test add_bamboo_hr_to_integrations task
    Case: adds bamboo hr integration successfully
    """
    add_bamboo_hr_to_integrations(add_org)
    
    # Verify integration was created
    integration = Integration.objects.filter(
        org_id=add_org.fyle_org_id,
        type='HRMS'
    ).first()
    assert integration is not None
    assert integration.is_active is True
    assert integration.org_name == add_org.name
    assert integration.tpa_id == settings.FYLE_CLIENT_ID
    assert integration.tpa_name == 'Fyle BambooHR Integration'


def test_deactivate_bamboo_hr_integration_case_1(mocker, add_org, db):
    """
    Test deactivate_bamboo_hr_integration task
    Case: deactivates integration successfully
    """
    # First create an integration
    integration = Integration.objects.create(
        org_id=add_org.fyle_org_id,
        type='HRMS',
        is_active=True,
        org_name=add_org.name,
        tpa_id=settings.FYLE_CLIENT_ID,
        tpa_name='Fyle BambooHR Integration'
    )
    
    deactivate_bamboo_hr_integration(add_org.id)
    
    # Verify integration was deactivated
    integration.refresh_from_db()
    assert integration.is_active is False
    assert integration.disconnected_at is not None


def test_deactivate_bamboo_hr_integration_case_2(mocker, add_org, db):
    """
    Test deactivate_bamboo_hr_integration task
    Case: no integration exists to deactivate
    """
    deactivate_bamboo_hr_integration(add_org.id)
    
    # Verify no integration exists
    assert Integration.objects.filter(
        org_id=add_org.fyle_org_id,
        type='HRMS'
    ).exists() is False


def test_invalidate_token_and_get_response_case_1(mocker, add_org, db):
    """
    Test invalidate_token_and_get_response task
    Case: invalidates token successfully
    """
    # Create a BambooHr instance
    bamboohr = BambooHr.objects.create(
        org_id=add_org.id,
        is_credentials_expired=False
    )
    
    # Create an integration
    integration = Integration.objects.create(
        org_id=add_org.fyle_org_id,
        type='HRMS',
        is_active=True,
        org_name=add_org.name,
        tpa_id=settings.FYLE_CLIENT_ID,
        tpa_name='Fyle BambooHR Integration'
    )
    
    result = invalidate_token_and_get_response(add_org.id)
    
    # Verify BambooHr credentials were expired
    bamboohr.refresh_from_db()
    assert bamboohr.is_credentials_expired is True
    
    # Verify integration token was expired
    integration.refresh_from_db()
    assert integration.is_token_expired is True
    
    assert result.status_code == 400
    assert 'Invalid token' in result.data['message']


def test_invalidate_token_and_get_response_case_2(mocker, add_org, db):
    """
    Test invalidate_token_and_get_response task
    Case: no BambooHr instance exists
    """
    result = invalidate_token_and_get_response(add_org.id)
    
    assert result.status_code == 400
    assert 'Invalid token' in result.data['message']
