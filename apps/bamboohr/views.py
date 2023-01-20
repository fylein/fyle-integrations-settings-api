import polling
import traceback
import logging
import json


from time import sleep
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import generics


from workato import Workato
from workato.exceptions import *
from apps.orgs.models import Org
from apps.orgs.actions import create_connection_in_workato
from apps.bamboohr.models import BambooHr, BambooHrConfiguration
from apps.bamboohr.serializers import BambooHrSerializer, BambooHrConfigurationSerializer

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

    def post(self, request, *args, **kwargs):
        connector = Workato()
        org = Org.objects.filter(id=kwargs['org_id']).first()
        bamboohr = BambooHr.objects.filter(org__id=org.id).first()

        try:
            package = connector.packages.post(org.managed_user_id, bamboohr.folder_id, 'assets/bamboohr_package.zip')
            
            # post package is an async request, polling to get the status of the package
            polling.poll(
                lambda: connector.packages.get(org.managed_user_id, package['id'])['status'] == 'completed',
                step=5,
                timeout=50
            )
            bamboohr.package_id = package['id']
            bamboohr.save()
    
            return Response(
                data={
                    'message': 'package uploaded successfully',
                },
                status=status.HTTP_200_OK
            )

        except BadRequestError as exception:
            error = traceback.format_exc()
            logger.error(error)
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

class BambooHrConnection(generics.CreateAPIView):
    """
    API Call to make Bamboo HR Connection in Workato
    """

    def post(self, request, *args, **kwargs):
        org = Org.objects.filter(id=kwargs['org_id']).first()
        bamboohr = BambooHr.objects.filter(org__id=kwargs['org_id']).first()

        try:
            
            # creating bamboo connection for cron job that will look for new employee in bamboohr
            bamboo_connection = create_connection_in_workato('BambooHR Connection', org.managed_user_id, request.data)
            
            # if the connection if successfull we will go on to create the second bamboohr connection
            # that is used for the complete sync recipe in bamboohr
            if bamboo_connection['authorization_status'] == 'success':
                connection_payload = {
                    "input": {
                        "ssl_params": "false",
                        "auth_type": "basic",
                        "basic_user": request.data['input']['api_token'],
                        "basic_password": "x"
                    }
                }
                bamboo_sync_connection = create_connection_in_workato('BambooHR Sync Connection', org.managed_user_id, connection_payload)
                bamboohr.api_token = request.data['input']['api_token']
                bamboohr.sub_domain = request.data['input']['subdomain']
                bamboohr.save()

                return Response(
                    data=bamboo_sync_connection,
                    status=status.HTTP_200_OK
                )

            return Response(
                data={'message': 'connection failed'},
                status=status.HTTP_400_BAD_REQUEST
            )

        except BadRequestError as exception:
            logger.error(
                'Error while creating Bamboo Hr Connection org_id - %s in Fyle %s',
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
                    'message': 'Error Creating Bamboo HR Connection in Recipe'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

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
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_object(self, *args, **kwargs):
        return self.get(self, *args, **kwargs)

class DisconnectView(generics.CreateAPIView):

    """
    API Call to Start And Stop a Recipe in Workato
    """

    def post(self, request, *args, **kwargs):
        connector = Workato()
        
        org = Org.objects.get(id=kwargs['org_id'])
        configuration = BambooHrConfiguration.objects.get(org__id=kwargs['org_id'])
        bamboohr = BambooHr.objects.filter(org__id=kwargs['org_id']).first()

        try:
            connections = connector.connections.get(managed_user_id=org.managed_user_id)['result']
            bamboo_connection_1 = next(connection for connection in connections if connection['name'] == 'BambooHR Connection')
            bamboo_connection_2 = next(connection for connection in connections if connection['name'] == 'BambooHR Sync Connection')

            configuration.recipe_status = False
            configuration.save()

            connection = connector.connections.post(
                managed_user_id=org.managed_user_id,
                connection_id=bamboo_connection_1['id'],

            )
            connector.connections.post(
                managed_user_id=org.managed_user_id,
                connection_id=bamboo_connection_2['id'],
            )

            bamboohr.api_token = None
            bamboohr.sub_domain = None
            bamboohr.save()

            return Response(
                data=connection,
                status=status.HTTP_200_OK
            )

        except NotFoundItemError as exception:
            logger.error(
                'Recipe with id %s not found in workato with org_id - %s in Fyle %s',
                configuration.recipe_id, org.id, exception.message
            )
            return Response(
                data=exception.message,
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as exception:
            logger.error(
                'Something unexpected happened in workato with org_id - %s in Fyle %s',
                org.id, exception.message
            )
            return Response(
                data={
                    'message': 'Error in Starting Or Stopping The Recipe'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class SyncEmployeesView(generics.UpdateAPIView):
    
    """
    API To Sync Employees From BambooHr To Fyle
    """

    def post(self, request, *args, **kwargs):
        connector = Workato()
        
        org = Org.objects.get(id=kwargs['org_id'])
        config = BambooHrConfiguration.objects.get(org__id=kwargs['org_id'])

        try:
            recipes = connector.recipes.get(managed_user_id=org.managed_user_id)['result']
            sync_recipe = next(recipe for recipe in recipes if recipe['name'] == "Bamboo HR Sync")
            code = json.loads(sync_recipe['code'])

            admin_emails = [
                {
                 'email': admin['email'],
                } for admin in config.emails_selected
            ]
            code['block'][6]['block'][1]['input']['personalizations']['to'] = admin_emails
            code['block'][6]['block'][1]['input']['from']['email'] = settings.SENDGRID_EMAIL
            sync_recipe['code'] = json.dumps(code)
            payload = {
                "recipe": {
                    "name": sync_recipe['name'],
                    "code": sync_recipe['code'],
                    "folder_id": str(sync_recipe['folder_id'])
                }
            }

            connector.recipes.post(org.managed_user_id, sync_recipe['id'], payload)
            connector.recipes.post(org.managed_user_id, sync_recipe['id'], None, 'start')
            sleep(5)
            connector.recipes.post(org.managed_user_id, sync_recipe['id'], None, 'stop')

            return Response(
                data=sync_recipe,
                status=status.HTTP_200_OK
            )


        except NotFoundItemError as exception:
            logger.error(
                'Recipe with id %s not found in workato with org_id - %s in Fyle %s',
                config.recipe_id, org.id, exception.message
            )
            return Response(
                data=exception.message,
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as exception:
            logger.error(
                'Something unexpected happened in workato with org_id - %s in Fyle %s',
                org.id, exception.message
            )
            return Response(
                data={'message': 'Error in Syncing Employees in BambooHR'},
                status=status.HTTP_400_BAD_REQUEST
            )
