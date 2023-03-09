from django.conf import settings
from workato import Workato

def set_gusto_properties(managed_user_id):

    # Function for Creating a Managed user in Workato
    connector = Workato()
    # Payload for setting up Global Properties in workato to be used
    # By the fyle workato sdk
    properties_payload = {
        'properties': {
            'GUSTO_CLIENT_ID': settings.GUSTO_CLIENT_ID,
            'GUSTO_CLIENT_SECRET': settings.GUSTO_CLIENT_SECRET,
            'GUSTO_ENVIRONMENT': settings.GUSTO_ENVIRONMENT
        }
    }

    # Setting Up Properties in Workato, to be used by fyle sdk
    connector.properties.post(managed_user_id, properties_payload)
