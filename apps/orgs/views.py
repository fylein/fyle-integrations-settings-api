
import os
import logging
from django.core.cache import cache
import traceback

from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from fyle_rest_auth.models import AuthToken
from fyle_rest_auth.helpers import get_fyle_admin
from admin_settings.helpers import get_cluster_domain

from apps.orgs.serializers import OrgSerializer
from apps.orgs.models import FyleCredential, Org, User
from workato_connector.workato import Workato


logger = logging.getLogger(__name__)
logger.level = logging.INFO


class OrgsView(generics.RetrieveUpdateAPIView):
    """
    New Fyle Org
    """
    serializer_class = OrgSerializer

    def get_object(self):
        org_id = self.request.query_params.get('org_id')
        return Org.objects.filter(fyle_org_id=org_id).first()

    def put(self, request):
        """
        Create a Org
        """
        access_token = request.META.get('HTTP_AUTHORIZATION')
        fyle_user = get_fyle_admin(access_token.split(' ')[1], None)
        org_name = fyle_user['data']['org']['name']
        org_id = fyle_user['data']['org']['id']

        org = Org.objects.filter(fyle_org_id=org_id).first()

        if org:
            org.user.add(User.objects.get(user_id=request.user))
            cache.delete(str(org.id))
        else:
            auth_tokens = AuthToken.objects.get(user__user_id=request.user)
            cluster_domain = get_cluster_domain(auth_tokens.refresh_token)
            org = Org.objects.create(name=org_name, fyle_org_id=org_id, cluster_domain=cluster_domain)
            org.user.add(User.objects.get(user_id=request.user))

            FyleCredential.objects.update_or_create(
                refresh_token=auth_tokens.refresh_token,
                org_id=org.id,
            )

        return Response(
            data=OrgSerializer(org).data,
            status=status.HTTP_200_OK
        )

class CreateWorkatoWorkspace(generics.RetrieveUpdateAPIView):
    """
    Create and Get Managed User In Workato
    """

    def update(self, request, *args, **kwargs):
        connector = Workato()

        try:
            managed_user = connector.managed_users.post(request.data)
            if managed_user:
                org = Org.objects.get(id=kwargs['org_id'])
                org.managed_user_id = managed_user['id']
                org.save()

            created_folder = connector.folders.post(managed_user['id'], 'Bamboo HR')
            connector.packages.post(managed_user['id'], created_folder['id'], 'assets/package.zip')

            properties_payload = {
                "properties": {
                    "CLIENT_ID": os.environ.get('FYLE_CLIENT_ID'),
                    "CLIENT_SECRET": os.environ.get('FYLE_CLIENT_SECRET'),
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
        managed_user_id=kwargs['managed_user_id']

        connections  = connector.connections.get(managed_user_id=managed_user_id)
        fyle_connection_id = connections['result'][1]['id']

        try:
            connection = connector.connections.put(
                managed_user_id=managed_user_id, 
                connection_id=fyle_connection_id,
                data=request.data
            )

        except Exception:
            return Response(
                data={
                    'message': 'Error in Creating Fyle Connection in Recipe'
                },
                status=status.HTTP_400_BAD_REQUEST
            )    

        return Response(
           connection,
           status=status.HTTP_200_OK
        )
