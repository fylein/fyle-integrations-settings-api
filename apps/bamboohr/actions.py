import json
from time import sleep
from workato import Workato

from django.conf import settings

from apps.orgs.models import Org
from apps.orgs.exceptions import handle_workato_exception
from apps.bamboohr.models import BambooHr, BambooHrConfiguration
from apps.names import BAMBOO_HR

@handle_workato_exception(task_name = 'Disconnect BambooHR')
def disconnect_bamboohr(org_id, configuration:BambooHrConfiguration, bamboohr: BambooHr):
    org = Org.objects.get(id=org_id)

    connector = Workato()
    connections = connector.connections.get(managed_user_id=org.managed_user_id)['result']
    bamboo_connection_1 = next(connection for connection in connections if connection['name'] == BAMBOO_HR['connections'][0])
    bamboo_connection_2 = next(connection for connection in connections if connection['name'] == BAMBOO_HR['connections'][1])

    configuration.recipe_status = False
    configuration.save()

    connection = connector.connections.post(
        managed_user_id=org.managed_user_id,
        connection_id=bamboo_connection_1['id'],

    )
    connector.connections.post(
        managed_user_id=org.managed_user_id,
        connection_id=bamboo_connection_2['id'],
    )

    bamboohr.api_token = None
    bamboohr.sub_domain = None
    bamboohr.save()

    return connection

@handle_workato_exception(task_name = 'Sync Employees of BambooHR')
def sync_employees(org_id, config: BambooHrConfiguration):
    org = Org.objects.get(id = org_id)
    recipes = connector.recipes.get(managed_user_id=org.managed_user_id)['result']
    sync_recipe = next(recipe for recipe in recipes if recipe['name'] == BAMBOO_HR['recipe'])
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
            "name": sync_recipe['name'],
            "code": sync_recipe['code'],
            "folder_id": str(sync_recipe['folder_id'])
        }
    }
    connector = Workato()
    connector.recipes.post(org.managed_user_id, sync_recipe['id'], payload)
    connector.recipes.post(org.managed_user_id, sync_recipe['id'], None, 'start')
    sleep(5)
    connector.recipes.post(org.managed_user_id, sync_recipe['id'], None, 'stop')

    return sync_recipe