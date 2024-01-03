from typing import Dict
from apps.users.models import User
from apps.fyle_hrms_mappings.models import DestinationAttribute
from .base import FyleEmployeeImport
from bamboosdk.bamboohrsdk import BambooHrSDK
from apps.bamboohr.models import BambooHr


class BambooHrEmployeeImport(FyleEmployeeImport):

    def __init__(self, org_id: int, user: User):
        super().__init__(org_id, user)
        self.bamboohr_sdk = BambooHrSDK(api_token=self.bamboohr.api_token, sub_domain=self.bamboohr.sub_domain)

    def sync_hrms_employees(self):
        employees = self.bamboohr_sdk.employees.get_all()
        self.upsert_employees(employees)

    def upsert_employees(self, employees: Dict):
        attributes = []
        for employee in employees['employees']:
            supervisor = [employee.get('supervisorEmail', None)]
            active_status = True if employee.get('status', None) == 'Active' else False

            display_name = employee.get('displayName', None)
            if not display_name:
                display_name = employee['firstName'] + ' ' + employee['lastName']
    
            detail = {
                'email': employee.get('workEmail', None),
                'department_name': employee.get('department', None),
                'full_name': display_name,
                'approver_emails': supervisor,
            }

            attributes.append({
                'attribute_type': 'EMPLOYEE',
                'value': display_name,
                'destination_id': employee['id'],
                'detail': detail,
                'active': active_status
                })
            
        DestinationAttribute.bulk_create_or_update_destination_attributes(
            attributes=attributes, attribute_type='EMPLOYEE', org_id=self.org_id, update=True)
        
        return []
