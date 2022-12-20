
from fyle_rest_auth.models import AuthToken

from apps.users.helpers import PlatformConnector
from apps.orgs.models import Org


def get_admin_employees(org_id, user):

    org = Org.objects.get(pk=org_id)
    refresh_token = AuthToken.objects.get(user__user_id=user).refresh_token
    platform = PlatformConnector(refresh_token, org.cluster_domain)

    employees_generator = platform.connection.v1beta.admin.employees.list_all(query_params={
        'is_enabled': 'eq.true',
        'order': 'id.desc',
        'roles': 'cs.["ADMIN"]'
    })

    admin_employees = []
    for employee in employees_generator:
        admin_employees = [
            {
             'email': employee['user']['email'],
             'name': employee['user']['full_name']
            } for employee in employee['data']
        ]
    
    return admin_employees
