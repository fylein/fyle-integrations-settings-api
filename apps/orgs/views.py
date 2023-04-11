
import logging
import traceback


from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import generics
from django.contrib.auth import get_user_model
from django.conf import settings

from workato.exceptions import *
from apps.orgs.serializers import OrgSerializer
from apps.orgs.models import Org, User
from apps.orgs.actions import get_admin_employees, create_connection_in_workato, \
        create_managed_user_and_set_properties
from apps.orgs.actions import get_admin_employees, handle_managed_user_exception
from .utils import get_signed_api_key
from apps.names import *

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


class CreateManagedUserInWorkato(generics.RetrieveUpdateAPIView):
    """
    Create and Get Managed User In Workato
    """

    def update(self, request, *args, **kwargs):

        org = Org.objects.get(id=kwargs['org_id'])
        managed_user = create_managed_user_and_set_properties(kwargs['org_id'], org)

        if 'id' in managed_user:
            return Response(
                managed_user,
                status=status.HTTP_200_OK
            )
        return managed_user
    
        return Response(
            data={'message': 'Managed User Not Created'},
            status=status.HTTP_400_BAD_REQUEST
        )


class FyleConnection(generics.CreateAPIView):
    """
    Api Call to make Fyle Connection in workato
    """

    def post(self, request, *args, **kwargs):


        org = Org.objects.get(id=kwargs['org_id'])
        data={
                "input": {
                    "key": "***"
                }
        }

        # Creating Fyle Connection In Workato COMMON_CONNECTIONS['fyle']
        connection = create_connection_in_workato(org.id, COMMON_CONNECTIONS['fyle'], org.managed_user_id, data)

        if 'authorization_status' in connection and connection['authorization_status'] == 'success':
            org.is_fyle_connected = True
            org.save()

            return Response(
                connection,
                status=status.HTTP_200_OK
            )
        elif  'authorization_status' in connection:
            return Response(
                connection,
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return connection
        return Response(
            data={'message': 'connection failed'},
            status=status.HTTP_400_BAD_REQUEST
        )


class SendgridConnection(generics.CreateAPIView):
    """
    API Call To Make Sendgrid Connection
    """

    def post(self, request, *args, **kwargs):

        org = Org.objects.get(id=kwargs['org_id'])
        data = {
            "input": {
                "api_key": settings.SENDGRID_API_KEY
            }
        }

        # Creating Fyle Sendgrid Connection
        connection = create_connection_in_workato(org.id, COMMON_CONNECTIONS['sendgrid'], org.managed_user_id, data)

        if 'authorization_status' in connection and connection['authorization_status'] == 'success':
            org.is_sendgrid_connected = True
            org.save()

            return Response(
                connection,
                status=status.HTTP_200_OK
            )

        elif 'authorization_status' in connection:
            return Response(
                connection,
                status = 500
            )
        
        return connection
        return Response(
            data={'message': 'connection failed'},
            status=status.HTTP_400_BAD_REQUEST
        )


class WorkspaceAdminsView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        """
        Get All Admins of this orgs
        """

        admin_employees = get_admin_employees(org_id=kwargs['org_id'], user=request.user)

        return Response(
            data=admin_employees,
            status=status.HTTP_200_OK
        )


class GenerateToken(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        try:
            managed_user_id = self.request.query_params.get('managed_user_id')
            token = get_signed_api_key(managed_user_id)
            return Response(
                data={'token':token},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            error = traceback.format_exc()
            logger.error('Error while generating token %s', error)
            return Response(
                data={
                    'message': 'Error Creating the Token'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
