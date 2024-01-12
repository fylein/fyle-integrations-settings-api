from typing import Dict, List
from datetime import datetime

from apps.bamboohr.models import BambooHr, BambooHrConfiguration
from apps.fyle_hrms_mappings.models import DestinationAttribute, ExpenseAttribute
from apps.orgs.models import FyleCredential, Org
from apps.users.helpers import PlatformConnector
from fyle_rest_auth.models import AuthToken

from apps.bamboohr.email import send_failure_notification_email
from django.conf import settings

class FyleEmployeeImport():

    def __init__(self, org_id: int):
        self.org_id = org_id
        org = Org.objects.get(id=self.org_id)
        cluster_domain = org.cluster_domain
        refresh_token = FyleCredential.objects.get(org=org).refresh_token
        self.platform_connection = PlatformConnector(refresh_token, cluster_domain)
    
    def sync_fyle_employees(self):
        self.platform_connection.sync_employees(org_id=self.org_id)

    def get_existing_departments_from_fyle(self):
        existing_departments: Dict = {}
        query_params={
            'order': 'id.desc'
        }
        departments_generator = self.platform_connection.get_department_generator(query_params=query_params)
        for response in departments_generator:
            for department in response['data']:
                existing_departments[department['display_name']] = {
                    'id': department['id'],
                    'is_enabled': department['is_enabled']
                }
        return existing_departments

    def create_fyle_department_payload(self, existing_departments, new_departments):
        departments_payload = []

        for department in new_departments:
            if department in existing_departments.keys():
                if not existing_departments[department]['is_enabled']:
                    departments_payload.append({
                    'name': department,
                    'id': existing_departments[department]['id'],
                    'is_enabled': True,
                    'display_name': department
                })
            else:
                departments_payload.append({
                'name': department,
                'display_name': department
            })
        
        return departments_payload

    def departments_to_be_imported(self, hrms_employees):
        new_departments = []

        for employee in hrms_employees:
            if employee.detail['department_name']:
                new_departments.append(employee.detail['department_name'])
        
        return list(set(new_departments))

    def post_department(self, departments_payload):
        for department in departments_payload:
            self.platform_connection.post_department(department)

    def import_departments(self, hrms_employees):
        existing_departments = self.get_existing_departments_from_fyle()
        new_departments = self.departments_to_be_imported(hrms_employees)
        departments_payload = self.create_fyle_department_payload(existing_departments, new_departments)
        self.post_department(departments_payload)

    def get_employee_and_approver_payload(self, hrms_employees, webhook_call):
        employee_payload: List[Dict] = []
        employee_emails: List[str] = []
        approver_emails: List[str] = []
        employee_approver_payload: List[Dict] = []
        incomplete_employees: List = []
        incomplete_employee_count: int = 0

        for employee in hrms_employees:
            if employee.detail['email']:
                update_create_employee_payload = {
                    'user_email': employee.detail['email'],
                    'user_full_name': employee.detail['full_name'],
                    'code': employee.destination_id,
                    'department_name': employee.detail['department_name'] if employee.detail['department_name'] else '',
                    'is_enabled': employee.active
                }
                employee_payload.append(update_create_employee_payload)
                employee_emails.append(employee.detail['email'])

                if employee.detail['approver_emails']:
                    employee_approver_payload.append({
                        'user_email': employee.detail['email'],
                        'approver_emails': employee.detail['approver_emails']
                    })
                    approver_emails.extend(employee.detail['approver_emails'])
            else:
                incomplete_employee_count += 1
                incomplete_employees.append({'name': employee.detail['full_name'], 'id':employee.destination_id})
        
        admin_email = self.get_admin_email()
        if incomplete_employee_count > 0:
            send_failure_notification_email(employees=incomplete_employees, number_of_employees=incomplete_employee_count, admin_email=admin_email)

        existing_approver_emails = ExpenseAttribute.objects.filter(
            org_id=self.org_id, attribute_type='EMPLOYEE', value__in=approver_emails
        ).values_list('value', flat=True)

        employee_approver_payload = list(filter(
            lambda employee_approver: set(
                employee_approver['approver_emails']
            ).issubset(employee_emails) or set(
                employee_approver['approver_emails']
            ).issubset(existing_approver_emails),
            employee_approver_payload
        ))

        return employee_payload, employee_approver_payload

    def fyle_employee_import(self, hrms_employees, webhook_call = False):
        fyle_employee_payload, employee_approver_payload = self.get_employee_and_approver_payload(hrms_employees, webhook_call=webhook_call)

        employee_exported_at_time = self.get_employee_exported_at()

        if fyle_employee_payload:
            self.platform_connection.bulk_post_employees(employees_payload=fyle_employee_payload)

            employee_exported_at_time = datetime.now()

        if employee_approver_payload:
            self.platform_connection.bulk_post_employees(employees_payload=employee_approver_payload)
            
            employee_exported_at_time = datetime.now()
        
        self.save_employee_exported_at_time(employee_exported_at = employee_exported_at_time)
        self.platform_connection.sync_employees(org_id=self.org_id)

    def sync_hrms_employees(self):
        raise NotImplementedError('Implement sync_hrms_employees() in the child class')
    
    def get_admin_email(self):
        raise NotImplementedError('Implement get_admin_email() in the child class')

    def set_employee_exported_at(self):
        raise NotImplementedError('Implement set_employee_exported_at() in the child class')

    def get_employee_exported_at(self):
        raise NotImplementedError('Implement get_employee_exported_at() in the child class')

    def save_employee_exported_at_time(self, employee_exported_at):
        raise NotImplementedError('Implement save_hrms() in the child class') 

    def sync_employees(self):
        self.sync_fyle_employees()
        self.sync_hrms_employees()

        hrms_employees = DestinationAttribute.objects.filter(
            attribute_type='EMPLOYEE',
            org_id=self.org_id,
            updated_at__gte=self.get_employee_exported_at(),
        ).order_by('value', 'id')

        self.import_departments(hrms_employees)
        self.fyle_employee_import(hrms_employees)
