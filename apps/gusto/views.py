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
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception:
            error = traceback.format_exc()
            logger.error(error)
            return Response(
                data={
                    'message': 'Error in Creating Folder'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception:
            error = traceback.format_exc()
            logger.error(error)
            return Response(
                data={
                    'message': 'Error in Uploading Package'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
                    "code": sync_recipe['code'],
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
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
