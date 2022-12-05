from requests import Response
import polling
import traceback
import logging
import time

from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import generics

from workato import Workato
from workato.exceptions import *
from apps.orgs.models import Org
from apps.bamboohr.models import BambooHr, Configuration
from apps.bamboohr.serializers import BambooHrSerializer, ConfigurationSerializer


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

    def get_object(self):
        return self.get(self)

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
            BambooHr.objects.create(folder_id=folder['id'], org=org)

            return Response(
                data=folder,
                status=status.HTTP_201_CREATED
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
    serializer_class = BambooHrSerializer

    def post(self, request, *args, **kwargs):
        connector = Workato()
        org = Org.objects.filter(id=kwargs['org_id']).first()
        bamboohr = BambooHr.objects.filter(org__id=org.id).first()
        try:
            if bamboohr.package_id:  
                package = connector.packages.get(org.managed_user_id, bamboohr.package_id)   
            else:
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
                    'package uploaded successfully'
                },
                status=status.HTTP_201_CREATED
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

class BambooHrConnection(generics.CreateAPIView):
    """
    API Call to make Bamboo HR Connection in Workato
    """

    def post(self, request, *args, **kwargs):
        connector = Workato()
        org = Org.objects.filter(id=kwargs['org_id']).first()
        bamboohr = BambooHr.objects.filter(org__id=kwargs['org_id']).first()

        try:
            connections = connector.connections.get(managed_user_id=org.managed_user_id)['result']
            bamboo_connection_1 = next(connection for connection in connections if connection['name'] == 'My BambooHR account')
            bamboo_connection_2 = next(connection for connection in connections if connection['name'] == 'Bamboo HR Test')

            connection = connector.connections.put(
                managed_user_id=org.managed_user_id,
                connection_id=bamboo_connection_1['id'],
                data=request.data
            )

            connection_payload = {
                "input": {
                    "ssl_params": "false",
                    "auth_type": "basic",
                    "basic_user": request.data['input']['api_token'],
                    "basic_password": "x"
                }
            }

            connection = connector.connections.put(
                managed_user_id=org.managed_user_id,
                connection_id=bamboo_connection_2['id'],
                data=connection_payload
            )

            bamboohr.api_token = request.data['input']['api_token']
            bamboohr.sub_domain = request.data['input']['subdomain']
            bamboohr.save()

            return Response(
                data=connection,
                status=status.HTTP_200_OK
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
                    'message': 'Error in Creating Bamboo HR Connection in Recipe'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class ConfigurationView(generics.ListCreateAPIView):

    serializer_class = ConfigurationSerializer
    queryset = Configuration.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            org_id = self.request.query_params.get('org_id')
            configuration = Configuration.objects.get(org__id=org_id)

            return Response(
                data=ConfigurationSerializer(configuration).data,
                status=status.HTTP_200_OK
            )

        except Configuration.DoesNotExist:
            return Response(
                data={'message': 'Configuration does not exist for this Workspace'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_object(self, *args, **kwargs):
        return self.get(self, *args, **kwargs)

class StartAndStopRecipe(generics.CreateAPIView):

    """
    API Call to Start And Stop a Recipe in Workato
    """

    def post(self, request, *args, **kwargs):
        connector = Workato()
        
        org = Org.objects.get(id=kwargs['org_id'])
        config = Configuration.objects.get(org__id=kwargs['org_id'])
        
        try:
            connection = connector.recipes.post(org.managed_user_id, config.recipe_id, None, request.data['payload'])

        except NotFoundItemError as exception:
            logger.error(
                'Recipe with id %s not found in workato with org_id - %s in Fyle %s',
                config.recipe_id, org.id, exception.message
            )
            return Response(
                data=exception.message,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except BadRequestError as exception:
            logger.error(
                'Something unexpected happened in workato with org_id - %s in Fyle %s',
                org.id, exception.message
            )
            return Response(
                data=exception.message,
                status=status.HTTP_400_BAD_REQUEST
            )
 
        return Response(
            data=connection,
            status=status.HTTP_200_OK
        )

class SyncEmployeesView(generics.UpdateAPIView):
    
    """
    API To Sync Employees From BambooHr To Fyle
    """

    def post(self, request, *args, **kwargs):
        connector = Workato()
        
        org = Org.objects.get(id=kwargs['org_id'])
        config = Configuration.objects.get(org__id=kwargs['org_id'])
        
        try:
            recipes = connector.recipes.get(managed_user_id=org.managed_user_id)['result']
            sync_recipe = next(recipe for recipe in recipes if recipe['name'] == "Bamboo HR")

            connector.recipes.post(org.managed_user_id, sync_recipe['id'], None, 'start')
            connector.recipes.post(org.managed_user_id, sync_recipe['id'], None, 'stop')

        except NotFoundItemError as exception:
            logger.error(
                'Recipe with id %s not found in workato with org_id - %s in Fyle %s',
                config.recipe_id, org.id, exception.message
            )
            return Response(
                data=exception.message,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except BadRequestError as exception:
            logger.error(
                'Something unexpected happened in workato with org_id - %s in Fyle %s',
                org.id, exception.message
            )
            return Response(
                data=exception.message,
                status=status.HTTP_400_BAD_REQUEST
            )
 
        return Response(
            data=sync_recipe,
            status=status.HTTP_200_OK
        )
