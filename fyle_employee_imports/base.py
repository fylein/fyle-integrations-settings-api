from apps.orgs.models import Org
from apps.users.helpers import PlatformConnector
from fyle_rest_auth.models import AuthToken

class FyleEmployeeImport():

    def __init__(self, org_id: int, user):
        self.org_id = org_id
        self.user = user
    
    def sync_fyle_employees(self):
        
        refresh_token = AuthToken.objects.get(user__user_id=self.user).refresh_token
        cluster_domain = Org.objects.get(user__user_id=self.user).cluster_domain
        platform_connection = PlatformConnector(refresh_token, cluster_domain)
        platform_connection.sync_employees(org_id=self.org_id)

    def get_existing_departments_from_fyle(self):
        pass

    def create_fyle_department_payload(self):
        pass

    def departments_to_be_imported(self):
        pass

    def post_department(self):
        pass

    def import_departments(self):
        pass

    def get_employee_and_approver_payload(self):
        pass

    def import_employees(self):
        pass

    def sync_hrms_employees(self):
        raise NotImplementedError('Implement sync_hrms_employees() in the child class')
    
    def sync_employees(self):
        self.sync_fyle_employees()
        self.sync_hrms_employees()

