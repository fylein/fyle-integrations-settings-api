from apps.bamboohr.models import BambooHr
from apps.fyle_hrms_mappings.models import DestinationAttribute
from apps.orgs.models import FyleCredential, Org
from apps.users.helpers import PlatformConnector
from fyle_employee_imports.bamboo_hr import BambooHrEmployeeImport
from bamboosdk.bamboohrsdk import BambooHrSDK
from django_q.models import Schedule

from datetime import datetime

def refresh_employees(org_id: int, schedule: bool = False):
    """
        Sync Employees from BambooHR to Fyle
    """
    bamboohr_importer = BambooHrEmployeeImport(org_id=org_id)
    bamboohr_importer.sync_employees(schedule=schedule)

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

def schedule_sync_employees(org_id):
    """
    Create schedule to sync employees every 6 hours
    """
    Schedule.objects.update_or_create(
        func = 'apps.bamboohr.tasks.refresh_employees',
        args = '{},{}'.format(org_id, True),
        defaults={
                'schedule_type': Schedule.MINUTES,
                'minutes': 6 * 60,
                'next_run': datetime.now()
        }
    )

def delete_sync_employee_schedule(org_id):
    """
    Delete schedule when bamboohr is disconnected
    """
    schedule: Schedule = Schedule.objects.filter(
            func='apps.bamboohr.tasks.refresh_employees',
            args='{},{}'.format(org_id, True)
        ).first()

    if schedule:
        schedule.delete()
