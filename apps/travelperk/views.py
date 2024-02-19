import logging
import traceback
import hmac
import hashlib
import json
from typing import Dict, List
from django.conf import settings
from django.db import transaction

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from django_q.tasks import async_task

from admin_settings.utils import LookupFieldMixin

from apps.orgs.models import Org, FyleCredential

from apps.travelperk.serializers import (
    TravelperkSerializer, 
    TravelperkProfileMappingSerializer, 
    SyncPaymentProfileSerializer, 
    TravelperkAdvancedSettingSerializer
)

from apps.travelperk.models import (
    TravelPerk, 
    TravelperkCredential, 
    Invoice, 
    InvoiceLineItem, 
    TravelperkProfileMapping, 
    TravelperkAdvancedSetting
)
from apps.travelperk.connector import TravelperkConnector
from apps.orgs.exceptions import handle_fyle_exceptions
from apps.travelperk.helpers import get_refresh_token_using_auth_code
from apps.users.helpers import PlatformConnector

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
                    'url':  settings.API_URL + '/orgs/{}/travelperk/travelperk_webhook/'.format(kwargs['org_id']),
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
                        'is_travelperk_connected': True,
                        'onboarding_state': 'PAYMENT_PROFILE_SETTINGS'
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
                invoice = Invoice.create_or_update_invoices(request.data, kwargs['org_id'])
                invoice_linteitmes = InvoiceLineItem.create_or_update_invoice_lineitems(invoice_lineitems_data, invoice)

            if invoice and invoice_linteitmes:
                async_task('apps.travelperk.actions.create_expense_in_fyle', kwargs['org_id'], invoice, invoice_linteitmes)

        return Response(
            data={
                'message': 'expenses created successfully'
            },
            status=status.HTTP_200_OK
        )


class AdvancedSettingView(generics.CreateAPIView, generics.RetrieveAPIView):
    """
    Retrieve or Create Advanced Settings
    """

    serializer_class = TravelperkAdvancedSettingSerializer
    lookup_field = 'org_id'
    lookup_url_kwarg = 'org_id'

    queryset = TravelperkAdvancedSetting.objects.all()


class TravelperkPaymentProfileMappingView(LookupFieldMixin, generics.ListCreateAPIView):
    """
    API Call to store payment profile mapping
    """

    serializer_class = TravelperkProfileMappingSerializer
    queryset = TravelperkProfileMapping.objects.all()

    def post(self, request, *args, **kwargs):

        try:
            mappings: List[Dict] = request.data

            travelperk_profile_mapping = TravelperkProfileMapping.bulk_create_profile_mappings(
                mappings=mappings,
                org_id=kwargs['org_id']
            )
                        
            travelperk = TravelPerk.objects.filter(org_id=kwargs['org_id']).first()
            if travelperk.onboarding_state == 'PAYMENT_PROFILE_SETTINGS':
                travelperk.onboarding_state = 'ADVANCED_SETTINGS'
                travelperk.save()

            return Response(data=self.serializer_class(travelperk_profile_mapping, many=True).data, status=status.HTTP_200_OK)

        except Exception as exception:
            logger.error(exception)
            return Response(
                data=exception,
                status=status.HTTP_400_BAD_REQUEST
            )


class AdvancedSettingView(generics.CreateAPIView, generics.RetrieveAPIView):
    """
    Retrieve or Create Advanced Settings
    """

    serializer_class = TravelperkAdvancedSettingSerializer
    queryset = TravelperkAdvancedSetting.objects.all()

    lookup_field = 'org_id'
    lookup_url_kwarg = 'org_id'

    
    def get_object(self):
        # Retrieve the value from the request
        org_id = self.kwargs['org_id']
        org = Org.objects.filter(id=org_id).first()

        # Attempt to retrieve the object based on the given condition
        advanced_settings, created = TravelperkAdvancedSetting.objects.get_or_create(org_id=org_id)
        if not advanced_settings.default_employee_name:
            fyle_credentials = FyleCredential.objects.filter(org_id=org_id).first()
            platform_connector = PlatformConnector(fyle_credentials.refresh_token, org.cluster_domain)

            user_profile = platform_connector.connection.v1beta.spender.my_profile.get()
            advanced_settings.default_employee_name = user_profile['data']['user']['email']
            advanced_settings.default_employee_id = user_profile['data']['user']['id']

        # If the object was created, return 201 Created status code
        if created:
            self.status_code = status.HTTP_201_CREATED
        else:
            self.status_code = status.HTTP_200_OK

        return advanced_settings



class SyncPaymentProfiles(generics.ListAPIView):
    """
    API Call to sync payment profiles
    """

    serializer_class = SyncPaymentProfileSerializer

    def get_queryset(self):
        return SyncPaymentProfileSerializer().sync_payment_profiles(self.kwargs['org_id'])
