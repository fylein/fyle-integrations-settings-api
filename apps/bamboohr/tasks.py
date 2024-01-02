from apps.bamboohr.models import BambooHr
from apps.fyle_hrms_mappings.models import DestinationAttribute
from fyle_employee_imports.bamboo_hr import BambooHrEmployeeImport
from apps.users.models import User

def refresh_employees(org_id: int, user: User):
    """
        Sync Employees from BambooHR to Fyle
    """
    bambooHrImporter = BambooHrEmployeeImport(org_id=org_id, user=user)
    bambooHrImporter.sync_employees()

def update_employee(org_id: int, user: User, payload: dict):

    """
        Update employee in fyle when employee in Bamboohr is added or updated
    """
    bamboohr = BambooHr.objects.get(org_id__in=[org_id], is_credentials_expired=False)
    bamboohr_importer = BambooHrEmployeeImport(org_id=org_id, user=user)

    employee_payload = {'employees': []}
    payload = payload['employees'][0]
    employee = {}
    employee['id'] = payload['id']
    employee['firstName'] = payload['fields']['firstName']['value']
    employee['lastName'] = payload['fields']['lastName']['value']
    for field in payload['changedFields']:
        employee[field] = payload['fields'][field]['value']

    employee_payload['employees'].append(employee)

    bamboohr_importer.upsert_employees(employees=employee_payload)

    hrms_employees = DestinationAttribute.objects.filter(
            attribute_type='EMPLOYEE',
            org_id=org_id,
            updated_at__gte=bamboohr.employee_exported_at,
        ).order_by('value', 'id')
    bamboohr_importer.import_departments(hrms_employees=hrms_employees)
    bamboohr_importer.fyle_employee_import(hrms_employees=hrms_employees)
