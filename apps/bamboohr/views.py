import logging

from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import generics

from workato.exceptions import *
from apps.orgs.models import Org
from apps.orgs.actions import create_connection_in_workato, post_folder, post_package
from apps.bamboohr.models import BambooHr, BambooHrConfiguration
from apps.bamboohr.serializers import BambooHrSerializer, BambooHrConfigurationSerializer
from apps.bamboohr.actions import disconnect_bamboohr, sync_employees
from apps.names import BAMBOO_HR

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
                status=status.HTTP_404_NOT_FOUND
            )

class PostFolder(generics.CreateAPIView):
    """
    API Call to Create Folder in Workato
    """
    serializer_class = BambooHrSerializer

    def post(self, request, *args, **kwargs):
        org = Org.objects.filter(id=kwargs['org_id']).first()

        folder = post_folder(
            org_id=kwargs['org_id'],
            folder_name='Bamboo HR'
        )
        bamboohr, _ = BambooHr.objects.update_or_create(
            org=org,
            defaults={
                'folder_id': folder['id']
            }
        )

        return Response(
            data=BambooHrSerializer(bamboohr).data,
            status=status.HTTP_200_OK
        )

class PostPackage(generics.CreateAPIView):
    """
    API Call to Post Package in Workato
    """

    def post(self, request, *args, **kwargs):
        org = Org.objects.filter(id=kwargs['org_id']).first()
        bamboohr = BambooHr.objects.filter(org__id=org.id).first()

        package = post_package(
            org_id=kwargs['org_id'],
            folder_id=bamboohr.folder_id,
            package_path='assets/bamboohr_package.zip'
        )
        bamboohr.package_id = package['id']
        bamboohr.save()

        return Response(
            data={
                'message': 'package uploaded successfully',
            },
            status=status.HTTP_200_OK
        )


class BambooHrConnection(generics.CreateAPIView):
    """
    API Call to make Bamboo HR Connection in Workato
    """

    def post(self, request, *args, **kwargs):
        org = Org.objects.filter(id=kwargs['org_id']).first()
        bamboohr = BambooHr.objects.filter(org__id=kwargs['org_id']).first()

        # creating bamboo connection for cron job that will look for new employee in bamboohr
        bamboo_connection = create_connection_in_workato(org.id, BAMBOO_HR['connections'][0], org.managed_user_id, request.data)
        
        # if the connection if successfull we will go on to create the second bamboohr connection
        # that is used for the complete sync recipe in bamboohr
        if 'authorization_status' in bamboo_connection and bamboo_connection['authorization_status'] == 'success':
            connection_payload = {
                "input": {
                    "ssl_params": "false",
                    "auth_type": "basic",
                    "basic_user": request.data['input']['api_token'],
                    "basic_password": "x"
                }
            }
            bamboo_sync_connection = create_connection_in_workato(org.id, BAMBOO_HR['connections'][1], org.managed_user_id, connection_payload)
            bamboohr.api_token = request.data['input']['api_token']
            bamboohr.sub_domain = request.data['input']['subdomain']
            bamboohr.save()

            return Response(
                data=bamboo_sync_connection,
                status=status.HTTP_200_OK
            )
        elif 'authorization_status' in bamboo_connection:
            return Response(
                bamboo_connection,
                status = status.HTTP_400_BAD_REQUEST
            )
        return bamboo_connection


class BambooHrConfigurationView(generics.ListCreateAPIView):

    serializer_class = BambooHrConfigurationSerializer
    queryset = BambooHrConfiguration.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            org_id = self.request.query_params.get('org_id')
            configuration = BambooHrConfiguration.objects.get(org__id=org_id)

            return Response(
                data=BambooHrConfigurationSerializer(configuration).data,
                status=status.HTTP_200_OK
            )

        except BambooHrConfiguration.DoesNotExist:
            return Response(
                data={'message': 'BambooHr Configuration does not exist for this Workspace'},
                status=status.HTTP_404_NOT_FOUND
            )

    def get_object(self, *args, **kwargs):
        return self.get(self, *args, **kwargs)

class DisconnectView(generics.CreateAPIView):

    """
    API Call to Start And Stop a Recipe in Workato
    """

    def post(self, request, *args, **kwargs):
        try:
            configuration = BambooHrConfiguration.objects.get(org__id=kwargs['org_id'])
            bamboohr = BambooHr.objects.filter(org__id=kwargs['org_id']).first()

            connection = disconnect_bamboohr(kwargs['org_id'], configuration, bamboohr)

            return Response(
                data=connection,
                status=status.HTTP_200_OK
            )
        except BambooHr.DoesNotExist:
            return Response(
                data = {
                    'message': 'BambooHR connection does not exists for this org.'
                },
                status = status.HTTP_404_NOT_FOUND
            )
        except BambooHrConfiguration.DoesNotExist:
            return Response(
                data={'message': 'BambooHr Configuration does not exist for this Workspace'},
                status=status.HTTP_404_NOT_FOUND
            )


class SyncEmployeesView(generics.UpdateAPIView):
    
    """
    API To Sync Employees From BambooHr To Fyle
    """

    def post(self, request, *args, **kwargs):
    
        try:
            config = BambooHrConfiguration.objects.get(org__id=kwargs['org_id'])
            sync_recipe = sync_employees(kwargs['org_id'], config)
            return Response(
                data=sync_recipe,
                status=status.HTTP_200_OK
            )
        except BambooHrConfiguration.DoesNotExist:
            return Response(
                data={'message': 'BambooHr Configuration does not exist for this Workspace'},
                status=status.HTTP_404_NOT_FOUND
            )
