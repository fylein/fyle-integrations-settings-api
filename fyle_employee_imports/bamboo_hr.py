from typing import Dict
from apps.users.models import User
from apps.fyle_hrms_mappings.models import DestinationAttribute
from .base import FyleEmployeeImport
from bamboosdk.bamboohrsdk import BambooHrSDK
from apps.bamboohr.models import BambooHr, BambooHrConfiguration

from datetime import datetime
class BambooHrEmployeeImport(FyleEmployeeImport):

    def __init__(self, org_id: int, user: User):
        super().__init__(org_id, user)
        self.bamboohr = BambooHr.objects.get(org_id__in=[self.org_id])
        self.bamboohr_configuration = BambooHrConfiguration.objects.get(org_id__in=[self.org_id])
        self.bamboohr_sdk = BambooHrSDK(api_token=self.bamboohr.api_token, sub_domain=self.bamboohr.sub_domain)
    
    def get_admin_email(self):
        email_selected = self.bamboohr_configuration.emails_selected
        admin_emails = []
        for email in email_selected:
            admin_emails.append(email['email'])
        return admin_emails

    def save_employee_exported_at_time(self):
        self.bamboohr.save()
    
    def set_employee_exported_at(self):
        self.bamboohr.employee_exported_at = datetime.now()

    def get_employee_exported_at(self):
        return self.bamboohr.employee_exported_at

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
            attributes=attributes, attribute_type='EMPLOYEE', org_id=self.org_id, update=True)
        
        return []
