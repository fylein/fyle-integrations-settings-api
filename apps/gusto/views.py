import polling
import traceback
import logging
import json

from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import generics


from workato import Workato
from workato.exceptions import *
from apps.orgs.models import Org
from apps.orgs.actions import post_folder, post_package
from apps.gusto.models import Gusto, GustoConfiguration
from apps.gusto.serializers import GustoSerializer, GustoConfigurationSerializer
from apps.gusto.utils import set_gusto_properties
from apps.names import *

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
        org = Org.objects.filter(id=kwargs['org_id']).first()

        set_gusto_properties(org.managed_user_id)
        folder = post_folder(
            org_id = kwargs['org_id'],
            folder_name='Gusto'
        )

        if isinstance(folder, Response):
            return folder
        
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

class PostPackage(generics.CreateAPIView):
    """
    API Call to Post Package in Workato
    """

    def post(self, *args, **kwargs):
        org = Org.objects.filter(id=kwargs['org_id']).first()
        gusto = Gusto.objects.filter(org__id=org.id).first()

        package = post_package(
            org_id=kwargs['org_id'],
            folder_id=gusto.folder_id,
            package_path='assets/gusto.zip'
        )

        if isinstance(package, Response):
            return package
        
        gusto.package_id = package['id']
        gusto.save()

        return Response(
            data={
                'message': 'package uploaded successfully',
            },
            status=status.HTTP_200_OK
        )

class GustoConfigurationView(generics.ListCreateAPIView):

    serializer_class = GustoConfigurationSerializer
    queryset = GustoConfiguration.objects.all()

    def get(self, *args, **kwargs):
        try:
            org_id = kwargs['org_id']
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

class SyncEmployeesView(generics.UpdateAPIView):
    
    """
    API To Sync Employees From Gusto To Fyle
    """

    def post(self, *args, **kwargs):
        connector = Workato()
        
        org = Org.objects.get(id=kwargs['org_id'])
        config = GustoConfiguration.objects.get(org__id=kwargs['org_id'])

        try:
            recipes = connector.recipes.get(managed_user_id=org.managed_user_id)['result']
            sync_recipe = next(recipe for recipe in recipes if recipe['name'] == GUSTO['recipe'])
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
                    "code": sync_recipe['code'],
                }
            }

            connector.recipes.post(org.managed_user_id, sync_recipe['id'], payload)
            connector.recipes.post(org.managed_user_id, sync_recipe['id'], None, 'start')

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
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GustoConnection(generics.ListCreateAPIView):
    """
    Api Call to make Gusto Connection in workato
    """

    def post(self, request, *args, **kwargs):

        org = Org.objects.get(id=kwargs['org_id'])
        gusto = Gusto.objects.get(org_id=org.id)
        connector = Workato()
        try:

            # Creating gusto Connection In Workato
            connections = connector.connections.get(managed_user_id=org.managed_user_id)['result']
            connection_id  = next(connection for connection in connections if connection['name'] == GUSTO['connection'])['id']

            gusto.connection_id = connection_id
            gusto.save()

            return Response(
                data={'message': {'connection_id': connection_id}},
                status=status.HTTP_200_OK
            )

        except BadRequestError as exception:
            logger.error(
                'Error while creating Gusto Connection in Workato with org_id - %s in Fyle %s',
                org.id, exception.message
            )
            return Response(
                data=exception.message,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as ex:
            return Response(
                data={
                    'message': 'Error Creating Gusto Connection in Recipe'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        

class RecipeStatusView(generics.UpdateAPIView):
    """
    Update View For Changing Recipe Status
    """
    def update(self, request, *args, **kwargs):

        connector = Workato()
        recipe_status = request.data.get('recipe_status')
        action = 'start' if recipe_status else 'stop'
        try:
            configuration: GustoConfiguration = GustoConfiguration.objects.get(org__id=kwargs['org_id'])
            configuration.recipe_status = recipe_status
            configuration.save()

            connector.recipes.post(configuration.org.managed_user_id, configuration.recipe_id, None, action)

            return Response(
                data=GustoConfigurationSerializer(configuration).data,
                status=status.HTTP_200_OK
            )
        except GustoConfiguration.DoesNotExist:
            return Response({
                'message': 'Gusto Configuration is not available.'
            }, status = status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            error = traceback.format_exc()
            logger.error(error)
            return Response({
                'message': error
            }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
