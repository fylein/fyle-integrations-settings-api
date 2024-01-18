from typing import Dict
from apps.bamboohr.email import send_failure_notification_email
from apps.users.models import User
from apps.fyle_hrms_mappings.models import DestinationAttribute
from .base import FyleEmployeeImport
from bamboosdk.bamboohrsdk import BambooHrSDK
from apps.bamboohr.models import BambooHr, BambooHrConfiguration

from datetime import datetime
class BambooHrEmployeeImport(FyleEmployeeImport):

    def __init__(self, org_id: int):
        super().__init__(org_id)
        self.bamboohr_queryset = BambooHr.objects.filter(org_id__in=[self.org_id]) #using queryset to use the update method, because save method will trigger signal
        self.bamboohr = self.bamboohr_queryset.first()
        self.bamboohr_configuration = BambooHrConfiguration.objects.get(org_id__in=[self.org_id])
        self.bamboohr_sdk = BambooHrSDK(api_token=self.bamboohr.api_token, sub_domain=self.bamboohr.sub_domain)
    
    def get_admin_email(self):
        email_selected = self.bamboohr_configuration.emails_selected
        admin_emails = []
        for email in email_selected:
            admin_emails.append(email['email'])
        return admin_emails

    def save_employee_exported_at_time(self, employee_exported_at: datetime):
        self.bamboohr_queryset.update(employee_exported_at= employee_exported_at)

    def get_employee_exported_at(self):
        return self.bamboohr.employee_exported_at

    def sync_hrms_employees(self):
        employees = self.bamboohr_sdk.employees.get_all()
        self.upsert_employees(employees)
    
    def sync_with_webhook(self, employee):
        employee_payload = []
        employee_approver_payload = []

        full_name = employee['firstName'] + ' ' + employee['lastName']

        if not employee.get('workEmail'):
            admin_email = self.get_admin_email()
            incomplete_employee = {'name': full_name, 'id': employee['id']}
            send_failure_notification_email(employees=[incomplete_employee], number_of_employees=1, admin_email=admin_email)
            return
        if employee.get('supervisorEId'):
            response = self.bamboohr_sdk.employees.get(employee['supervisorEId'])
            email = response['workEmail']
            fyle_employee = self.platform_connection.get_employee_by_email(email=email)
            if len(fyle_employee):
                employee_approver_payload.append({
                    'user_email': employee['workEmail'],
                    'approver_emails': [email]
                    }
                )
    
        update_create_employee_payload = {
            'user_email': employee['workEmail'],
            'user_full_name': full_name,
            'code': employee['id'],
            'department_name': employee['department'] if employee['department'] else '',
            'is_enabled': employee['status']
        }
        employee_payload.append(update_create_employee_payload)
        if employee['department']:
            existing_departments = self.get_existing_departments_from_fyle()
            department_payload = self.create_fyle_department_payload(existing_departments, [employee['department']])
            if department_payload:
                self.platform_connection.post_department(department_payload[0])

        self.platform_connection.bulk_post_employees(employees_payload=employee_payload)
        if employee_approver_payload:
            self.platform_connection.bulk_post_employees(employees_payload=employee_approver_payload)


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
