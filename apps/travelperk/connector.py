import logging
from django.conf import settings


from apps.travelperk.models import TravelperkCredential, TravelPerk
from connectors.travelperk import Travelperk


logger = logging.getLogger(__name__)


class TravelperkConnector:
    """
    Travelperk Connector Class
    """
    
    def __init__(self, credentials_object: TravelperkCredential, org_id: int):
        
        client_id = settings.TRAVELPERK_CLIENT_ID
        client_secret = settings.TRAVELPERK_CLIENT_SECRET
        environment = 'sandbox'
        refresh_token = credentials_object.refresh_token

        self.connection = Travelperk(client_id, client_secret, refresh_token, environment)
        self.org_id = org_id
        
        credentials_object.refresh_token = self.connection.refresh_token
        credentials_object.save()


    def create_webhook(self, data: dict):
        """
        Create Webhook in Travelperk
        :param data: Webhook Data
        :return: Webhook Data
        """

        response = self.connection.webhooks.create(data)
        if response:
            TravelPerk.objects.update_or_create(
                org_id=self.org_id,
                defaults={
                    'webhook_subscription_id': response['id'],
                    'webhook_enabled': response['enabled']
                }
            )

        return response

