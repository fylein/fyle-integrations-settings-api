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
