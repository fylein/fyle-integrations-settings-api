import logging
import traceback
import polling
from django.conf import settings
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status


from workato import Workato
from workato.exceptions import *

from apps.names import TRAVELPERK
from apps.orgs.models import Org
from apps.orgs.actions import create_connection_in_workato, upload_properties
from apps.travelperk.serializers import TravelperkSerializer, TravelPerkConfigurationSerializer
from apps.travelperk.models import TravelPerk, TravelPerkConfiguration


logger = logging.getLogger(__name__)
logger.level = logging.INFO

# Create your views here.
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
                status=status.HTTP_400_BAD_REQUEST
            )

class PostFolder(generics.CreateAPIView):
    """
    API Call to Create Folder in Workato
    """
    serializer_class = TravelperkSerializer

    def post(self, request, *args, **kwargs):
        connector = Workato()
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

        try:
            folder = connector.folders.post(org.managed_user_id, 'Travelperk')
            upload_properties(org.managed_user_id, properties_payload)

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

        except BadRequestError as exception:
            logger.error(
                'Error while posting folder to workato with org_id - %s in Fyle %s',
                org.id, exception.message
            )
            return Response(
                data=exception.message,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception:
            error = traceback.format_exc()
            logger.error(error)
            return Response(
                data={
                    'message': 'Error in Creating Folder'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class PostPackage(generics.CreateAPIView):
    """
    API Call to Post Package in Workato
    """
    serializer_class = TravelperkSerializer

    def post(self, request, *args, **kwargs):
        connector = Workato()
        org = Org.objects.filter(id=kwargs['org_id']).first()
        travelperk = TravelPerk.objects.filter(org__id=org.id).first()

        try:
            package = connector.packages.post(org.managed_user_id, travelperk.folder_id, 'assets/travelperk.zip')
            polling.poll(
                lambda: connector.packages.get(org.managed_user_id, package['id'])['status'] == 'completed',
                step=5,
                timeout=50
            )
            travelperk.package_id = package['id']
            travelperk.save()
    
            return Response(
                data={
                    'message': 'package uploaded successfully'
                },
                status=status.HTTP_200_OK
            )

        except BadRequestError as exception:
            logger.error(
                'Error while posting bamboo package to workato for org_id - %s in Fyle %s',
                org.id, exception.message
            )
            return Response(
                data=exception.message,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception:
            error = traceback.format_exc()
            logger.error(error)
            return Response(
                data={
                    'message': 'Error in Uploading Package'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class AwsS3Connection(generics.CreateAPIView):
    """
    Api Call to make S3 Connection in workato
    """

    def post(self, request, *args, **kwargs):

        org = Org.objects.get(id=kwargs['org_id'])
        travelperk = TravelPerk.objects.get(org_id=org.id)
        try:
        
            data={
                "input": {
                    "key": "***"
                }
            }

            # Creating Fyle Connection In Workato
            connection = create_connection_in_workato(TRAVELPERK['s3'], org.managed_user_id, data)

            if connection['authorization_status'] == 'success':
                travelperk.is_s3_connected = True
                travelperk.save()

                return Response(
                   connection,
                   status=status.HTTP_200_OK
                )

            return Response(
                data={'message': 'connection failed'},
                status=status.HTTP_400_BAD_REQUEST
            )

        except BadRequestError as exception:
            logger.error(
                'Error while creating AWS Connection in Workato with org_id - %s in Fyle %s',
                org.id, exception.message
            )
            return Response(
                data=exception.message,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception:
            return Response(
                data={
                    'message': 'Error Creating AWS Connection in Recipe'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

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
                status=status.HTTP_400_BAD_REQUEST
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

        if recipe_status == False:
            connector.recipes.post(configuration.org.managed_user_id, configuration.recipe_id, None, 'stop')
            connector.connections.post(configuration.org.managed_user_id, travelperk.connection_id)
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

        org = Org.objects.get(id=kwargs['org_id'])
        travelperk = TravelPerk.objects.get(org_id=org.id)
        connector = Workato()
        try:

            # Creating travelperk Connection In Workato
            connections = connector.connections.get(managed_user_id=org.managed_user_id)['result']
            connection_id = next(connection for connection in connections if connection['name'] == TRAVELPERK['connection'])['id']

            travelperk.travelperk_connection_id = connection_id
            travelperk.save()

            return Response(
                data={'message': {'connection_id': connection_id}},
                status=status.HTTP_200_OK
            )

        except BadRequestError as exception:
            logger.error(
                'Error while creating Travelperk Connection in Workato with org_id - %s in Fyle %s',
                org.id, exception.message
            )
            return Response(
                data=exception.message,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as exception:
            error = traceback.format_exc()
            logger.error(error)
            return Response(
                data={
                    'message': 'Error Creating Travelperk Connection in Recipe'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
