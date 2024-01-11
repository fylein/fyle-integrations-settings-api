from apps.bamboohr.models import BambooHr
from apps.fyle_hrms_mappings.models import DestinationAttribute
from apps.orgs.models import FyleCredential, Org
from apps.users.helpers import PlatformConnector
from fyle_employee_imports.bamboo_hr import BambooHrEmployeeImport

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
    bamboohr = BambooHr.objects.get(org_id__in=[org_id], is_credentials_expired=False)
    bamboohr_importer = BambooHrEmployeeImport(org_id=org_id)
    employee_payload = {'employees': []}
    payload = payload['employees'][0]
    employee = {}
    employee['id'] = payload['id']
    employee['firstName'] = payload['fields']['firstName']['value']
    employee['lastName'] = payload['fields']['lastName']['value']
    for field in payload['changedFields']:  
        employee[field] = payload['fields'][field]['value']

    if not employee.get('status', None):
        employee['status'] = True

    employee_payload['employees'].append(employee)

    bamboohr_importer.upsert_employees(employees=employee_payload, webhook_update=True)

    hrms_employees = DestinationAttribute.objects.filter(
            attribute_type='EMPLOYEE',
            org_id=org_id,
            updated_at__gte=bamboohr.employee_exported_at,
        ).order_by('value', 'id')
    bamboohr_importer.import_departments(hrms_employees=hrms_employees)
    bamboohr_importer.fyle_employee_import(hrms_employees=hrms_employees, webhook_call=True)
