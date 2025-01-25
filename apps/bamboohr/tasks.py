import logging
from apps.bamboohr.models import BambooHr
from apps.fyle_hrms_mappings.models import DestinationAttribute
from apps.integrations.models import Integration
from apps.orgs.models import FyleCredential, Org
from apps.users.helpers import PlatformConnector
from fyle_employee_imports.bamboo_hr import BambooHrEmployeeImport
from bamboosdk.bamboohrsdk import BambooHrSDK
from django_q.models import Schedule

from datetime import datetime

logger = logging.getLogger(__name__)
logger.level = logging.INFO


def import_employees(org_id: int, is_incremental_sync: bool = False):
    """
        Sync Employees from BambooHR to Fyle
    """
    bamboohr_importer = BambooHrEmployeeImport(org_id=org_id)
    bamboohr_importer.sync_employees(is_incremental_sync=is_incremental_sync)

def update_employee(org_id: int, payload: dict):
    """
        Update employee in fyle when employee in Bamboohr is added or updated
    """
    employee = {}
    payload = payload['employees'][0]
    employee['id'] = payload['id']
    payload = payload['fields']
    for field in payload.keys():
        employee[field] = payload[field]['value']
    
    employee['status'] = True if employee.get('status', None) == 'Active' else False
    
    bamboohr_importer = BambooHrEmployeeImport(org_id=org_id)
    bamboohr_importer.sync_with_webhook(employee=employee)


def send_employee_email_missing_failure_notification(org_id: int):
    """
    Send failure email to employees who don't have email associated with them
    """
    bamboo_hr_importer = BambooHrEmployeeImport(org_id=org_id)
    bamboo_hr_importer.send_employee_email_missing_failure_notification()


def schedule_sync_employees(org_id):
    """
    Create schedule to sync employees every 6 hours
    """
    Schedule.objects.update_or_create(
        func = 'apps.bamboohr.tasks.import_employees',
        args = '{},{}'.format(org_id, True),
        defaults={
                'schedule_type': Schedule.MINUTES,
                'minutes': 6 * 60,
                'next_run': datetime.now()
        }
    )

    schedule_failure_emails_for_employees(org_id)


def delete_sync_employee_schedule(org_id):
    """
    Delete schedule when bamboohr is disconnected
    """
    schedule: Schedule = Schedule.objects.filter(
            func='apps.bamboohr.tasks.import_employees',
            args='{},{}'.format(org_id, True)
        ).first()

    if schedule:
        schedule.delete()


def schedule_failure_emails_for_employees(org_id):
    """
    Schedule failure emails for employees who don't have email associated with them
    Runs once every week
    """

    Schedule.objects.update_or_create(
        func = 'apps.bamboohr.tasks.send_employee_email_missing_failure_notification',
        args = '{}'.format(org_id),
        defaults={
                'schedule_type': Schedule.MINUTES,
                'minutes': 7 * 24 * 60,
                'next_run': datetime.now()
        }
    )

def add_bamboo_hr_to_integrations(org):
    logger.info(f'New integration record: Fyle BambooHR Integration (HRMS) | {org.fyle_org_id = } | {org.name = }')

    Integration.objects.update_or_create(
        org_id=org.fyle_org_id,
        type='HRMS',
        defaults={
            'is_active': True,
            'org_name': org.name,
            'tpa_id': 'tpayrBcJzWAlx',
            'tpa_name': 'Fyle BambooHR Integration'
        }
    )

def deactivate_bamboo_hr_integration(org_id):
    """
    Deactivate the integration for the given org_id
    """
    try:
        org = Org.objects.get(id=org_id)
    except Org.DoesNotExist:
        logger.error(f'Did not deactivate BambooHR inetgration: Org with id {org_id} not found')

    integration = Integration.objects.filter(org_id=org.fyle_org_id, type='HRMS').first()
    if integration:
        integration.is_active=False
        integration.disconnected_at=datetime.now()
        integration.save()
        logger.info(f'Deactivated integration: Fyle BambooHR Integration (HRMS) | {org.fyle_org_id = } | {org.name = }')
    else:
        logger.error(f'Integration not found: Fyle BambooHR Integration (HRMS) | {org.fyle_org_id = } | {org.name = }')