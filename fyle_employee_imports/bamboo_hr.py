from typing import Dict

from apps.fyle_hrms_mappings.models import DestinationAttribute
from .base import FyleEmployeeImport
from bamboosdk.bamboohrsdk import BambooHrSDK
from apps.bamboohr.models import BambooHr


class BambooHrEmployeeImport(FyleEmployeeImport):

    def __init__(self, org_id: int, user):
        super().__init__(org_id, user)
        # bamboo_hr = BambooHr.objects.get(org_id__in=org_id)
        self.bamboohr_sdk = BambooHrSDK(api_token='864acbfb14b38f974439af49ec95bc02e52a45b9', sub_domain='baba')

    def sync_hrms_employees(self):
        employees = self.bamboohr_sdk.employees.get_all()
        self.upsert_employees(employees)

    def upsert_employees(self, employees: Dict):
        attributes = []
        for employee in employees['employees']:
            supervisor = [employee['supervisorEmail']]
            active_status = True if employee['status'] == 'Active' else False
            detail = {
                'email': employee['workEmail'] if employee['workEmail'] else None,
                'department_name': employee['department'] if employee['department'] else None,
                'full_name': employee['displayName'] if employee['displayName'] else None,
                'approver_emails': supervisor,
            }

            attributes.append({
                            'attribute_type': 'EMPLOYEE',
                            'value': employee['displayName'],
                            'destination_id': employee['id'],
                            'detail': detail,
                            'active': active_status
                    })
            
        DestinationAttribute.bulk_create_or_update_destination_attributes(
            attributes=attributes, attribute_type='EMPLOYEE', org_id=self.org_id)
        
        return []
