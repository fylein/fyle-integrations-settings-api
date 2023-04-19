import json
from time import sleep
from workato import Workato

from django.conf import settings

from apps.orgs.models import Org
from apps.orgs.exceptions import handle_workato_exception
from apps.gusto.models import Gusto, GustoConfiguration
from apps.names import GUSTO
from django.conf import settings
from apps.orgs.actions import upload_properties

def set_gusto_properties(managed_user_id: str):

    # Payload for setting up Global Properties in workato to be used
    # By the gusto workato sdk
    properties_payload = {
        'properties': {
            'GUSTO_CLIENT_ID': settings.GUSTO_CLIENT_ID,
            'GUSTO_CLIENT_SECRET': settings.GUSTO_CLIENT_SECRET,
            'GUSTO_ENVIRONMENT': settings.GUSTO_ENVIRONMENT
        }
    }
    upload_properties(managed_user_id, properties_payload)

@handle_workato_exception(task_name = 'Create Gusto Connection')
def create_gusto_connection(org_id):
    org = Org.objects.get(id=org_id)
    gusto = Gusto.objects.get(org_id=org_id)
    connector = Workato()
    # Creating gusto Connection In Workato
    connections = connector.connections.get(managed_user_id=org.managed_user_id)['result']
    connection_id  = next(connection for connection in connections if connection['name'] == GUSTO['connection'])['id']

    gusto.connection_id = connection_id
    gusto.save()
    return connection_id

@handle_workato_exception(task_name='Sync Employees in Gusto')
def sync_employees(org_id):
    connector = Workato()
    org = Org.objects.get(id=org_id)
    config = GustoConfiguration.objects.get(org__id=org_id)
    recipes = connector.recipes.get(managed_user_id=org.managed_user_id)['result']
    sync_recipe = next(recipe for recipe in recipes if recipe['name'] == GUSTO['recipe'])
    code = json.loads(sync_recipe['code'])
    admin_emails = [
        {
            'email': admin['email'],
        } for admin in config.emails_selected
    ]
    code['block'][6]['block'][1]['input']['personalizations']['to'] = admin_emails
    code['block'][6]['block'][1]['input']['from']['email'] = settings.SENDGRID_EMAIL
    sync_recipe['code'] = json.dumps(code)
    payload = {
        "recipe": {
            "code": sync_recipe['code'],
        }
    }

    connector.recipes.post(org.managed_user_id, sync_recipe['id'], payload)
    connector.recipes.post(org.managed_user_id, sync_recipe['id'], None, 'start')
    return sync_recipe

