from typing import Dict
from apps.fyle_hrms_mappings.models import DestinationAttribute
from apps.orgs.models import Org
from apps.users.helpers import PlatformConnector
from fyle_rest_auth.models import AuthToken

class FyleEmployeeImport():

    def __init__(self, org_id: int, user):
        self.org_id = org_id
        self.user = user
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
        departments_generator = self.platform_connection.get_departments(query_params=query_params)
        for response in departments_generator:
            if response.get('data'):
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

    def get_employee_and_approver_payload(self):
        pass

    def import_employees(self):
        pass

    def sync_hrms_employees(self):
        raise NotImplementedError('Implement sync_hrms_employees() in the child class')
    
    def sync_employees(self):
        self.sync_fyle_employees()
        self.sync_hrms_employees()

        hrms_employees = DestinationAttribute.objects.filter(
        attribute_type='EMPLOYEE',
        org_id=self.org_id
        ).order_by('value', 'id')

        self.import_departments(hrms_employees)
