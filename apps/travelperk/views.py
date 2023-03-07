import logging
import traceback
import polling
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status


from workato import Workato
from workato.exceptions import *


from apps.orgs.models import Org
from apps.orgs.actions import create_connection_in_workato
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

        try:
            folder = connector.folders.post(org.managed_user_id, 'Travelperk')
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
        bamboohr = TravelPerk.objects.filter(org__id=org.id).first()

        try:
            package = connector.packages.post(org.managed_user_id, bamboohr.folder_id, 'assets/travelperk.zip')
            polling.poll(
                lambda: connector.packages.get(org.managed_user_id, package['id'])['status'] == 'completed',
                step=5,
                timeout=50
            )
            bamboohr.package_id = package['id']
            bamboohr.save()
    
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

class FyleTravelperkConnection(generics.ListAPIView):
    """
    Api Call to make Fyle Connection in workato
    """

    def get(self, request, *args, **kwargs):
        
        org = Org.objects.get(id=kwargs['org_id'])
        travelperk = TravelPerk.objects.get(org_id=org.id)
        connector = Workato()
        try:

            # Creating Fyle Connection In Workato
            connections = connector.connections.get(managed_user_id=org.managed_user_id)['result']
            connection_id  = next(connection for connection in connections if connection['name'] == 'Travelperk Connection')['id']

            travelperk.travelperk_connection_id = connection_id
            travelperk.save()

            return Response(
                data={'message': {'connection_id': connection_id}},
                status=status.HTTP_200_OK
            )

        except BadRequestError as exception:
            logger.error(
                'Error while creating Fyle Connection in Workato with org_id - %s in Fyle %s',
                org.id, exception.message
            )
            return Response(
                data=exception.message,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception:
            return Response(
                data={
                    'message': 'Error Creating Fyle Connection in Recipe'
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
            connection = create_connection_in_workato('S3 Connection', org.managed_user_id, data)

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