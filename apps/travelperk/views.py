import logging
import traceback
import hmac
import hashlib
import json
from django.conf import settings
from django.db import transaction
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status


from apps.orgs.models import Org
from apps.travelperk.serializers import TravelperkSerializer
from apps.travelperk.models import TravelPerk, TravelPerkConfiguration, TravelperkCredential, Invoice, InvoiceLineItem
from apps.travelperk.connector import TravelperkConnector
from apps.orgs.exceptions import handle_fyle_exceptions

from .actions import create_expense_in_fyle
from .helpers import get_refresh_token_using_auth_code

logger = logging.getLogger(__name__)
logger.level = logging.INFO


class TravelperkView(generics.ListAPIView):
    serializer_class = TravelperkSerializer

    def get(self, request, *args, **kwargs):
        try:
            travelperk = TravelPerk.objects.get(org_id__in=[kwargs['org_id']])

            return Response(
                data=TravelperkSerializer(travelperk).data,
                status=status.HTTP_200_OK
            )
        except TravelPerk.DoesNotExist:
            return Response(
                data={'message': 'Travelperk Not Found'},
                status=status.HTTP_404_NOT_FOUND
            )


class DisconnectTravelperkView(generics.CreateAPIView):
    """
    Api call to Disconnect Travelperk Connection
    """
    
    def post(self, request, *args, **kwargs):
        try:
            travelperk = TravelPerk.objects.filter(org=kwargs['org_id']).first()
            travelperk_creds = TravelperkCredential.objects.filter(org=kwargs['org_id']).first()

            travelperk_connector = TravelperkConnector(travelperk_creds, kwargs['org_id'])
            travelperk_connector.delete_webhook_connection(travelperk.webhook_subscription_id)

            travelperk.webhook_subscription_id = None
            travelperk.is_travelperk_connected = False
            travelperk.save()

            return Response(
                data={'message': 'disconnected successfully'},
                status=status.HTTP_200_OK
            )
        
        except TravelPerk.DoesNotExist:
            return Response(
                data={'message': 'no travelperk connection found'},
                status=status.HTTP_404_NOT_FOUND
            )


class ConnectTravelperkView(generics.CreateAPIView):
    """
    Api Call to make Travelperk Connection
    """
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):

        try:
            org = Org.objects.get(id=kwargs['org_id'])
            refresh_token = get_refresh_token_using_auth_code(request.data.get('code'), kwargs['org_id'])
            
            if refresh_token:
                travelperk_credential = TravelperkCredential.objects.get(org=org)
                travelperk_connection = TravelperkConnector(travelperk_credential, kwargs['org_id'])

                travelperk_webhook_data = {
                    'name': 'travelperk webhook invoice',
                    'url': settings.API_URL + '/orgs/{}/travelperk/travelperk_webhook/'.format(kwargs['org_id']),
                    'secret': settings.TKWEBHOOKS_SECRET,
                    'events': [
                        'invoice.issued'
                    ]
                }

                created_webhook = travelperk_connection.create_webhook(travelperk_webhook_data)
                TravelPerk.objects.update_or_create(
                    org=org,
                    defaults={
                        'webhook_id': created_webhook['id'],
                        'is_travelperk_connected': True
                    }
                )

                return Response(
                    data=created_webhook,
                    status=status.HTTP_200_OK
                )

        except Exception:
            error = traceback.format_exc()
            logger.error(error)

            return Response(
                data='Something went wrong while connecting to travelperk',
                status=status.HTTP_400_BAD_REQUEST
            )


class TravelperkWebhookAPIView(generics.CreateAPIView):
    
    authentication_classes = []
    permission_classes = []

    @handle_fyle_exceptions()
    def create(self, request, *args, **kwargs):
        
        payload = request.data
        secret = settings.TKWEBHOOKS_SECRET
        signature = hmac.new(secret.encode(), json.dumps(payload).encode(), hashlib.sha256).hexdigest()

        if signature != request.META['HTTP_TK_WEBHOOK_HMAC_SHA256']:
            return Response(
                data={
                    'message': 'Invalid Signature'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            # Custom processing of the webhook event data
            with transaction.atomic():
                # Extract invoice line items from the request data
                logger.info("webhook data: {}".format(request.data))
                invoice_lineitems_data = request.data.pop('lines')

                # Create or update Invoice and related line items
                invoice = Invoice.create_or_update_invoices(request.data)
                invoice_linteitmes = InvoiceLineItem.create_or_update_invoice_lineitems(invoice_lineitems_data, invoice)

            create_expense_in_fyle(kwargs['org_id'], invoice, invoice_linteitmes)

            return Response(
                data={
                    'message': 'expenses created successfully'
                },
                status=status.HTTP_200_OK
            )
