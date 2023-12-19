import logging
import traceback
from django.conf import settings
from django.db import transaction
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status

from workato import Workato
from workato.exceptions import *

from apps.names import TRAVELPERK
from apps.orgs.models import Org
from apps.orgs.actions import create_connection_in_workato, upload_properties, post_folder, post_package
from apps.travelperk.serializers import TravelperkSerializer, TravelPerkConfigurationSerializer
from apps.travelperk.models import TravelPerk, TravelPerkConfiguration, TravelperkCredential, Invoice, InvoiceLineItem
from apps.travelperk.actions import connect_travelperk
from apps.travelperk.connector import TravelperkConnector

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

class PostFolder(generics.CreateAPIView):
    """
    API Call to Create Folder in Workato
    """
    serializer_class = TravelperkSerializer

    def post(self, request, *args, **kwargs):
        org = Org.objects.filter(id=kwargs['org_id']).first()

        properties_payload = {
            'properties': {
                'TRAVELPERK_CLIENT_ID': settings.TRAVELPERK_CLIENT_ID,
                'TRAVELPERK_CLIENT_SECRET': settings.TRAVELPERK_CLIENT_SECRET,
                'TRAVELPERK_AUTH_URL': settings.TRAVELPERK_AUTH_URL,
                'TRAVELPERK_TOKEN_URL': settings.TRAVELPERK_TOKEN_URL,
                'TRAVELPERK_BASE_URL': settings.TRAVELPERK_BASE_URL
            }
        }
        upload_properties(org.managed_user_id, properties_payload)
        folder = post_folder(
            org_id=kwargs['org_id'],
            folder_name='Travelperk'
        )

        # case of an error Response
        if isinstance(folder, Response):
            return folder
        
        travelperk, _ = TravelPerk.objects.update_or_create(
            org=org,
            defaults={
                'folder_id': folder['id']
            }
        )

        return Response(
            data=TravelperkSerializer(travelperk).data,
            status=status.HTTP_200_OK
        )

class PostPackage(generics.CreateAPIView):
    """
    API Call to Post Package in Workato
    """
    serializer_class = TravelperkSerializer

    def post(self, request, *args, **kwargs):
        org = Org.objects.filter(id=kwargs['org_id']).first()
        travelperk = TravelPerk.objects.filter(org__id=org.id).first()
        package = post_package(
            org_id=kwargs['org_id'],
            folder_id=travelperk.folder_id,
            package_path='assets/travelperk.zip'
        )
        
        # in case of an error response
        if isinstance(package, Response):
            return package
        
        travelperk.package_id = package['id']
        travelperk.save()
        return Response(
            data={
                'message': 'package uploaded successfully'
            },
            status=status.HTTP_200_OK
        )


class AwsS3Connection(generics.CreateAPIView):
    """
    Api Call to make S3 Connection in workato
    """

    def post(self, request, *args, **kwargs):

        org = Org.objects.get(id=kwargs['org_id'])
        travelperk = TravelPerk.objects.get(org_id=org.id)

        data={
            "input": {
                "key": "***"
            }
        }

        # Creating Fyle Connection In Workato
        connection = create_connection_in_workato(org.id, TRAVELPERK['s3'], org.managed_user_id, data)

        if 'authorization_status' in connection and connection['authorization_status'] == 'success':
            travelperk.is_s3_connected = True
            travelperk.save()

            return Response(
                connection,
                status=status.HTTP_200_OK
            )
    
        elif 'authorization_status' in connection:
            return Response(connection, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return connection


class TravekPerkConfigurationView(generics.ListCreateAPIView):

    serializer_class = TravelPerkConfigurationSerializer
    queryset = TravelPerk.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            org_id = self.request.query_params.get('org_id')
            travelperk_configuration = TravelPerkConfiguration.objects.get(org__id=org_id)

            return Response(
                data=TravelPerkConfigurationSerializer(travelperk_configuration).data,
                status=status.HTTP_200_OK
            )

        except TravelPerkConfiguration.DoesNotExist:
            return Response(
                data={'message': 'Configuration does not exist for this Workspace'},
                status=status.HTTP_404_NOT_FOUND
            )

    def get_object(self, *args, **kwargs):
        return self.get(self, *args, **kwargs)


class RecipeStatusView(generics.UpdateAPIView):
    """
    Update View For Changing Recipe Status
    """
    def update(self, request, *args, **kwargs):

        connector = Workato()
        recipe_status = request.data.get('recipe_status')

        travelperk: TravelPerk = TravelPerk.objects.get(org__id=kwargs['org_id'])
        configuration: TravelPerkConfiguration = TravelPerkConfiguration.objects.get(org__id=kwargs['org_id'])
        configuration.is_recipe_enabled = recipe_status
        configuration.save()

        action = 'start' if recipe_status else 'stop'
        connector.recipes.post(configuration.org.managed_user_id, configuration.recipe_id, None, action=action)
        
        if recipe_status == False:
            connector.connections.post(configuration.org.managed_user_id, travelperk.travelperk_connection_id)
            travelperk.is_travelperk_connected = False
            travelperk.save()
        else:
            connector.recipes.post(configuration.org.managed_user_id, configuration.recipe_id, None, 'start')

        return Response(
            data=TravelPerkConfigurationSerializer(configuration).data,
            status=status.HTTP_200_OK
        )


class TravelperkConnection(generics.ListCreateAPIView):
    """
    Api Call to make Travelperk Connection in workato
    """

    def post(self, request, *args, **kwargs):
        connection_id = connect_travelperk(kwargs['org_id'])

        # case of an error Response
        if isinstance(connection_id, Response):
            return connection_id
        
        return Response(
            data={'message': {'connection_id': connection_id}},
            status=status.HTTP_200_OK
        )


class ConnectTravelperkView(generics.CreateAPIView):
    """
    Api Call to make Travelperk Connection in workato
    """

    def post(self, request, *args, **kwargs):

        try:
            org = Org.objects.get(id=kwargs['org_id'])
            refresh_token = get_refresh_token_using_auth_code(request.data.get('code'), kwargs['org_id'])
            
            if refresh_token:
                travelperk_credential = TravelperkCredential.objects.get(org=org)
                travelperk_connection = TravelperkConnector(travelperk_credential, kwargs['org_id'])
                
                travelperk_webhook_data = {
                    'name': 'travelperk webhook invoice',
                    'url': 'https://webhook.site/e4ac2898-209f-4dd2-88cf-738dea95ecdc',
                    'secret': 'some secret',
                    'events': [
                        'invoice.issued'
                    ]
                }

                created_webhook = travelperk_connection.create_webhook(travelperk_webhook_data)
                print('created_webhook', created_webhook)
                TravelPerk.objects.update_or_create(
                    org=org,
                    defaults={
                        'webhook_id': created_webhook['id'],
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

    def create(self, request, *args, **kwargs):
        try:
            # Custom processing of the webhook event data
            with transaction.atomic():
                # Extract invoice line items from the request data
                invoice_lineitems_data = request.data.pop('lines')

                # Create or update Invoice and related line items
                invoice = Invoice.create_or_update_invoices(request.data)
                invoice_linteitmes = InvoiceLineItem.create_or_update_invoice_lineitems(invoice_lineitems_data, invoice)

            create_expense_in_fyle(kwargs['org_id'], invoice, invoice_linteitmes)

            return Response({'status': 'success'})

        except Exception as e:
            return Response({'status': 'error', 'error_message': str(e)})
