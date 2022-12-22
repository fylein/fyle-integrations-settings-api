
from fyle_rest_auth.models import AuthToken

from workato import Workato
from apps.users.helpers import PlatformConnector
from apps.orgs.models import Org
from apps.bamboohr.models import BambooHr


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


def handle_managed_user_exception(org_id):
    connector = Workato()
    managed_user = connector.managed_users.get_by_id(org_id=org_id)

    if managed_user:
        org, _ = Org.objects.update_or_create(
            fyle_org_id=org_id,
            defaults={
                'managed_user_id': managed_user['id']
            }
        )

        folder = connector.folders.get(managed_user_id=managed_user['id'])['result']
        if len(folder) > 0:
            BambooHr.objects.update_or_create(
                org_id=org.id,
                defaults={
                    'folder_id': folder[0]['id']
                }
            )
