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
from apps.gusto.models import Gusto, GustoConfiguration
from apps.gusto.serializers import GustoSerializer, GustoConfigurationSerializer

logger = logging.getLogger(__name__)
logger.level = logging.INFO


class GustoView(generics.ListAPIView):
    serializer_class = GustoSerializer

    def get(self, *args, **kwargs):
        try:
            gusto = Gusto.objects.get(org_id = kwargs['org_id'])
            return Response(
                data=GustoSerializer(gusto).data,
                status=status.HTTP_200_OK
            )
        except Gusto.DoesNotExist:
            return Response(
                data={'message': 'Gusto Details Not Found'},
                status=status.HTTP_404_NOT_FOUND
            )

class PostFolder(generics.CreateAPIView):
    """
    API Call to Create Folder in Workato
    """
    serializer_class = GustoSerializer

    def post(self, *args, **kwargs):
        connector = Workato()
        org = Org.objects.filter(id=kwargs['org_id']).first()

        try:
            folder = connector.folders.post(org.managed_user_id, 'Gusto')
            gusto, _ = Gusto.objects.update_or_create(
                org=org,
                defaults={
                    'folder_id': folder['id']
                }
            )

            return Response(
                data=GustoSerializer(gusto).data,
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

    def post(self, *args, **kwargs):
        connector = Workato()
        org = Org.objects.filter(id=kwargs['org_id']).first()
        gusto = Gusto.objects.filter(org__id=org.id).first()

        try:
            package = connector.packages.post(org.managed_user_id, Gusto.folder_id, 'assets/gusto.zip')
            
            # post package is an async request, polling to get the status of the package
            polling.poll(
                lambda: connector.packages.get(org.managed_user_id, package['id'])['status'] == 'completed',
                step=5,
                timeout=50
            )
            gusto.package_id = package['id']
            gusto.save()
    
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
                'Error while posting Gusto package to workato for org_id - %s in Fyle %s',
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

class GustoConnection(generics.CreateAPIView):
    """
    API Call to make Gusto Connection in Workato
    """

    def post(self, request, *args, **kwargs):
        org = Org.objects.filter(id=kwargs['org_id']).first()
        gusto = Gusto.objects.filter(org__id=kwargs['org_id']).first()

        try:
            
            # creating gusto connection for cron job that will look for new employee in Gusto
            gusto_connection = create_connection_in_workato('Gusto Connection', org.managed_user_id, request.data)
            
            # if the connection if successfull we will go on to create the second Gusto connection
            # that is used for the complete sync recipe in Gusto
            if gusto_connection['authorization_status'] == 'success':
                connection_payload = {
                    "input": {
                        "ssl_params": "false",
                        "connection_name": "Gusto Connection",
                        "client_id": settings.GUSTO_CLIENT_ID,
                        "client_secret": settings.GUSTO_CLIENT_SECRET,
                        "environment": settings.GUSTO_ENVIRONMENT
                    }
                }
                gusto_sync_connection = create_connection_in_workato('Gusto Sync Connection', org.managed_user_id, connection_payload)
                gusto.connection_id = gusto_connection['id']
                gusto.save()

                return Response(
                    data=gusto_sync_connection,
                    status=status.HTTP_200_OK
                )

            return Response(
                data={'message': 'connection failed'},
                status=status.HTTP_400_BAD_REQUEST
            )

        except BadRequestError as exception:
            logger.error(
                'Error while creating Gusto Connection org_id - %s in Fyle %s',
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
                    'message': 'Error Creating Gusto Connection in Recipe'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class GustoConfigurationView(generics.ListCreateAPIView):

    serializer_class = GustoConfigurationSerializer
    queryset = GustoConfiguration.objects.all()

    def get(self, *args, **kwargs):
        try:
            org_id = self.request.query_params.get('org_id')
            configuration = GustoConfiguration.objects.get(org__id=org_id)

            return Response(
                data=GustoConfigurationSerializer(configuration).data,
                status=status.HTTP_200_OK
            )

        except GustoConfiguration.DoesNotExist:
            return Response(
                data={'message': 'Gusto Configuration does not exist for this Workspace'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def get_object(self, *args, **kwargs):
        return self.get(self, *args, **kwargs)

class DisconnectView(generics.CreateAPIView):

    """
    API Call to Start And Stop a Recipe in Workato
    """

    def post(self, *args, **kwargs):
        connector = Workato()
        org_id = kwargs['org_id']
        org = Org.objects.get(id=org_id)
        configuration = GustoConfiguration.objects.get(org__id=org_id)

        try:
            connections = connector.connections.get(managed_user_id=org.managed_user_id)['result']
            gusto_connection_1 = next(connection for connection in connections if connection['name'] == 'Gusto Connection')
            gusto_connection_2 = next(connection for connection in connections if connection['name'] == 'Gusto Sync Connection')

            configuration.recipe_status = False
            configuration.save()

            connection = connector.connections.post(
                managed_user_id=org.managed_user_id,
                connection_id=gusto_connection_1['id'],

            )
            connector.connections.post(
                managed_user_id=org.managed_user_id,
                connection_id=gusto_connection_2['id'],
            )

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
    API To Sync Employees From Gusto To Fyle
    """

    def post(self, request, *args, **kwargs):
        connector = Workato()
        
        org = Org.objects.get(id=kwargs['org_id'])
        config = GustoConfiguration.objects.get(org__id=kwargs['org_id'])

        try:
            recipes = connector.recipes.get(managed_user_id=org.managed_user_id)['result']
            sync_recipe = next(recipe for recipe in recipes if recipe['name'] == "Gusto Sync")
            code = json.loads(sync_recipe['code'])
            admin_emails = [
                {
                 'email': admin['email'],
                } for admin in config.emails_selected
            ]

            code['block'][5]['block'][1]['input']['personalizations']['to'] = admin_emails
            code['block'][5]['block'][1]['input']['from']['email'] = settings.SENDGRID_EMAIL
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
                data={'message': 'Error in Syncing Employees in Gusto'},
                status=status.HTTP_400_BAD_REQUEST
            )
