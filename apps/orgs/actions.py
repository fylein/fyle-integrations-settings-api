
import logging
import traceback


from fyle_rest_auth.models import AuthToken
from django.conf import settings


from workato import Workato
from workato.exceptions import *

from apps.users.helpers import PlatformConnector
from apps.orgs.models import Org, FyleCredential
from apps.bamboohr.models import BambooHr


logger = logging.getLogger(__name__)
logger.level = logging.INFO


def get_admin_employees(org_id, user):

    org = Org.objects.get(pk=org_id)
    refresh_token = AuthToken.objects.get(user__user_id=user).refresh_token
    platform = PlatformConnector(refresh_token, org.cluster_domain)

    # Getting all the admin from fyle, used to send notification email
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
    

def create_connection_in_workato(connection_name, managed_user_id, data):
    connector = Workato()

    # Getting all the connection and filtering out the connection by 
    # the name to get the connection id
    connections = connector.connections.get(managed_user_id=managed_user_id)['result']
    connection_id  = next(connection for connection in connections if connection['name'] == connection_name)['id']

    # Api call for creating the connection
    connection = connector.connections.put(
        managed_user_id=managed_user_id,
        connection_id=connection_id,
        data=data
    )
    
    return connection


def create_managed_user_and_set_properties(org: Org):

    # Function for Creating a Managed user in Workato
    connector = Workato()
    org = Org.objects.get(id=org.id)
    fyle_credentials = FyleCredential.objects.get(org__id=org.id)
    
    # Payload For Creating Managed User in Workato
    workspace_data = {
        'name': org.name,
        'external_id': org.fyle_org_id,
    }
    
    if 'staging' in org.cluster_domain:
        workspace_data['name'] = 'Staging - {}'.format(org.name)
        workspace_data['origin_url'] = 'https://integrations.fyleapps.tech,http://localhost:4200'
    else:
        workspace_data['origin_url'] = 'https://integrations.fyleapps.com'

    managed_user = connector.managed_users.post(workspace_data)
    if managed_user['id']:
        org.managed_user_id = managed_user['id']
        org.save()

        # Payload for setting up Global Properties in workato to be used
        # By the fyle workato sdk
        properties_payload = {
            'properties': {
                'FYLE_CLIENT_ID': settings.FYLE_CLIENT_ID,
                'FYLE_CLIENT_SECRET': settings.FYLE_CLIENT_SECRET,
                'FYLE_BASE_URL': settings.FYLE_BASE_URL,
                'FYLE_TOKEN_URI': settings.FYLE_TOKEN_URI,
                'BASE_URI': org.cluster_domain,
                'REFRESH_TOKEN': fyle_credentials.refresh_token
            }
        }

        # Setting Up Properties in Workato, to be used by fyle sdk
        connector.properties.post(managed_user['id'], properties_payload)

    return managed_user


def handle_managed_user_exception(org: Org):

    try:
        connector = Workato()
        managed_user = connector.managed_users.get_by_id(org_id=org.fyle_org_id)
        if managed_user:
            org, _ = Org.objects.update_or_create(
                fyle_org_id=org.fyle_org_id,
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

    except NotFoundItemError as exception:
        logger.info(
            'Managed user id not found in Workato - %s',
            exception.message
        )  

    except InternalServerError as exception:
        logger.info(
            'Error while creating Workato Workspace org_id - %s in Fyle %s',
            org.id, exception.message
        )  

    except Exception:
        error = traceback.format_exc()
        logger.error(
            'Something wrong happened with org_id - %s in Fyle %s',
            org.id, error
        )  
