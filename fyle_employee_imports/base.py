from typing import Dict, List
from datetime import datetime

from apps.bamboohr.models import BambooHr, BambooHrConfiguration
from apps.fyle_hrms_mappings.models import DestinationAttribute, ExpenseAttribute
from apps.orgs.models import Org
from apps.users.helpers import PlatformConnector
from fyle_rest_auth.models import AuthToken

from apps.bamboohr.email import send_failure_notification_email
from django.conf import settings

class FyleEmployeeImport():

    def __init__(self, org_id: int, user):
        self.org_id = org_id
        self.user = user
        self.bamboohr = BambooHr.objects.get(org_id__in=[self.org_id])
        self.bamboohr_configuration = BambooHrConfiguration.objects.get(org_id__in=[self.org_id])
        refresh_token = AuthToken.objects.get(user__user_id=self.user).refresh_token
        cluster_domain = Org.objects.get(user__user_id=self.user).cluster_domain
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

    def get_employee_and_approver_payload(self, hrms_employees):
        employee_payload: List[Dict] = []
        employee_emails: List[str] = []
        approver_emails: List[str] = []
        employee_approver_payload: List[Dict] = []
        unimported_employees: List = []
        no_unimported_employees: int = 0

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
                no_unimported_employees += 1
                unimported_employees.append({'name': employee.detail['full_name'], 'id':employee.destination_id})
        
        admin_email = self.bamboohr_configuration.additional_email_options['admin_email']
        send_failure_notification_email(employees=unimported_employees, number_of_employees=no_unimported_employees, admin_email=admin_email)

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

    def fyle_employee_import(self, hrms_employees):
        fyle_employee_payload, employee_approver_payload = self.get_employee_and_approver_payload(hrms_employees)

        if fyle_employee_payload:
            self.platform_connection.bulk_post_employees(employees_payload=fyle_employee_payload)

            self.bamboohr.employee_exported_at = datetime.now()

        if employee_approver_payload:
            self.platform_connection.bulk_post_employees(employees_payload=employee_approver_payload)
            
            self.bamboohr.employee_exported_at = datetime.now()
        
        self.bamboohr.save()
        self.platform_connection.sync_employees(org_id=self.org_id)

    def sync_hrms_employees(self):
        raise NotImplementedError('Implement sync_hrms_employees() in the child class')
    
    def sync_employees(self):
        self.sync_fyle_employees()
        self.sync_hrms_employees()

        hrms_employees = DestinationAttribute.objects.filter(
            attribute_type='EMPLOYEE',
            org_id=self.org_id,
            updated_at__gte=self.bamboohr.employee_exported_at,
        ).order_by('value', 'id')

        self.import_departments(hrms_employees)
        self.fyle_employee_import(hrms_employees)
