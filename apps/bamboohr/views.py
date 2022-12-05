from requests import Response
import polling
import traceback
import logging

from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import generics

from workato.workato import Workato
from apps.orgs.models import Org
from apps.bamboohr.models import BambooHr
from apps.bamboohr.serializers import BambooHrSerializer


logger = logging.getLogger(__name__)
logger.level = logging.INFO


class BambooHrView(generics.ListAPIView):
    serializer_class = BambooHrSerializer

    def get(self, request, *args, **kwargs):
        try:
            bamboohr = BambooHr.objects.get(org_id__in=[kwargs['org_id']])

            return Response(
                data=BambooHrSerializer(bamboohr).data,
                status=status.HTTP_200_OK
            )
        except BambooHr.DoesNotExist:
            return Response(
                data={'message': 'Bamboo HR Details Not Found'},
                status=status.HTTP_400_BAD_REQUEST
            )

class PostFolder(generics.CreateAPIView):
    """
    API Call to Create Folder in Workato
    """
    serializer_class = BambooHrSerializer

    def post(self, request, *args, **kwargs):
        connector = Workato()
        org = Org.objects.filter(id=kwargs['org_id']).first()

        try:
            folder = connector.folders.post(org.managed_user_id, 'Bamboo HR')
            bamboohr = BambooHr.objects.create(folder_id=folder['id'], org=org)

            return Response(
                data=BambooHrSerializer(bamboohr).data,
                status=status.HTTP_200_OK
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
    serializer_class = BambooHrSerializer

    def post(self, request, *args, **kwargs):
        connector = Workato()
        org = Org.objects.filter(id=kwargs['org_id']).first()
        bamboohr = BambooHr.objects.filter(org__id=org.id).first()

        try:
            package = connector.packages.post(org.managed_user_id, bamboohr.folder_id, 'assets/package.zip')                
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

        except Exception:
            error = traceback.format_exc()
            logger.error(error)
            return Response(
                data={
                    'message': 'Error in Uploading Package'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class BambooHrConnection(generics.CreateAPIView):
    """
    API Call to make Bamboo HR Connection in Workato
    """

    def post(self, request, *args, **kwargs):
        connector = Workato()
        org = Org.objects.filter(id=kwargs['org_id']).first()
        bamboohr = BambooHr.objects.filter(org__id=kwargs['org_id']).first()

        try:
            connections = connector.connections.get(managed_user_id=org.managed_user_id)
            bamboo_connections = connections['result'][1]
            connector.connections.put(
                managed_user_id=org.managed_user_id,
                connection_id=bamboo_connections['id'],
                data=request.data
            )

            bamboohr.api_token = request.data['input']['api_token']
            bamboohr.sub_domain = request.data['input']['subdomain']

            bamboohr.save()
            org.save()

            return Response(
                data=BambooHrSerializer(bamboohr).data,
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                data={
                    'message': 'Error Creating Bamboo HR Connection in Recipe'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
