
import os
import logging
import traceback

from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import generics

from apps.orgs.serializers import OrgSerializer
from apps.orgs.models import Org, User
from workato.workato import Workato


logger = logging.getLogger(__name__)
logger.level = logging.INFO

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
                        "REFRESH_TOKEN": os.environ.get('FYLE_REFRESH_TOKEN'),
                        "FYLE_BASE_URL": os.environ.get('FYLE_BASE_URL')
                    }
                }

                properties = connector.properties.post(managed_user['id'], properties_payload)

                return Response(
                    properties,
                    status=status.HTTP_200_OK
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

        connections = connector.connections.get(managed_user_id=org.managed_user_id)
        fyle_connection_id = connections['result'][2]['id']

        try:
            connection = connector.connections.put(
                managed_user_id=org.managed_user_id, 
                connection_id=fyle_connection_id,
                data=request.data
            )

            if connection['authorization_status'] == 'success':
                org.is_bamboo_connector = True
                org.save()

                return Response(
                    data={
                        'message': 'Connection Successfull'
                    },
                    status=status.HTTP_201_CREATED
                )

            return Response(
               connection,
               status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                data={
                    'message': 'Error in Creating Fyle Connection in Recipe'
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

        connections = connector.connections.get(managed_user_id=org.managed_user_id)
        sendgrid_connection_id = connections['result'][0]['id']

        try:
            connection = connector.connections.put(
                managed_user_id=org.managed_user_id,
                connection_id=sendgrid_connection_id,
                data={
                    "input": {
                        "api_key": os.environ.get('SENDGRID_API_KEY')
                    }
                }
            )

            if connection['authorization_status'] == 'success':
                return Response(
                    data={
                        'message': 'Connection Successfull'
                    },
                    status=status.HTTP_201_CREATED
                )

            return Response(
               connection,
               status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                data={
                    'message': 'Error in Creating Fyle Connection in Recipe'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
