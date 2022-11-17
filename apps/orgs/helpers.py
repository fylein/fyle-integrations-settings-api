import logging
from django.conf import settings

from apps.orgs.models import FyleCredential, Org
from workato.workato import Workato

logger = logging.getLogger(__name__)
logger.level = logging.INFO

def create_workato_workspace(org):
    connector = Workato()
    workspace_data = {
        "name": org.name,
        "external_id": org.fyle_org_id,
        "notification_email": org.user.first().email
    }

    managed_user = connector.managed_users.post(workspace_data)
    fyle_credentials = FyleCredential.objects.get(org_id=org.id)
    if managed_user:
        org = Org.objects.get(id=org.id)
        org.managed_user_id = managed_user['id']
        org.save()

        properties_payload = {
            "properties": {
                "FYLE_CLIENT_ID": settings.FYLE_CLIENT_ID,
                "FYLE_CLIENT_SECRET": settings.FYLE_CLIENT_SECRET,
                "FYLE_BASE_URL": settings.FYLE_BASE_URL,
                "REFRESH_TOKEN": fyle_credentials.refresh_token
            }
        }

        connector.properties.post(managed_user['id'], properties_payload)
        created_folder = connector.folders.post(managed_user['id'], 'Bamboo HR')
        connector.packages.post(managed_user['id'], created_folder['id'], 'assets/package.zip')

        return managed_user
