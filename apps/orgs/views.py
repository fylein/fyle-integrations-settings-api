
import os
import logging
import traceback
import json

from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import generics
from fyle_rest_auth.models import AuthToken
from django.contrib.auth import get_user_model


from apps.orgs.serializers import OrgSerializer
from apps.orgs.models import Org, User, FyleCredential
from workato import Workato
from workato.exceptions import *

from apps.users.helpers import PlatformConnector


logger = logging.getLogger(__name__)
logger.level = logging.INFO

User = get_user_model()


class ReadyView(generics.RetrieveAPIView):
    """
    Ready call
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        """
        Ready call
        """

        return Response(
            data={
                'message': 'Ready'
            },
            status=status.HTTP_200_OK
        )

class OrgsView(generics.RetrieveUpdateAPIView):
    """
    New Fyle Org
    """
    serializer_class = OrgSerializer

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(user_id=self.request.user)
            org_id = self.request.query_params.get('org_id')
            org = Org.objects.get(user__in=[user], fyle_org_id=org_id)

            return Response(
                data=OrgSerializer(org).data,
                status=status.HTTP_200_OK
            )
        except Org.DoesNotExist:
            return Response(
                data={'message': 'Org Not Found'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_object(self):
        return self.get(self)

class CreateWorkatoWorkspace(generics.RetrieveUpdateAPIView):
    """
    Create and Get Managed User In Workato
    """
    def update(self, request, *args, **kwargs):
        connector = Workato()
        org = Org.objects.get(id=kwargs['org_id'])
        fyle_credentials = FyleCredential.objects.get(org__id=org.id)

        try:
            workspace_data = {
                'name': org.name,
                'external_id': org.fyle_org_id,
                'notification_email': org.user.first().email
            }

            managed_user = connector.managed_users.post(workspace_data)
            if managed_user['id']:
                org.managed_user_id = managed_user['id']
                org.save()

                properties_payload = {
                    "properties": {
                        "FYLE_CLIENT_ID": os.environ.get('FYLE_CLIENT_ID'),
                        "FYLE_CLIENT_SECRET": os.environ.get('FYLE_CLIENT_SECRET'),
                        "FYLE_BASE_URL": os.environ.get('FYLE_BASE_URL'),
                        "REFRESH_TOKEN": fyle_credentials.refresh_token
                    }
                }

                properties = connector.properties.post(managed_user['id'], properties_payload)

                return Response(
                    properties,
                    status=status.HTTP_200_OK
                )

        except BadRequestError as exception:
            logger.error(
                'Error while creating Workato Workspace org_id - %s in Fyle %s',
                org.id, exception.message
            )

            if 'message' in exception.message and 'external id has already been taken' in exception.message['message'].lower():
                return Response(
                    data={'message': 'Workspace already exists'},
                    status=status.HTTP_201_CREATED
                )

            return Response(
                data=exception.message,
                status=status.HTTP_400_BAD_REQUEST
            )

        except InternalServerError as exception:
            logger.error(
                'Error while creating Workato Workspace org_id - %s in Fyle %s',
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
                    'message': 'Error in Creating Workato Workspace'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class FyleConnection(generics.CreateAPIView):
    """
    Api Call to make Fyle Connection in workato
    """

    def post(self, request, *args, **kwargs):

        connector = Workato()
        org = Org.objects.get(id=kwargs['org_id'])

        try:
            connections = connector.connections.get(managed_user_id=org.managed_user_id)['result']
            fyle_connection = next(connection for connection in connections if connection['name'] == "Fyle Test Connection")

            connection = connector.connections.put(
                managed_user_id=org.managed_user_id, 
                connection_id=fyle_connection['id'],
                data=request.data
            )

            return Response(
               connection,
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

class SendgridConnection(generics.CreateAPIView):
    """
    API Call To Make Sendgrid Connection
    """
    def post(self, request, *args, **kwargs):

        connector = Workato()
        org = Org.objects.get(id=kwargs['org_id'])

        try:
            connections = connector.connections.get(managed_user_id=org.managed_user_id)['result']
            sendgrid_connection_id = next(connection for connection in connections if connection['name'] == "My SendGrid account")
            
            connection = connector.connections.put(
                managed_user_id=org.managed_user_id,
                connection_id=sendgrid_connection_id['id'],
                data={
                    "input": {
                        "api_key": os.environ.get('SENDGRID_API_KEY')
                    }
                }
            )
            
            return Response(
               connection,
               status=status.HTTP_200_OK
            )
            
        except BadRequestError as exception:
            logger.error(
                'Error while creating Sendgrid Connection org_id - %s in Fyle %s',
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
                    'message': 'Error Creating Sendgrid Connection in Recipe'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class WorkspaceAdminsView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        """
        Get Admins for the workspaces
        """

        org = Org.objects.get(pk=kwargs['org_id'])
        refresh_token = AuthToken.objects.get(user__user_id=request.user).refresh_token
        platform = PlatformConnector(refresh_token, org.cluster_domain)

        admin_email = []
        user_ids = []
        users = org.user.all()
        for user in users:
            admin = User.objects.get(user_id=user)
            user_ids.append(admin.user_id)

        id_filter = 'in.{}'.format(tuple(user_ids)).replace('\'', '"') \
            if len(user_ids) > 1 else 'eq.{}'.format(user_ids[0])

        employees_generator = platform.connection.v1beta.admin.employees.list_all(query_params={
            'user->id': id_filter,
            'order': 'id.desc'
        })

        for employee in employees_generator:
            admin_employees = [
                    {
                     'email': employee['user']['email'],
                     'name': employee['user']['full_name']
                    } for employee in employee['data']]

        for user in users:
            admin = User.objects.get(user_id=user)
            for employee in admin_employees:
                if employee['email'] == admin.email:
                    admin_email.append(employee)

        return Response(
                data=admin_email,
                status=status.HTTP_200_OK
            )
