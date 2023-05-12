from workato import Workato

from apps.orgs.models import Org
from apps.orgs.exceptions import handle_workato_exception
from apps.travelperk.models import TravelPerk
from apps.names import TRAVELPERK


@handle_workato_exception(task_name = 'Travelperk Connection')
def connect_travelperk(org_id):
    connector = Workato()
    org = Org.objects.get(id=org_id)
    travelperk = TravelPerk.objects.get(org_id=org.id)
    connections = connector.connections.get(managed_user_id=org.managed_user_id)['result']
    connection_id = next(connection for connection in connections if connection['name'] == TRAVELPERK['connection'])['id']

    travelperk.travelperk_connection_id = connection_id
    travelperk.save()
    return connection_id
