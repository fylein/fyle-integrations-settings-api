from apps.bamboohr.models import BambooHr
from apps.fyle_hrms_mappings.models import DestinationAttribute
from apps.orgs.models import FyleCredential, Org
from apps.users.helpers import PlatformConnector
from fyle_employee_imports.bamboo_hr import BambooHrEmployeeImport
from bamboosdk.bamboohrsdk import BambooHrSDK

def refresh_employees(org_id: int):
    """
        Sync Employees from BambooHR to Fyle
    """
    bamboohr_importer = BambooHrEmployeeImport(org_id=org_id)
    bamboohr_importer.sync_employees()

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
