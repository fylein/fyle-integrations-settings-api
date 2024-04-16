import logging
from django.conf import settings


from apps.travelperk.models import TravelperkCredential, TravelPerk, TravelperkProfileMapping
from connectors.travelperk import Travelperk


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


    def delete_webhook_connection(self, webhook_subscription_id: str):
        """
        Delete Webhook in Travelperk
        :param webhook_subscription_id: Webhook Id
        :return: Dict
        """

        response = self.connection.webhooks.delete(webhook_subscription_id)        
        return response


    def sync_invoice_profile(self):
        """
        Sync Invoice Profile
        :return: Dict
        """

        response = self.connection.invoice_profiles.get_all()
        for invoice_profile in response:
            country_name = invoice_profile['billing_information']['country_name'] if 'country_name' in invoice_profile['billing_information'] else None
            currency = invoice_profile['currency'] if 'currency' in invoice_profile else None
            TravelperkProfileMapping.objects.update_or_create(
                org_id=self.org_id,
                profile_name=invoice_profile['name'],
                source_id=invoice_profile['id'],
                defaults={
                    'country': country_name,
                    'currency': currency,
                }
            )

        return response
