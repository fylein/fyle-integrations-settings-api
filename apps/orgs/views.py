
from django.core.cache import cache

from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from fyle_rest_auth.models import AuthToken
from fyle_rest_auth.helpers import get_fyle_admin
from apps.orgs.helpers import get_cluster_domain

from apps.orgs.serializers import OrgSerializer
from apps.orgs.models import FyleCredential, Org, User
from workato_connector.workato import Workato


class ReadyView(viewsets.ViewSet):
    """
    Ready call
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        """
        Ready call
        """

        Org.objects.first()

        return Response(
            data={
                'message': 'Ready'
            },
            status=status.HTTP_200_OK
        )

class OrgsView(viewsets.ViewSet):
    """
    Fyle Org
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Create a Workspace
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

    def get(self, request):
        """
        Get workspace
        """
        user = User.objects.get(user_id=request.user)
        org_id = request.query_params.get('org_id')
        org = Org.objects.filter(user__in=[user], fyle_org_id=org_id).all()

        return Response(
            data=OrgSerializer(org, many=True).data,
            status=status.HTTP_200_OK
        )

    def get_by_id(self, request, **kwargs):
        """
        Get Org by id
        """
        try:
            user = User.objects.get(user_id=request.user)
            org = Org.objects.get(pk=kwargs['org_id'], user=user)

            return Response(
                data=OrgSerializer(org).data if org else {},
                status=status.HTTP_200_OK
            )
        except Org.DoesNotExist:
            return Response(
                data={
                    'message': 'Org with this id does not exist'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ManagedUser(viewsets.ViewSet):
    """
    Create and Get Managed User In Workato
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):

        connector = Workato()

        managed_user = connector.managed_users.post(request.data)
        if managed_user:
            org = Org.objects.get(id=kwargs['org_id'])
            org.managed_user_id = managed_user['id']
            org.save()

        return Response(
            managed_user,
            status=status.HTTP_200_OK
        )
    
    def get(self, request, *args, **kwargs):

        connector = Workato()

        managed_users = connector.managed_users.get()

        return Response(
            managed_users,
            status=status.HTTP_200_OK
        )
