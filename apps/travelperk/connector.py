import logging
from django.conf import settings


from apps.travelperk.models import TravelperkCredential
from connectors.travelperk.core.client import Travelperk


logger = logging.getLogger(__name__)


class TravelperkConnector:
    """
    Travelperk Connector Class
    """
    
    def __init__(self, credentials_object: TravelperkCredential, org_id: int):
        
        client_id = settings.TRAVELPERK_CLIENT_ID
        client_secret = settings.TRAVELPERK_CLIENT_SECRET
        environment = settings.TRAVELPERK_ENVIRONMENT
        refresh_token = credentials_object.refresh_token
        
        self.connection = Travelperk(client_id, client_secret, refresh_token, environment)
        self.org_id = org_id
        
        credentials_object.refresh_token = self.connection.refresh_token
        credentials_object.save()
